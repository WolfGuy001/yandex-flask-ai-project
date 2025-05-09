from flask import Flask, render_template, redirect, request, Response, stream_with_context
from data import db_session
from data.users import User
from data.reviews import Reviews
from data.login import LoginForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from ollama import chat


# Инициализация Flask-приложения и настройка авторизации
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Имя модели для генерации рецензий
AI_MODEL = 'yandex/YandexGPT-5-Lite-8B-instruct-GGUF:latest'


def main():
    db_session.global_init("db/database.db")
    app.run(debug=True)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", title="Главная")


@app.route("/review", methods=['GET', 'POST'])
def review():
    db_sess = db_session.create_session()
    current_review = None
    
    if request.method == 'POST' and current_user.is_authenticated:
        task = request.form.get('task')
        source_text = request.form.get('source_text')
        text = request.form.get('text')
        
        if task and text:
            # Проверяем, указан ли исходный текст
            if not source_text:
                source_text = "нет"
            
            # Создаем новую рецензию сначала без AI рецензии
            review = Reviews(
                task=task,
                source_text=source_text,
                text=text,
                ai_review="",  # Пустая рецензия, будет заполнена через стриминг
                user_id=current_user.id
            )
            
            db_sess.add(review)
            db_sess.commit()
            current_review = review
    
    if current_user.is_authenticated and not current_review:
        # Показываем последнюю рецензию пользователя
        latest_review = db_sess.query(Reviews).filter(
            Reviews.user_id == current_user.id
        ).order_by(Reviews.created_date.desc()).first()
        current_review = latest_review

    return render_template("review.html", current_review=current_review, title="Рецензия")


@app.route('/stream_review/<int:review_id>')
@login_required
def stream_review(review_id):
    db_sess = db_session.create_session()
    review = db_sess.query(Reviews).filter(Reviews.id == review_id, 
                                          Reviews.user_id == current_user.id).first()
    
    if not review:
        return Response("Рецензия не найдена", mimetype='text/plain')
    
    def generate():
        # Генерируем рецензию с помощью ollama
        ai_review = ""
        
        prompt = create_review_prompt(review.task, review.source_text, review.text)
        
        try:
            stream = chat(
                model=AI_MODEL,
                messages=[{'role': 'user', 'content': prompt}],
                stream=True,
            )
            
            for chunk in stream:
                content = chunk['message']['content']
                ai_review += content
                yield f"data: {content}\n\n"
            
            # После завершения стриминга сохраняем полную рецензию в базу данных
            review.ai_review = ai_review
            db_sess.commit()
        except Exception as e:
            # В случае ошибки генерируем сообщение об ошибке
            error_message = f"Произошла ошибка при генерации рецензии: {str(e)}"
            yield f"data: {error_message}\n\n"
            
        yield "data: [DONE]\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route("/history")
def history():
    db_sess = db_session.create_session()
    
    if current_user.is_authenticated:
        reviews = db_sess.query(Reviews).filter(
            Reviews.user_id == current_user.id
        ).order_by(Reviews.created_date.desc()).all()
    else:
        reviews = []
    
    return render_template("history.html", reviews=reviews, title="История рецензий")


@app.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):

    db_sess = db_session.create_session()
    review = db_sess.query(Reviews).filter(Reviews.id == review_id, 
                                          Reviews.user_id == current_user.id).first()
    
    if review:
        db_sess.delete(review)
        db_sess.commit()
    
    return redirect('/history')


def create_review_prompt(task, source_text, text):
    prompt = f"""Ты - эксперт по проверке школьных и студенческих сочинений. 
Тебе нужно написать подробную и справедливую рецензию на сочинение по приведенному заданию.

Задание: {task}

Исходный текст: {source_text}

Сочинение: {text}

Напиши подробную рецензию, оценив следующие критерии:
1. Оценка структуры: Проанализируй структуру сочинения, включая вступление, основную часть и заключение. Укажи, насколько логично и последовательно выстроен текст.
2. Раскрытие темы: Определи, насколько полно и глубоко раскрыта тема сочинения. Отметь, соответствует ли содержание заданию.
3. Аргументация: Оцени качество и убедительность аргументов. Определи, насколько хорошо автор обосновывает свою позицию.
4. Грамотность: Выяви грамматические, пунктуационные, лексические и стилистические ошибки (если есть).
5. Общая оценка: Дай общую оценку работы, отметив сильные стороны и аспекты, требующие доработки.
"""
    
    return prompt


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
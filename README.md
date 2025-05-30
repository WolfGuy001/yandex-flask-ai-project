# AI Рецензирование сочинений

Веб-приложение на Flask для автоматического рецензирования сочинений с использованием YandexGPT.

## Описание проекта

Сервис позволяет пользователям загружать задания и тексты сочинений для получения подробной рецензии, генерируемой моделью искусственного интеллекта. Рецензия выводится в реальном времени.

## Функциональность

- Регистрация и авторизация пользователей
- Создание новых рецензий с вводом задания и текста сочинения
- Стриминговый вывод рецензии в реальном времени 
- Сохранение истории рецензий
- Управление рецензиями (просмотр, удаление)

## Структура проекта

- `main.py` - основной файл приложения с маршрутами
- `data/` - модули для работы с базой данных
  - `db_session.py` - настройка сессии БД
  - `users.py` - модель пользователя
  - `reviews.py` - модель рецензии
  - `login.py` - формы авторизации
- `forms/` - формы для работы с данными
  - `user.py` - формы для регистрации
- `templates/` - шаблоны HTML
  - `base.html` - базовый шаблон
  - `index.html` - главная страница
  - `review.html` - страница создания и просмотра рецензии
  - `history.html` - страница истории рецензий
  - `login.html` - страница авторизации
  - `register.html` - страница регистрации
- `db/` - директория с файлом базы данных

## Установка и запуск
Предварительно необходимо установить [ollama](https://ollama.com/)

Далее, последовательтно введите в cmd (ВАЖНО, отключите VPN):
```
ollama run yandex/YandexGPT-5-Lite-8B-instruct-GGUF
/bye
ollama pull ollama run yandex/YandexGPT-5-Lite-8B-instruct-GGUF
```

1. Клонируйте репозиторий:
```
git clone https://github.com/ваш-логин/flask-ai-project.git
cd flask-ai-project
```

2. Создайте и активируйте виртуальное окружение:
```
python -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
.venv\Scripts\activate     # Для Windows
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. Запустите приложение:
```
python main.py
```

## Использование

1. Откройте браузер и перейдите по адресу http://localhost:5000
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите на вкладку "Рецензия" для создания новой рецензии
4. Введите задание и текст сочинения, нажмите "Отправить на рецензию"
5. Наблюдайте за процессом генерации рецензии в реальном времени
6. Просматривайте историю своих рецензий во вкладке "История" 

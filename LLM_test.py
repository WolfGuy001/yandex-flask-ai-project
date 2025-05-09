"""
Пример использования библиотеки ollama для стриминга ответов от языковой модели.
Этот файл можно использовать для тестирования подключения к модели.
"""
from ollama import chat

# Название модели (YandexGPT или другая модель, установленная в Ollama)
MODEL_NAME = 'yandex/YandexGPT-5-Lite-8B-instruct-GGUF:latest'

def test_model_streaming():
    """Функция для тестирования стриминга от языковой модели"""
    print(f"Тестирование модели {MODEL_NAME}...")
    print("Запрос: 'Почему небо голубое?'")
    print("\nОтвет: ", end="")
    
    # Отправляем запрос к модели с включенным стримингом
    stream = chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': 'Почему небо голубое?'}],
        stream=True,
    )
    
    # Выводим ответ по мере его получения
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
    
    print("\n\nТестирование завершено.")

if __name__ == "__main__":
    test_model_streaming()
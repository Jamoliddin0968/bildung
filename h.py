import io

from google.cloud import vision
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('dmtt.json')
client = vision.ImageAnnotatorClient(
    credentials=creds,
)


def detect_text(image_path):
    """Функция для извлечения текста из изображения с использованием Google Cloud Vision API."""

    # Открываем файл изображения
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Создаем объект Image
    image = vision.Image(content=content)

    # Вызываем метод text_detection для распознавания текста
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print('Текст, обнаруженный на изображении:')
        for text in texts:
            print(f"Текст: {text.description}")
            break  # Первый элемент в списке `texts` содержит весь текст

    if response.error.message:
        raise Exception(f"Ошибка API: {response.error.message}")


# Пример использования
image_path = 'image.png'  # Замените на путь к вашему изображению
detect_text(image_path)

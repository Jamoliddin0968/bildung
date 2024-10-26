import os

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Указываем путь к PDF-файлу и директорию для сохранения изображений
pdf_path = 'matematika10page.pdf'
output_folder = 'output_images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


images = []
for i, page in enumerate(convert_from_path(pdf_path)):
    image_path = os.path.join(output_folder, f'page_{i + 1}.png')
    if not os.path.exists(image_path):  # Если изображение еще не создано
        page.save(image_path, 'PNG')
        print(f"Страница {i + 1} сохранена как {image_path}.")
    images.append(image_path)

# Проверим, сколько страниц было сохранено
print(f"Обработано {len(images)} изображений в папку {output_folder}.")

full_text = ""  # Переменная для хранения всего текста из всех страниц
for i, image_path in enumerate(images):
    image = Image.open(image_path)

    # Шаг 3: Применение Tesseract для распознавания текста и формул
    text = pytesseract.image_to_string(
        image)

    # Добавляем распознанный текст страницы в общий текст
    # Добавляем разделитель для страниц
    full_text += f"\n\n--- Page {i + 1} ---\n\n"
    full_text += text
text_output_file = "hhj.txt"
# Шаг 4: Сохранение всего текста в один файл
with open(text_output_file, 'w', encoding='utf-8') as text_file:
    text_file.write(full_text)
    print(f"Весь текст сохранен в {text_output_file}.")

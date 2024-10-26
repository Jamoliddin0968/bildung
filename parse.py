import json
import re

import fitz


def cyrillic_to_latin(text: str) -> str:
    """Функция для преобразования узбекского текста с кириллицы на латиницу."""
    # Словарь для сопоставления кириллических символов их латинским эквивалентам
    cyrillic_to_latin_dict = {
        'А': 'A', 'а': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g',
        'Д': 'D', 'д': 'd',
        'Е': 'E', 'е': 'e',
        'Ё': 'Yo', 'ё': 'yo',
        'Ж': 'J', 'ж': 'j',
        'З': 'Z', 'з': 'z',
        'И': 'I', 'и': 'i',
        'Й': 'Y', 'й': 'y',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        'Х': 'X', 'х': 'x',
        'Ц': 'Ts', 'ц': 'ts',
        'Ч': 'Ch', 'ч': 'ch',
        'Ш': 'Sh', 'ш': 'sh',
        'Щ': 'Sch', 'щ': 'sch',
        'Ъ': '', 'ъ': '',
        'Ы': 'I', 'ы': 'i',
        'Ь': '', 'ь': '',
        'Э': 'E', 'э': 'e',
        'Ю': 'Yu', 'ю': 'yu',
        'Я': 'Ya', 'я': 'ya',
        'Қ': 'Q', 'қ': 'q',
        'Ғ': 'Gʼ', 'ғ': 'gʼ',
        'Ў': 'Oʼ', 'ў': 'oʼ',
        'Ҳ': 'H', 'ҳ': 'h',
    }

    # Преобразуем текст, заменяя каждый символ
    latin_text = ''.join(cyrillic_to_latin_dict.get(char, char)
                         for char in text)
    return latin_text


def normalize(text: str):
    replacements = {
        " ′к": "q",
        "′к": "q",
        "\n′К": "Q",
        "′К": "Q",
        "ˇу": "o'",
        "ˇУ": "O'",
        " -г": "g'",
        "-г": "g'",
        "-Г": "G'",
        " ′х": "h",
        "′х": "h",
        "′Х": "H",

        "′\nК": "Q",
        "′ Х": "H",
        "′\nХ": "H",
        "D)\n": "D)",
    }

    # Проходим по каждому ключу и заменяем в тексте соответствующее значение
    for old_value, new_value in replacements.items():
        text = text.replace(old_value, new_value)

    return text


def extract_text_with_fonts_from_pdf(pdf_document):
    """Извлекаем текст и информацию о шрифтах из PDF."""
    doc = fitz.open(pdf_document)
    all_pages_text = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        page_content = []
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_content = []
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        # Сохраняем каждую часть текста вместе с информацией о шрифте
                        line_content.append({
                            "text": text,
                            "font": font,
                            "size": size
                        })
                    # Добавляем каждую строку на страницу
                    page_content.append(line_content)
        # Сохраняем все текстовые данные и шрифты для каждой страницы
        all_pages_text.append(page_content)

    doc.close()
    return all_pages_text


def generate_answers_json(text_data, correct_answer_font='Fm'):
    """Генерация JSON с правильными ответами на основе шрифтов."""
    correct_answers = {}
    question_code = None
    theme_id = None
    cnt = 0
    prev_text = ""  # Для хранения предыдущего текста

    for page_num, page_content in enumerate(text_data):
        for line_content in page_content:
            for span in line_content:
                text = span["text"]
                font = span["font"]
                size = span["size"]

                if not theme_id:
                    ab_c_match = re.search(r"^(\d+\.\d+-\d+)", text)
                    if ab_c_match:
                        ab_c_value = ab_c_match.group(0)
                        theme_id = ab_c_value

                if not question_code:
                    match = re.search(r"(\d{6})\)", prev_text)
                    if match:
                        # Сохраняем шестизначный код
                        question_code = match.group(1)

                # Логика для поиска правильных ответов
                if font == correct_answer_font and text[:2] in ['A)', 'B)', 'C)', 'D)']:
                    cnt += 1
                    if question_code:
                        print(theme_id)
                        correct_answers[question_code] = {
                            'answer': text[0],
                            'theme_id': theme_id
                        }
                        question_code = None
                        theme_id = None

                prev_text = text

    print(f"Всего правильных ответов: {cnt}")
    return correct_answers


def extract_text_from_pdf(pdf_path):
    """Извлекаем текст в обычном текстовом режиме из PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text("text")  # Извлекаем текст в режиме "text"
    return cyrillic_to_latin(normalize(text))


def parse_questions_and_answers(text: str, correct_answers):
    """Парсим вопросы и ответы из текста и сопоставляем правильные ответы."""
    qa_pattern = re.compile(
        r"\((\d{6})\)\s*(.*?)\nA\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)\nD\)\s*(.*?)(?:\n\d|\Z)", re.S)

    matches = qa_pattern.findall(text)

    qa_list = []
    for match in matches:
        question_number = match[0]  # Шестизначный номер вопроса
        # Удаляем символы новой строки из текста вопроса
        question = match[1].strip().replace("\n", " ")
        # Удаляем символы новой строки из ответов
        answers = {
            "A": match[2].strip().replace("\n", " "),  # Вариант A
            "B": match[3].strip().replace("\n", " "),  # Вариант B
            "C": match[4].strip().replace("\n", " "),  # Вариант C
            "D": match[5].strip().replace("\n", " ")   # Вариант D
        }

        qa_list.append({
            'question_number': question_number,
            'question': question,
            'answers': answers,
            "correct_answer": correct_answers.get(question_number)
        })

    return qa_list


def save_to_json(data, output_path):
    """Сохранение данных в JSON файл."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_txt(qa_list, output_path):
    """Сохранение данных в TXT файл."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pdf_text)  # Разделение между вопросами


# Основной код
pdf_path = "D://documents/tests/kimyo.pdf"  # путь к вашему PDF-файлу
# путь для сохранения результата JSON
output_json_path = 'questions_answers.json'
# путь для сохранения результата TXT
output_txt_path = 'questions_answers.txt'

# Извлекаем текст из PDF
pdf_text = extract_text_from_pdf(pdf_path)
answers_text = extract_text_with_fonts_from_pdf(pdf_path)

# Генерируем JSON с правильными ответами
answer_list = generate_answers_json(answers_text, correct_answer_font='Fn')

# Парсим вопросы и ответы
qa_list = parse_questions_and_answers(pdf_text, answer_list)
print(len(qa_list))
# Сохраняем результат в JSON
save_to_json(qa_list, output_json_path)

# Сохраняем результат в TXT
save_to_txt(pdf_text, output_txt_path)

print(
    f"Вопросы и ответы успешно сохранены в {output_json_path} и {output_txt_path}")

import json
import re

import fitz  # PyMuPDF


# Функция для чтения текста из PDF с помощью PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text("text")  # Извлекаем текст в режиме "text"
    return text

# Функция для поиска вопросов и ответов


def parse_questions_and_answers(text):
    # Регулярное выражение для поиска вопросов, которые начинаются с 6-значного числа
    qa_pattern = re.compile(
        r"\((\d{6})\)\s*(.*?)\nA\)(.*?)\nB\)(.*?)\nC\)(.*?)\nD\)(.*?)\n", re.S)

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
            'answers': answers
        })

    return qa_list

# Сохранение в JSON файл


def save_to_json(qa_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qa_list, f, ensure_ascii=False, indent=4)


# Основной код
pdf_path = "D:/Documents/tests/ona_tili.pdf"
# pdf_path = ''  # путь к вашему PDF-файлу
output_path = 'questions_answers.json'  # путь для сохранения результата

# Извлекаем текст из PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Парсим вопросы и ответы
qa_list = parse_questions_and_answers(pdf_text)
print(len(qa_list))

# Сохраняем результат в JSON
save_to_json(qa_list, output_path)

print(f"Вопросы и ответы успешно сохранены в {output_path}")

import re
import json
from PyPDF2 import PdfReader

def extract_questions_and_answers(text):
    # Регулярные выражения для поиска вопросов и ответов
    question_pattern = re.compile(r"\d+\.\s+(.+?)(?=\nA\))", re.DOTALL)
    answer_pattern = re.compile(r"A\)\s*(.+?)\nB\)\s*(.+?)\nC\)\s*(.+?)\nD\)\s*(.+?)(?=\n|\Z)", re.DOTALL)

    # Найти все вопросы
    questions = question_pattern.findall(text)

    # Найти все варианты ответов
    answers = answer_pattern.findall(text)

    # Создание списка для хранения данных
    data = []

    # Преобразование вопросов и ответов в JSON-совместимый формат
    for i in range(min(len(questions), len(answers))):
        question_data = {
            "question": questions[i].strip(),
            "options": {
                "A": answers[i][0].strip(),
                "B": answers[i][1].strip(),
                "C": answers[i][2].strip(),
                "D": answers[i][3].strip(),
            }
        }
        data.append(question_data)

    return data

def parse_pdf_to_json(pdf_path, output_json_path):
    # Чтение PDF файла
    reader = PdfReader(pdf_path)
    text = ''
    
    # Объединение текста со всех страниц
    for page in reader.pages:
        text += page.extract_text()
    
    # Извлечение вопросов и ответов
    qa_data = extract_questions_and_answers(text)
    
    # Запись данных в JSON файл
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(qa_data, json_file, ensure_ascii=False, indent=4)

    print(f"Parsing completed. Data saved to {output_json_path}")

# Пример использования
parse_pdf_to_json("tarih.pdf", "output.json")

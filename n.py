from PIL import Image
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor


# Функция для постобработки LaTeX
def post_process_latex(result):
    result = result.replace('\\\\', '\n')  # Исправляем символы новой строки
    # Убираем двойные фигурные скобки
    result = result.replace('{{', '{').replace('}}', '}')
    result = result.replace('\\begin{array}{l}', '')  # Убираем начало array
    result = result.replace('\\end{array}', '')  # Убираем конец array
    result = result.replace('\\;', ' ')  # Убираем лишние пробелы
    result = result.replace('\\mathrm{A)}', 'A)')  # Форматируем пункты ответа
    result = result.replace('\\mathrm{B)}', 'B)')
    result = result.replace('\\mathrm{C)}', 'C)')
    result = result.replace('\\mathrm{D)}', 'D)')
    result = result.replace('\\left', '').replace(
        '\\right', '')  # Исправляем скобки
    result = result.replace('$$', '')
    return result

# Функция для разделения вопроса и ответов


def split_question_answers(processed_result):
    lines = processed_result.split('\n')
    question = f"$$ {lines[0]} $$"  # Обрамляем вопрос в LaTeX-блок
    # Форматируем ответы с LaTeX
    answer_A = f"A) $$ {lines[1].replace('A)', '')} $$"
    answer_B = f"B) $$ {lines[2].replace('B)', '')} $$"
    answer_C = f"C) $$ {lines[3].replace('C)', '')} $$"
    answer_D = f"D) $$ {lines[4].replace('D)', '')} $$"
    return question, answer_A, answer_B, answer_C, answer_D


# Загрузка модели и процессора
model = load_model()
processor = load_processor()

# Загружаем изображение
img = Image.open("image.png")

# Получаем результат из модели
results = batch_inference([img], model, processor)
print(results)
# Применяем постобработку к результату
processed_result = post_process_latex(results[0])

# Разделяем на вопрос и ответы
question, answer_A, answer_B, answer_C, answer_D = split_question_answers(
    processed_result)

# Выводим результаты
print("Question:", question)
print("A)", answer_A)
print("B)", answer_B)
print("C)", answer_C)
print("D)", answer_D)

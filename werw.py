import fitz  # PyMuPDF


# Функция для извлечения текста из PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # загружаем страницу
            l = page.get_text()  # извлекаем текст

            print(l)
    return text

# Функция для оборачивания текста в базовый LaTeX-шаблон


def convert_text_to_latex(text):
    # Шаблон для LaTeX-документа
    latex_template = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amssymb}

    \title{PDF to LaTeX}
    \date{}

    \begin{document}

    \maketitle

    \section*{Extracted Content}
    \begin{verbatim}
    {}
    \end{verbatim}

    \end{document}
    """

    # Возвращаем текст, обёрнутый в LaTeX шаблон
    return latex_template.format(text)

# Функция для сохранения LaTeX файла


def save_latex_file(latex_code, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(latex_code)


# Основной блок программы
pdf_path = 'base.pdf'  # Путь к PDF-файлу
output_latex_path = 'output_file.tex'  # Путь для сохранения LaTeX-файла

# Извлечение текста из PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Преобразование текста в LaTeX
latex_code = convert_text_to_latex(pdf_text)

# Сохранение LaTeX-кода в файл
save_latex_file(latex_code, output_latex_path)

print(
    f"PDF был успешно преобразован в LaTeX и сохранён как {output_latex_path}")

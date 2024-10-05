from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTLine, LTTextBox


def extract_underlined_text(pdf_path):
    underlined_text = []

    # Проходим по каждой странице документа
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            # Проверяем, является ли элемент текстовым блоком
            if isinstance(element, LTTextBox):
                for text_line in element:
                    # Для каждого символа в строке проверяем, является ли он подчеркиванием
                    underlined = False
                    line_chars = []
                    for char in text_line:
                        if isinstance(char, LTChar):
                            if 'underline' in char.fontname.lower():  # Проверяем имя шрифта для подчеркивания
                                underlined = True
                            line_chars.append(char.get_text())
                    if underlined:
                        underlined_text.append(''.join(line_chars))

    return underlined_text


pdf_path = "bio.pdf"
underlined_text = extract_underlined_text(pdf_path)

# Выводим подчеркнутый текст
for text in underlined_text:
    print(text)

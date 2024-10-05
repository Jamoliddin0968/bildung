import json
import re

import fitz  # PyMuPDF library for extracting text from PDF


# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf_fitz(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text("text").replace('-\n',
                                                  '').replace('\n', ' ').replace(', ', ',')
    return text

# Function to clean special characters in the extracted text


def clean_text(text):
    replacements = {
        # '¢': '*',  # Replace multiplication symbol
        # '¡': '-',  # Replace subtraction symbol
        # '¶': '/',  # Replace division symbol (if exists)
        # '¼': 'π',  # Replace incorrect symbol for pi
        # 'p': '√'   # Replace incorrect 'p' with square root symbol √
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Fixing incomplete square roots like "2√" -> "2√2"
    # text = re.sub(r'√\s*$', '√2', text)  # If √ is incomplete, add 2 after it
    return text

# Rest of the code for processing remains the same


def parse_questions_from_text(text):
    # Split text by question IDs, such as (XX-X-X)
    question_blocks = re.split(r'(\(\d{2}-\d{1,2}-\d{1,3}\))', text)

    questions = []

    # Iterate over the question blocks
    for i in range(1, len(question_blocks), 2):
        question_id = question_blocks[i]  # Question ID, e.g., (96-1-1)
        question_body = question_blocks[i + 1].strip()  # The question text
        # Extract the question text before any answer options
        question_text = re.split(r'[A-E]\)', question_body)[0].strip()
        if question_id == "(97-9-113)":
            print(question_body)
        # Extract options (A), B), C), etc.), allowing for multi-line answers
        # Split by A), B), etc.
        options_raw = re.split(r'([A-E]\))', question_body)[1:]

        # Clean and combine options
        options = []
        for j in range(0, len(options_raw), 2):
            option_letter = options_raw[j].strip()  # A), B), etc.
            # Multi-line option text
            option_text = options_raw[j +
                                      1].strip()

            # Replace incorrect symbols and format fractions
            option_text = clean_text(option_text)
            option_text = format_fractions_and_clean_options(option_text)

            options.append(f"{option_letter} {option_text}")

        # Append question data
        questions.append({
            'id': question_id.strip('()'),
            'question': question_text,
            'options': options
        })

    return questions

# Function to save questions to a JSON file


def format_fractions_and_clean_options(text):
    # Удаление пробелов между символом √ и числом (например, "√ 3" -> "√3")
    text = re.sub(r'√\s+(\d+)', r'√\1', text)

    # Remove any question numbers like "2.", "3.", etc., at the end of an option
    text = re.sub(r'\d+\.\s*$', '', text)
    text = text.replace('·', '*')
    return text.strip(' ')


def save_to_json(questions, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)

# Main function


# Main function
def main(pdf_path, output_json_path):
    # Extract text from the PDF using PyMuPDF (fitz)
    text = extract_text_from_pdf_fitz(pdf_path)
    print(text[90000:92000])
    # Clean the text by replacing special characters
    cleaned_text = clean_text(text)

    # Parse questions from the cleaned text
    questions = parse_questions_from_text(cleaned_text)

    # Print the number of questions parsed
    print(f"Total number of questions parsed: {len(questions)}")

    # Save the parsed questions as JSON
    save_to_json(questions, output_json_path)

    print(f"Questions successfully parsed and saved to {output_json_path}")


# Running with the provided PDF path
pdf_path = "D:/Documents/tests/ona_tili.pdf"
output_json_path = 'parsed_questions_with_ids.json'
main(pdf_path, output_json_path)

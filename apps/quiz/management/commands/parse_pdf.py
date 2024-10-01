import re
from PyPDF2 import PdfReader
from django.core.management.base import BaseCommand
from apps.quiz.models import Question, Subject, Answer  # Corrected import from apps.quiz.models

class Command(BaseCommand):
    help = "Parse a PDF and load questions and answers into the database"

    def add_arguments(self, parser):
        parser.add_argument('pdf_path', type=str, help="Path to the PDF file")

    def handle(self, *args, **kwargs):
        pdf_path = kwargs['pdf_path']

        # Open and read the PDF file
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Replace common misinterpretations of symbols and fix concatenated numbers/letters
        text = text.replace("¼", "π")  # Replace incorrect characters with the pi symbol
        text = text.replace(";", ",")  # Replace semicolons with commas for proper answer formatting
        text = text.replace("¡", "-")  # Handle the '¡' character as a negative sign
        text = text.replace("²", "^2")  # Handle squared symbols in mathematical expressions
       
        # Fix common issues with concatenated answer parts (e.g., "3C)" to "3 C)")
        text = re.sub(r"(\d+)\s*([A-E]\))", r"\1, \2", text)  # Fix concatenated answers like '3C)' into '3, C)'
        
        # Handle other spacing issues between numbers and letters
        text = re.sub(r"(\d+)([A-E])", r"\1, \2", text)  # Ensure proper space between numbers and answer letters

        # Handle line breaks properly
        text = text.replace("\n", " ")

        # **Step 1: Updated regex pattern to capture question number and code**
        question_with_answer_pattern = re.compile(r"(\d+)\.\s*\((\d+-\d+-\d+)\)\s+(.*?)(?=(\d+\.\s*\(|$))", re.DOTALL)

        # **Step 2: Updated answer regex to handle answers starting directly after the question**
        # We now include A) specifically at the beginning, as it often appears right after the question.
        answer_pattern = re.compile(r"(A)\)\s*([^A-E]+)|([B-E])\)\s*([^A-E]+)")  # Capturing A), B), etc.

        # Step 3: Get all question-answer blocks
        question_answer_blocks = question_with_answer_pattern.findall(text)

        if not question_answer_blocks:
            self.stdout.write(self.style.ERROR("No questions with answers found in the PDF"))
            return

        # Assuming a default subject (you can customize this based on your subject data)
        subject, _ = Subject.objects.get_or_create(name="Mathematics")

        # Step 4: Loop through each extracted question-answer block
        for question_data in question_answer_blocks:
            # question_data[0]: Question number (e.g., 19)
            # question_data[1]: Question code (e.g., 99-2-2)
            # question_data[2]: Question block (rest of the question text and answers)
            question_number, code, question_block = question_data[0], question_data[1], question_data[2]

            # **Keep the original question code as-is (e.g., (97-10-18))**
            print(f"Original Question Code: {code}")

            # Split the question from the answers based on the first occurrence of A)
            question_text_split = re.split(r"[A-E]\)", question_block, maxsplit=1)

            if len(question_text_split) < 2:
                # No answers found after the question, skip this block
                self.stdout.write(self.style.ERROR(f"Skipping question {code} due to missing answers"))
                continue

            question_text = question_text_split[0].strip()  # This is the actual question text
            answers_block = question_text_split[1]           # This is the block that contains the answers

            # Debug print to see the answers block
            print(f"Answers Block for {code}: {answers_block}")

            # Step 5: Now extract the individual answers from the answers block
            # Use the updated regex to ensure A) is captured, even if it appears directly after the question
            answers = answer_pattern.findall(answers_block)

            # Clean up answers and organize them
            parsed_answers = [(m[0] or m[2], m[1] or m[3]) for m in answers]

            # Debug print for answers
            print(f"Parsed Answers for {code}: {parsed_answers}")

            # **Check for at least 4 answers**
            if not parsed_answers or len(parsed_answers) < 4:
                self.stdout.write(self.style.ERROR(f"Skipping question {code} due to incomplete answers (found {len(parsed_answers)} answers)"))
                continue

            # Step 6: Create the question in the database with the original code
            question = Question.objects.create(subject=subject, code=code, text=question_text)

            # Step 7: Collect answers for bulk creation
            answer_objects = []
            for answer_letter, answer_text in parsed_answers:
                answer_objects.append(Answer(question=question, text=answer_text.strip(), is_correct=False))

            # Bulk create the answers
            Answer.objects.bulk_create(answer_objects)

            self.stdout.write(self.style.SUCCESS(f"Added question {code} with {len(parsed_answers)} answers"))

        self.stdout.write(self.style.SUCCESS("PDF parsing and database population completed successfully"))

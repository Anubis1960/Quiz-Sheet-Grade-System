from io import BytesIO
import os
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from textwrap import wrap

# Define constants for layout
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20
QR_CODE_SIZE = 80
TITLE_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 14
TEXT_FONT_SIZE = 12
SPACING = 15
STUDENT_ID_BOX_WIDTH = 200
STUDENT_ID_BOX_HEIGHT = 40
BUBBLE_SHEET_HEIGHT = 500
BUBBLE_SHEET_MARGIN = 200
STUDENT_ID_BOX_MARGIN = 120
QUESTION_SPACING = 20


def generate_pdf(quiz_id: str, quiz_data: dict, teacher_name: str) -> BytesIO:
    """
    Generates a PDF for the quiz including a bubble sheet, QR code, title, description,
    teacher's name, and a student ID box. Additionally, it includes a page for questions.

    Args:
        quiz_id (str): The unique identifier for the quiz (used for QR code).
        quiz_data (dict): A dictionary containing quiz title, description, and questions.
        teacher_name (str): The name of the teacher for the quiz.

    Returns:
        BytesIO: A file-like object containing the generated PDF.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # Fixed position for the bubble sheet
    bubble_sheet_y_position = MARGIN + 10  # 10 points spacing from the bottom
    add_bubble_sheet(c, os.path.join(os.path.dirname(__file__), "sheet.png"), bubble_sheet_y_position)

    # Add a QR code with the quiz ID
    add_qr_code(c, quiz_id)

    # Add the title
    title_y = PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING
    add_title(c, quiz_data["title"], title_y)

    # Add the description and teacher
    add_description_and_teacher(c, quiz_data["description"], teacher_name, title_y)

    student_y_position = bubble_sheet_y_position + BUBBLE_SHEET_HEIGHT + SPACING

    # Add a box for the student ID
    add_student_id_box(c, student_y_position)

    # Start a new page for questions
    c.showPage()
    add_questions(c, quiz_data["questions"])

    # Save the PDF
    c.save()
    buf.seek(0)

    return buf


def add_qr_code(c: canvas.Canvas, quiz_id: str):
    """
    Adds a QR code to the PDF at the specified location.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        quiz_id (str): The unique quiz identifier to encode in the QR code.

    Returns:
        None
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(quiz_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    qr_image = ImageReader(img_io)

    qr_y = PAGE_HEIGHT - MARGIN - QR_CODE_SIZE
    c.drawImage(qr_image, MARGIN, qr_y, width=QR_CODE_SIZE, height=QR_CODE_SIZE)


def add_title(c: canvas.Canvas, title: str, y_position: float):
    """
    Adds the quiz title to the PDF at the specified Y position.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        title (str): The title of the quiz.
        y_position (float): The Y position to place the title.

    Returns:
        None
    """
    c.setFont("Helvetica-Bold", TITLE_FONT_SIZE)
    c.drawCentredString(PAGE_WIDTH / 2, y_position, title)


def add_description_and_teacher(c: canvas.Canvas, description: str, teacher: str, y_position: float) -> float:
    """
    Adds the quiz description and teacher's name to the PDF.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        description (str): The description of the quiz.
        teacher (str): The teacher's name.
        y_position (float): The starting Y position to draw the text.

    Returns:
        float: The Y position after the description and teacher text have been added.
    """
    c.setFont("Helvetica", SUBTITLE_FONT_SIZE)

    description_lines = wrap(description, 90)  # Wrap description text
    desc_y = y_position - SUBTITLE_FONT_SIZE - SPACING

    for line in description_lines:
        c.drawString(MARGIN, desc_y, line)
        desc_y -= SPACING

    teacher_y = desc_y - SPACING
    c.drawString(MARGIN, teacher_y, f"Teacher: {teacher}")

    return teacher_y - SPACING


def add_student_id_box(c: canvas.Canvas, y_position: float) -> float:
    """
    Adds a box for the student ID to the PDF.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        y_position (float): The Y position to place the student ID box.

    Returns:
        float: The Y position after the student ID box has been drawn.
    """
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    student_id_label_y = y_position + SPACING

    c.drawString(MARGIN, student_id_label_y, "Student ID:")
    c.rect(STUDENT_ID_BOX_MARGIN, student_id_label_y, STUDENT_ID_BOX_WIDTH, STUDENT_ID_BOX_HEIGHT)

    return student_id_label_y - SPACING


def add_bubble_sheet(c: canvas.Canvas, image_path: str, y_position: float):
    """
    Adds an image (bubble sheet) to the PDF at the specified location and size.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        image_path (str): The path to the bubble sheet image.
        y_position (float): The Y position to place the image.

    Returns:
        None
    """
    c.drawImage(image_path, MARGIN, y_position, width=PAGE_WIDTH - BUBBLE_SHEET_MARGIN, height=BUBBLE_SHEET_HEIGHT)


def add_questions(c: canvas.Canvas, questions: list):
    """
    Adds the quiz questions and options to the PDF.

    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        questions (list): A list of question dictionaries, where each contains the question text and options.

    Returns:
        None
    """
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    y = PAGE_HEIGHT - MARGIN

    for q_index, question in enumerate(questions):
        # Wrap question text
        question_text_lines = wrap(f"{q_index + 1}: {question['text']}", 90)
        question_height = len(question_text_lines) * SPACING

        # Prepare options lines
        option_lines = []
        max_line_width = 90  # Maximum characters per line

        for i, option in enumerate(question['options']):
            wrapped_option = wrap(f"{chr(65 + i)}. {option}", max_line_width)
            option_lines.extend(wrapped_option)

        options_height = len(option_lines) * SPACING

        # Check if question and options fit on the current page
        total_height = question_height + options_height + QUESTION_SPACING
        if y - total_height < MARGIN:
            c.showPage()
            y = PAGE_HEIGHT - MARGIN
            c.setFont("Helvetica", TEXT_FONT_SIZE)

        # Draw question text
        for line in question_text_lines:
            c.drawString(MARGIN, y, line)
            y -= SPACING

        # Draw options
        for line in option_lines:
            c.drawString(MARGIN, y, line)
            y -= SPACING

        # Add spacing between questions
        y -= QUESTION_SPACING


if __name__ == '__main__':
    q_data = {
        "description": "Description of "
                       "Quizfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfgfg"
                       "fgfgdghghghghghghghghghghghghghghghghghghghghghghgh 1",
        "questions": [
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is "
                        "2+2"
                        "?aaaaaaaaaaaaaaaaaaaaaaaaaffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
                        "fffffaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "33333333333333333333333333333333333333333333333333333333hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh33333333333333333333333333333333333333333333333333",
                    "4",
                    "5"
                ],
                "text": "What is 2+2?"
            },
            {
                "correct_answers": [
                    "1"
                ],
                "options": [
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                ],
                "text": "What is 2+2?"
            }
        ],
        "teacher": "John Dadaoe",
        "title": "Quiz Ti4tle 1"
    }

    q_id = "5HOnQYKhJtrnC0MMDDFk"
    b = generate_pdf(q_id, q_data, "John Dadaoe")

    with open(f"{q_id}.pdf", "wb") as f:
        f.write(b.read())

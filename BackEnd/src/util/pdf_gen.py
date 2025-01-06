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
STUDENT_ID_BOX_HEIGHT = 20
BUBBLE_SHEET_HEIGHT = 500
BUBBLE_SHEET_MARGIN = 200
STUDENT_ID_BOX_MARGIN = 120


def generate_pdf(quiz_id: str, quiz_data: dict) -> BytesIO:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # Fixed position for the bubble sheet
    bubble_sheet_y_position = MARGIN + 10  # 10 points spacing from the bottom
    add_bubble_sheet(c, os.path.join(os.path.dirname(__file__), "ftest.png"), bubble_sheet_y_position)

    # Add a QR code with the quiz ID
    add_qr_code(c, quiz_id)

    # Add the title
    title_y = PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING
    add_title(c, quiz_data["title"], title_y)

    # Add the description and teacher
    add_description_and_teacher(c, quiz_data["description"], quiz_data["teacher"], title_y)

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
    c.setFont("Helvetica-Bold", TITLE_FONT_SIZE)
    c.drawCentredString(PAGE_WIDTH / 2, y_position, title)


def add_description_and_teacher(c: canvas.Canvas, description: str, teacher: str, y_position: float) -> float:
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
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    student_id_label_y = y_position + SPACING

    c.drawString(MARGIN, student_id_label_y, "Student ID:")
    c.rect(STUDENT_ID_BOX_MARGIN, student_id_label_y, STUDENT_ID_BOX_WIDTH, STUDENT_ID_BOX_HEIGHT)

    return student_id_label_y - SPACING


def add_bubble_sheet(c: canvas.Canvas, image_path: str, y_position: float):
    c.drawImage(image_path, MARGIN, y_position, width=PAGE_WIDTH - BUBBLE_SHEET_MARGIN, height=BUBBLE_SHEET_HEIGHT)


def add_questions(c: canvas.Canvas, questions: list):
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    y = PAGE_HEIGHT - MARGIN

    for q_index, question in enumerate(questions):
        wall_txt = [f"{q_index + 1}: {question['text']}"]
        for o_idx, option in enumerate(question["options"]):
            wall_txt.append(f"  {chr(65 + o_idx)}. {option}")

        for line in wall_txt:
            y -= SPACING
            y -= SPACING
            lines = wrap(line, 90)
            for l in lines:
                c.drawString(MARGIN, y, l)
                y -= SPACING
                if y < MARGIN:
                    c.showPage()
                    y = PAGE_HEIGHT - MARGIN
                    c.setFont("Helvetica", TEXT_FONT_SIZE)
                    c.drawString(MARGIN, y, l)
                    y -= SPACING


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
                    "33333333333333333333333333333333333333333333333333333333hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
                    "hhh33333333333333333333333333333333333333333333333333",
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

    q_id = "1234"
    b = generate_pdf(q_id, q_data)

    with open(f"{q_id}.pdf", "wb") as f:
        f.write(b.read())

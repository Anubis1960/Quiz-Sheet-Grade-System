from io import BytesIO
import os
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from src.models.question import Question

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


def generate_pdf(quiz_id: str, quiz_data: dict) -> BytesIO:
    print(quiz_data)
    print(quiz_id)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # Layout functions
    add_qr_code(c, quiz_id)
    add_title(c, quiz_data["title"])
    add_description_and_teacher(c, quiz_data["description"], quiz_data["teacher"])
    add_student_id_box(c)

    img_path = os.path.join(os.path.dirname(__file__), "FINAL.png")
    add_bubble_sheet(c, img_path)
    # Start new page for questions
    c.showPage()
    add_questions(c, quiz_data["questions"])

    # Save the PDF
    c.save()
    buf.seek(0)

    return buf


def add_qr_code(c: canvas.Canvas, quiz_id: str):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(quiz_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to ImageReader and draw on canvas
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    qr_image = ImageReader(img_io)

    # Position: Top-left corner
    c.drawImage(qr_image, MARGIN, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE, width=QR_CODE_SIZE, height=QR_CODE_SIZE)


def add_title(c: canvas.Canvas, title: str):
    c.setFont("Helvetica-Bold", TITLE_FONT_SIZE)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING, title)


def add_description_and_teacher(c: canvas.Canvas, description: str, teacher: str):
    c.setFont("Helvetica", SUBTITLE_FONT_SIZE)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING * 3, f"Description: {description}")
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING * 4, f"Teacher: {teacher}")


def add_student_id_box(c: canvas.Canvas):
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING * 6, "Student ID:")
    c.rect(MARGIN + 100, PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING * 7, STUDENT_ID_BOX_WIDTH, STUDENT_ID_BOX_HEIGHT)


def add_bubble_sheet(c: canvas.Canvas, image_path: str):
    bubble_y = PAGE_HEIGHT - MARGIN - QR_CODE_SIZE - SPACING * 10 - BUBBLE_SHEET_HEIGHT
    c.drawImage(image_path, MARGIN, bubble_y, width=PAGE_WIDTH - BUBBLE_SHEET_MARGIN, height=BUBBLE_SHEET_HEIGHT)


def add_questions(c: canvas.Canvas, questions: list):
    c.setFont("Helvetica", TEXT_FONT_SIZE)
    y = PAGE_HEIGHT - MARGIN
    max_line_width = PAGE_WIDTH - 2 * MARGIN  # Maximum usable width for text
    answer_spacing = 120  # Space between answers in the same line

    for q_index, question in enumerate(questions):
        # Question text
        y -= SPACING
        c.drawString(MARGIN, y, f"{q_index + 1}. {question['text']}")
        y -= SPACING

        # Answer choices on the same line if space permits
        x = MARGIN
        for ch_index, choice in enumerate(question['options']):
            answer_text = f"{chr(65 + ch_index)}) {choice}"  # Capitalize letters (A, B, C, ...)
            text_width = c.stringWidth(answer_text, "Helvetica", TEXT_FONT_SIZE)

            if x + text_width > max_line_width:  # Move to the next line if no space
                x = MARGIN
                y -= SPACING

            c.drawString(x, y, answer_text)
            x += answer_spacing  # Increment position for the next answer

        y -= SPACING  # Add spacing after answers

        # Start a new page if space runs out
        if y < MARGIN:
            c.showPage()
            c.setFont("Helvetica", TEXT_FONT_SIZE)
            y = PAGE_HEIGHT - MARGIN


if __name__ == '__main__':
    q_data = {
        "title": "Sample Quiz",
        "description": "This is a sample quiz.",
        "teacher": "John Doe",
        "questions": [
            {
                "text": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
            },
            {
                "text": "What is the capital of Germany?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
            },
        ],
    }

    q_id = "1234"
    b = generate_pdf(q_id, q_data)

    with open(f"{q_id}.pdf", "wb") as f:
        f.write(b.read())
        f.close()
Module src.util.pdf_gen
=======================

Functions
---------

`add_bubble_sheet(c: reportlab.pdfgen.canvas.Canvas, image_path: str, x_position: float, y_position: float, width: float, height: float)`
:   Adds an image (bubble sheet) to the PDF at the specified location and size.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        image_path (str): The path to the bubble sheet image.
        x_position (float): The X position to place the image.
        y_position (float): The Y position to place the image.
        width (float): The width of the image.
        height (float): The height of the image.
    
    Returns:
        None

`add_description_and_teacher(c: reportlab.pdfgen.canvas.Canvas, description: str, teacher: str, y_position: float) ‑> float`
:   Adds the quiz description and teacher's name to the PDF.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        description (str): The description of the quiz.
        teacher (str): The teacher's name.
        y_position (float): The starting Y position to draw the text.
    
    Returns:
        float: The Y position after the description and teacher text have been added.

`add_qr_code(c: reportlab.pdfgen.canvas.Canvas, quiz_id: str)`
:   Adds a QR code to the PDF at the specified location.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        quiz_id (str): The unique quiz identifier to encode in the QR code.
    
    Returns:
        None

`add_questions(c: reportlab.pdfgen.canvas.Canvas, questions: list)`
:   Adds the quiz questions and options to the PDF.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        questions (list): A list of question dictionaries, where each contains the question text and options.
    
    Returns:
        None

`add_student_id_box(c: reportlab.pdfgen.canvas.Canvas, y_position: float) ‑> float`
:   Adds a box for the student ID to the PDF.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        y_position (float): The Y position to place the student ID box.
    
    Returns:
        float: The Y position after the student ID box has been drawn.

`add_title(c: reportlab.pdfgen.canvas.Canvas, title: str, y_position: float)`
:   Adds the quiz title to the PDF at the specified Y position.
    
    Args:
        c (canvas.Canvas): The reportlab canvas to draw on.
        title (str): The title of the quiz.
        y_position (float): The Y position to place the title.
    
    Returns:
        None

`generate_pdf(quiz_id: str, quiz_data: dict, teacher_name: str) ‑> _io.BytesIO`
:   Generates a PDF for the quiz including a bubble sheet, QR code, title, description,
    teacher's name, and a student ID box. Additionally, it includes a page for questions.
    
    Args:
        quiz_id (str): The unique identifier for the quiz (used for QR code).
        quiz_data (dict): A dictionary containing quiz title, description, and questions.
        teacher_name (str): The name of the teacher for the quiz.
    
    Returns:
        BytesIO: A file-like object containing the generated PDF.
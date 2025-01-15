import imutils
from imutils.perspective import four_point_transform
from numpy import ndarray
from qreader import QReader

from src.util.pdf_gen import *
from src.util.text_recognition.process_text import *


def retry_on_failure(image: MatLike) -> ndarray | None:
    """
    Attempts to process an image and extract the document region even if initial processing fails.
    It applies several image processing techniques to find and extract the document.

    Args:
        image (MatLike): The input image to process.

    Returns:
        ndarray | None: The extracted document region, or None if extraction fails.
    """
    # Rescale image to fit a consistent size
    image = rescale_image(image)

    # Convert to grayscale, apply Gaussian blur and edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # Find external contours in the edge-detected image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Set minimum and maximum area for document contours
    doc_cnt = None
    min_area = 0.5 * image.shape[0] * image.shape[1]
    max_area = 0.95 * image.shape[0] * image.shape[1]

    if len(cnts) > 0:
        # Sort contours by area and check for a quadrilateral contour
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            area = cv2.contourArea(c)
            if min_area < area < max_area:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4:  # Quadrilateral detected
                    doc_cnt = approx
                    break
    else:
        # If no contours found, return None
        return None

    if doc_cnt is None:
        # If no document contour found, return None
        return None

    # Apply perspective transform to extract the document
    paper = four_point_transform(image, doc_cnt.reshape(4, 2))
    return paper


def get_document_contours(image: MatLike) -> None | ndarray:
    """
    Attempts to extract the document from an image by detecting its contours.
    This function is used to detect the document region, resize it, and apply edge detection.

    Args:
        image (MatLike): The input image to process.

    Returns:
        None | ndarray: The extracted document region, or None if extraction fails.
    """
    # Rescale the image for consistent size
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    copy = imutils.resize(image, height=500)

    # Convert to grayscale, apply Gaussian blur and edge detection
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    doc_cnt = None
    # Loop over the contours to find a quadrilateral
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            doc_cnt = approx
            break

    if doc_cnt is None:
        # If no document contour found, return None
        return None

    # Apply perspective transform to extract the document
    paper = four_point_transform(orig, doc_cnt.reshape(4, 2) * ratio)
    return paper


def rescale_image(image: MatLike, width: int = 595, height: int = 842) -> MatLike:
    """
    Rescales the image to a specified width and height.

    Args:
        image (MatLike): The input image to be rescaled.
        width (int): The target width.
        height (int): The target height.

    Returns:
        MatLike: The rescaled image.
    """
    scaled_image = cv2.resize(image, (width, height))
    return scaled_image


def parser(image: MatLike) -> tuple[ndarray | None, str, str]:
    """
    Processes an image, scans for a QR code, detects the document, extracts the student ID,
    and returns the processed data including bubble sheet and quiz ID.

    Args:
        image (MatLike): The input image to process.

    Returns:
        tuple: A tuple containing the bubble sheet (ndarray), student ID (str), and quiz ID (str).
    """
    copy = image.copy()

    # Try scanning the QR code multiple times
    quiz_id = scan_qr_code(image)
    tries = 0
    while quiz_id == "" and tries < 10:
        quiz_id = scan_qr_code(image)
        tries += 1

    # Rescale the image for document extraction
    image = rescale_image(image)
    if quiz_id == "":
        quiz_id = scan_qr_code(image)
        tries = 0
        while quiz_id == "" and tries < 10:
            quiz_id = scan_qr_code(image)
            tries += 1

    # Extract the document from the image
    paper = get_document_contours(image)

    if paper is None:
        # If no document is found, attempt retry processing
        paper = retry_on_failure(copy)
        if paper is None:
            return None, "", ""  # Return empty values if no document found

    paper = rescale_image(paper)

    # Crop the bubble sheet and student ID box from the paper
    bubble_sheet = crop_bubble_sheet(paper)
    student_id_box = crop_id_box(paper)

    # Read the student ID from the cropped box
    student_id = read_id(student_id_box)

    return bubble_sheet, student_id, quiz_id


def crop_bubble_sheet(paper: MatLike) -> list[ndarray]:
    """
    Crops the bubble sheet section from the document based on predefined coordinates.

    Args:
        paper (MatLike): The document image from which to extract the bubble sheet.

    Returns:
        list[ndarray]: A list of cropped bubble sheets.
    """
    bubble_sheets = []
    bubble_width = int(BUBBLE_SHEET_MARGIN / 3)
    bubble_height = int(BUBBLE_SHEET_HEIGHT)

    bubble_y = int(PAGE_HEIGHT - (MARGIN + bubble_height))  # Bottom-aligned bubbles
    bubble_x = BUBBLE_SHEET_X

    # Loop to crop multiple bubble sheets (adjusting the X-coordinate each time)
    for i in range(3):
        cropped_sheet = paper[
                        bubble_y - 10:bubble_y + bubble_height + 20,  # Y-coordinates
                        bubble_x:bubble_x + bubble_width + 10  # X-coordinates
                        ]
        cropped_sheet = rescale_image(cropped_sheet, width=455, height=749)
        bubble_sheets.append(cropped_sheet)
        bubble_x += bubble_width  # Shift X to next bubble

    return bubble_sheets


def crop_id_box(paper: MatLike) -> MatLike:
    """
    Crops the student ID box section from the document.

    Args:
        paper (MatLike): The document image from which to extract the student ID box.

    Returns:
        MatLike: The cropped student ID box.
    """
    student_id_box_y = int(PAGE_HEIGHT - BUBBLE_SHEET_HEIGHT - MARGIN - 2 * SPACING - STUDENT_ID_BOX_HEIGHT)
    student_id_box_x = STUDENT_ID_BOX_MARGIN

    student_id_box = paper[student_id_box_y - 10:student_id_box_y + STUDENT_ID_BOX_HEIGHT + 10,
                     student_id_box_x - 10:student_id_box_x + STUDENT_ID_BOX_WIDTH + 10]

    return student_id_box


def scan_qr_code(image: MatLike) -> str:
    """
    Scans a QR code from the given image using the QReader library.

    Args:
        image (MatLike): The image to scan for a QR code.

    Returns:
        str: The QR code data, if found, otherwise an empty string.
    """
    qreader = QReader()
    decoded_text = qreader.detect_and_decode(image=image)
    return decoded_text[0]  # Return the decoded text from the QR code


if __name__ == "__main__":
    img = cv2.imread("30sh.JPG")  # Load an image for processing
    parser(img)  # Call the parser to process the image
    cv2.waitKey(0)  # Wait for a key press to close the image window
    cv2.destroyAllWindows()  # Close all OpenCV windows

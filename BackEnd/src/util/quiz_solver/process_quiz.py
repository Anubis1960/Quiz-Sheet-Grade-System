import imutils
from imutils.perspective import four_point_transform
from numpy import ndarray
from qreader import QReader

from src.util.pdf_gen import *
from src.util.text_recognition.process_text import *


def retry_on_failure(image: MatLike) -> ndarray | None:
    image = rescale_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    cnts = cv2.findContours(
        edged.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)
    doc_cnt = None
    min_area = 0.5 * image.shape[0] * image.shape[1]
    max_area = 0.95 * image.shape[0] * image.shape[1]

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:
            area = cv2.contourArea(c)
            if min_area < area < max_area:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4:
                    doc_cnt = approx
                    break
    else:
        # print("No contours found")
        return None

    if doc_cnt is None:
        # print("No document found")
        return None

    paper = four_point_transform(image, doc_cnt.reshape(4, 2))
    return paper


def get_document_contours(image: MatLike) -> None | ndarray:
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    copy = imutils.resize(image, height=500)
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    doc_cnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            doc_cnt = approx
            break

    if doc_cnt is None:
        # print("No document found")
        return None

    paper = four_point_transform(orig, doc_cnt.reshape(4, 2) * ratio)
    return paper


def rescale_image(image: MatLike, width: int = 595, height: int = 842) -> MatLike:
    scaled_image = cv2.resize(image, (width, height))
    return scaled_image


def parser(image: MatLike) -> tuple[ndarray | None, str, str]:
    copy = image.copy()

    quiz_id = scan_qr_code(image)
    tries = 0
    while quiz_id == "" and tries < 10:
        quiz_id = scan_qr_code(image)
        tries += 1

    image = rescale_image(image)
    if quiz_id == "":
        quiz_id = scan_qr_code(image)
        tries = 0
        while quiz_id == "" and tries < 10:
            quiz_id = scan_qr_code(image)
            tries += 1

    paper = get_document_contours(image)

    if paper is None:
        paper = retry_on_failure(copy)
        if paper is None:
            return None, "", ""
    paper = rescale_image(paper)

    # cv2.imshow("Paper", paper)
    # cv2.waitKey(0)

    bubble_sheet = crop_bubble_sheet(paper)

    student_id_box = crop_id_box(paper)

    student_id = read_id(student_id_box)

    return bubble_sheet, student_id, quiz_id


def crop_bubble_sheet(paper: MatLike) -> list[ndarray]:
    # Dynamically calculate bubble sheet coordinates using constants and scaling
    bubble_sheets = []
    bubble_width = int(BUBBLE_SHEET_MARGIN / 3)
    bubble_height = int(BUBBLE_SHEET_HEIGHT)

    # Start position
    bubble_y = int(PAGE_HEIGHT - (MARGIN + bubble_height))  # Align to bottom
    bubble_x = BUBBLE_SHEET_X
    for i in range(3):
        print(f"X: {bubble_x}, Y: {bubble_y}")

        # Crop the bubble sheet from the paper with a small buffer
        cropped_sheet = paper[
                        bubble_y - 10:bubble_y + bubble_height + 20,  # Y-coordinates
                        bubble_x:bubble_x + bubble_width + 10  # X-coordinates
                        ]
        cropped_sheet = rescale_image(cropped_sheet, width=455, height=749)
        bubble_sheets.append(cropped_sheet)
        bubble_x += bubble_width

    return bubble_sheets


def crop_id_box(paper: MatLike) -> MatLike:
    # Dynamically calculate student ID box coordinates using constants and scaling
    student_id_box_y = int(PAGE_HEIGHT - BUBBLE_SHEET_HEIGHT - MARGIN - 2 * SPACING - STUDENT_ID_BOX_HEIGHT)
    student_id_box_x = STUDENT_ID_BOX_MARGIN

    student_id_box = paper[student_id_box_y - 10:student_id_box_y + STUDENT_ID_BOX_HEIGHT + 10,
                     student_id_box_x - 10:student_id_box_x + STUDENT_ID_BOX_WIDTH + 10]

    return student_id_box


def scan_qr_code(image: MatLike) -> str:
    qreader = QReader()
    decoded_text = qreader.detect_and_decode(image=image)
    # print(f"Decoded text: {decoded_text[0]}")
    return decoded_text[0]


if __name__ == "__main__":
    img = cv2.imread("30sh.JPG")
    parser(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

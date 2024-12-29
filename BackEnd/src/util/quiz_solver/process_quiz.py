from cv2.typing import MatLike
from imutils.perspective import four_point_transform
from typing import Dict, List
from imutils import contours
import numpy as np
import imutils
import matplotlib.pyplot as plt
import cv2
import qrcode
from src.util.quiz_solver.bubble_solver import *
from src.util.pdf_gen import *

def get_document_contours(image: MatLike) -> MatLike:
    cnts = cv2.findContours(
        image.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)
    doc_cnt = None

    if len(cnts) > 0:
        # sorting the contours according to their size in descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # looping over the sorted contours
        for c in cnts:
            # approximating the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we can assume we have found the paper
            if len(approx) == 4:
                doc_cnt = approx
    else:
        print("No contours found")
        return None

    if doc_cnt is None:
        print("No document found")
        return None

    return doc_cnt


def rescale_image(image, width=595, height=842):
    print(f"Original image size: {image.shape}")
    scaled_image = cv2.resize(image, (width, height))
    print(f"Scaled image size: {scaled_image.shape}")
    return scaled_image


def parser(img: str):
    image = cv2.imread(img)

    # Convert the image to grayscale, blur it, and find edges in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # Extract the document contours
    img_contoured = get_document_contours(edged)

    if img_contoured is not None:
        # Perform a perspective transformation to isolate the document
        paper = four_point_transform(image, img_contoured.reshape(4, 2))

    # Attempt to scan the QR code to retrieve the quiz ID
    quiz_id = scan_qr_code(paper)
    tries = 0
    while quiz_id == "" and tries < 10:
        quiz_id = scan_qr_code(paper)
        tries += 1

    # Rescale the paper to A4 size for consistent coordinates
    paper = rescale_image(paper)

    bubble_sheet = crop_bubble_sheet(paper)

    # Parse the quiz from the bubble sheet (replace with actual parsing logic)
    quiz_data = parse_quiz(bubble_sheet)
    return quiz_data

def crop_bubble_sheet(paper: MatLike) -> MatLike:
    # Dynamically calculate bubble sheet coordinates using constants and scaling
    bubble_sheet_y_position = MARGIN + 10  # Positioned 10 points from the bottom of the page

    bubble_x = MARGIN
    bubble_y = int(PAGE_HEIGHT - bubble_sheet_y_position - BUBBLE_SHEET_HEIGHT)  # Adjust to bottom alignment
    bubble_width = int(PAGE_WIDTH - BUBBLE_SHEET_MARGIN)
    bubble_height = int(BUBBLE_SHEET_HEIGHT)

    # Crop the bubble sheet from the paper
    bubble_sheet = paper[bubble_y:bubble_y + bubble_height, bubble_x:bubble_x + bubble_width]

    return bubble_sheet

def scan_qr_code(image):
    # load the input image

    # find the qrcode in the image
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)

    # if there is a qrcode present
    if bbox is not None:
        return data
    return ""

if __name__ == "__main__":
    parser("exam2.png")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

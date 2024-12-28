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

def parser(img: str):
    image = cv2.imread(img)

    # convert the image to grayscale, blur it, and find edges in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply GaussianBlur to the gray image to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply Canny edge detection to find the edges in the image
    edged = cv2.Canny(blurred, 75, 200)

    img_contured = get_document_contours(edged)

    if img_contured is not None:
        paper = four_point_transform(image, img_contured.reshape(4, 2))
    #     warped = four_point_transform(gray, img_contured.reshape(4, 2))
    #     thresh = cv2.threshold(warped, 0, 255,
    #                            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    #                            )[1]
    # else:
    #     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    #                            )[1]

    cv2.imshow("paper", paper)

    quiz_id = scan_qr_code(paper)
    while quiz_id == "":
        quiz_id = scan_qr_code(paper)



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
    parser("sample_exam.png")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

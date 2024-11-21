from cv2.typing import MatLike
from imutils.perspective import four_point_transform
from typing import Dict, List
from imutils import contours
import numpy as np
import imutils
import matplotlib.pyplot as plt
import cv2


def get_bubble_contours(thresh: MatLike) -> MatLike:
    # finding contours in the thresholded image, then initializing the list of contours that correspond to questions
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    question_cnts = []
    # looping over the contours
    for c in cnts:
        # computing the bounding box of the contour, then using the bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        print(f"Width: {w}, Height: {h}, Aspect Ratio: {ar}")
        # in order to label the contour as a question, region should be sufficiently wide, sufficiently tall,
        # and have an aspect ratio approximately equal to 1
        if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
            question_cnts.append(c)

    # sorting the question contours top-to-bottom, then initializing the total number of correct answers
    question_cnts = contours.sort_contours(question_cnts, method="top-to-bottom")[0]

    return question_cnts


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

    if img_contured is None:
        thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                               )[1]
    else:
        paper = four_point_transform(image, img_contured.reshape(4, 2))
        warped = four_point_transform(gray, img_contured.reshape(4, 2))
        thresh = cv2.threshold(warped, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                               )[1]

    bubble_contours = [
        c for c in get_bubble_contours(thresh)
    ]

    if img_contured is not None:
        return check_image(thresh, paper, bubble_contours, QUESTIONS, nz_threshold=1000)
    else:
        return check_image(thresh, image, bubble_contours, QUESTIONS, nz_threshold=1400)


def check_image(thresh: MatLike, paper: MatLike, bubble_contours: List[MatLike], questions: Dict[int, List[int]],
                nz_threshold: int = 1400) -> Dict[int, List[int]]:
    num_correct = 0
    answers = {}

    # each question has 5 possible answers, to loop over the question in batches of 5
    for (q, i) in enumerate(np.arange(0, len(bubble_contours), 5)):
        # sorting the contours for the current question from left to right, then initializing the index of the
        # bubbled answer
        cnts = contours.sort_contours(bubble_contours[i:i + 5])[0]
        bubbled = None

        # loop over the sorted contours
        for (j, c) in enumerate(cnts):
            # construct a mask that reveals only the current
            # "bubble" for the question
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            # apply the mask to the thresholded image, then
            # count the number of non-zero pixels in the
            # bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)

            # if the current total has a larger number of total
            # non-zero pixels, then we are examining the currently
            # bubbled-in answer

            if total > nz_threshold:
                if bubbled is None:
                    bubbled = [(total, j)]
                else:
                    bubbled.append((total, j))

        print(f"Bubbled: {bubbled}")

        # initialize the index of the question
        k = questions[q]
        current_correct = 0

        for ans in k:
            if ans >= len(cnts):
                continue
            if ans in [b[1] for b in bubbled]:
                color = (0, 255, 0)
                current_correct += 1
            else:
                color = (0, 0, 255)
            cv2.drawContours(paper, [cnts[ans]], -1, color, 3)

        if current_correct == len(k):
            num_correct += 1

        # update the list of correct answers
        for b in bubbled:
            if answers.get(q) is None:
                answers[q] = [b[1]]
            else:
                answers[q].append(b[1])

    # grab the test taker
    score = (num_correct / len(questions)) * 100
    cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imshow("Exam", paper)
    cv2.waitKey(0)

    return answers


QUESTIONS = {0: [1, 2, 3, 4], 1: [4], 2: [0], 3: [3], 4: [1]}

answers = parser("test.png")
from typing import Dict, List

import cv2
import imutils
import numpy as np
from cv2.typing import MatLike
from imutils import contours

QUESTIONS = [[1, 2, 3, 4], [4], [0], [3], [1], [1], [1], [1], [1], [1]]


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

        # print(f"Width: {w}, Height: {h}, Aspect Ratio: {ar}")
        # in order to label the contour as a question, region should be sufficiently wide, sufficiently tall,
        # and have an aspect ratio approximately equal to 1
        if w >= 20 and h >= 20 and 0.9 <= ar <= 1.4:
            question_cnts.append(c)

    # sorting the question contours top-to-bottom, then initializing the total number of correct answers
    question_cnts = contours.sort_contours(question_cnts, method="top-to-bottom")[0]

    return question_cnts


def stabilize_threshold_level(bubble_contours: List[MatLike], thresh: MatLike) -> int:
    # initialize a list of bubble regions
    bubble_regions = []

    # loop over the question regions
    for c in bubble_contours:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # initialize a mask that will be used to crop the region of interest
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # apply the mask to the thresholded image, then append the bounding box region to the list of bubble regions
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        bubble_regions.append((total, (x, y, w, h)))

    # sort the bubble regions by the total number of non-zero pixels in the bubble area
    bubble_regions = sorted(bubble_regions, key=lambda x: x[0], reverse=True)

    for region in bubble_regions:
        print(f"Total: {region[0]}")

    return int(bubble_regions[0][0]*0.5) if int(bubble_regions[0][0]*0.5) > 700 else 700


def solve_quiz(image: MatLike, ans: List[List[int]]):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                           )[1]

    bubble_contours = [
        c for c in get_bubble_contours(thresh)
    ]

    thresh_level = stabilize_threshold_level(bubble_contours, thresh)

    print(f"Threshold Level: {thresh_level}")

    return solve(thresh, bubble_contours, ans, nz_threshold=thresh_level)


def solve(thresh: MatLike, bubble_contours: List[MatLike], questions: List[List[int]],
          nz_threshold: int = 1000) -> tuple[Dict[int, List[int]], float]:
    num_correct = 0
    answers = {}

    # each question has 5 possible answers, to loop over the question in batches of 5
    for (q, i) in enumerate(np.arange(0, len(bubble_contours), 5)):
        if q >= len(questions):
            break
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

            # print(f"Total: {total}")

            if total > nz_threshold:
                if bubbled is None:
                    bubbled = [(total, j)]
                else:
                    bubbled.append((total, j))

        # print(f"Bubbled: {bubbled}")

        if bubbled is None:
            continue

        # initialize the index of the question
        k = questions[q]
        current_correct = 0

        for ans in k:
            if ans >= len(cnts):
                continue
            if ans in [b[1] for b in bubbled]:
                # color = (0, 255, 0)
                current_correct += 1
            # else:
            #     color = (0, 0, 255)
            # cv2.drawContours(image, [cnts[ans]], -1, color, 3)

        if current_correct == len(k) and current_correct == len(bubbled):
            num_correct += 1

        # update the list of correct answers
        for b in bubbled:
            if answers.get(q) is None:
                answers[q] = [b[1]]
            else:
                answers[q].append(b[1])

    # grab the test taker
    sc = (num_correct / len(questions)) * 100
    # cv2.putText(image, "{:.2f}%".format(sc), (10, 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    # cv2.imshow("Exam", image)
    # cv2.waitKey(0)

    print(f"Score: {sc}")
    print(f"Answers: {answers}")

    return answers, sc


if __name__ == '__main__':
    answers, score = solve_quiz(cv2.imread("../cmpl-sheet.png"), QUESTIONS)
    print(answers, score)

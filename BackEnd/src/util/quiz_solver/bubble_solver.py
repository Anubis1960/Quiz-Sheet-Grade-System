from typing import Dict, List

import cv2
import imutils
import numpy as np
from cv2.typing import MatLike
from imutils import contours

# A 2D list defining the answers for each question. Each question can have multiple correct answers.
QUESTIONS = [[1, 2, 3, 4], [4], [0], [3], [1], [1], [1], [1], [1], [1]]


def retry_bubble_contours(thresh: MatLike) -> MatLike:
    """
    Attempts to refine the bubble contours by preprocessing the thresholded image and applying morphological
    operations to close gaps. If the initial contour extraction fails, this method tries again to improve the detection.

    Args:
        thresh: The thresholded binary image.

    Returns:
        The filtered list of contours that correspond to the bubbles.
    """
    # Preprocess the image to improve contour detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours in the processed image
    cnts = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return filter_bubble_contours(cnts)


def filter_bubble_contours(cnts: List[MatLike]) -> List[MatLike]:
    """
    Filters the contours to keep only those that correspond to bubbles, based on their size and aspect ratio.

    Args:
        cnts: The list of contours extracted from the image.

    Returns:
        A filtered list of contours that are likely to be bubbles.
    """
    question_cnts = []
    for c in cnts:
        # Compute the bounding box and aspect ratio of each contour
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        # Select contours that are sufficiently wide, tall, and have an aspect ratio near 1
        if w >= 30 and h >= 30 and 0.85 <= ar <= 1.3:
            question_cnts.append(c)

    # Sort contours top to bottom
    question_cnts = contours.sort_contours(question_cnts, method="top-to-bottom")[0]

    return question_cnts


def get_bubble_contours(thresh: MatLike) -> MatLike:
    """
    Extracts the bubble contours from the thresholded image. This function will retry if it doesn't find exactly
    50 bubbles (one for each possible question).

    Args:
        thresh: The thresholded binary image.

    Returns:
        A list of bubble contours.
    """
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    bubble_contours = filter_bubble_contours(cnts)

    # Retry if the number of bubble contours isn't as expected
    if len(bubble_contours) != 50:
        bubble_contours = retry_bubble_contours(thresh)

    return bubble_contours


def stabilize_threshold_level(bubble_contours: List[MatLike], thresh: MatLike) -> int:
    """
    Adjusts the threshold level based on the bubble contours by calculating the number of non-zero pixels in the
    detected bubble regions. This helps refine the detection of the bubbles.

    Args:
        bubble_contours: The contours of the detected bubbles.
        thresh: The thresholded binary image.

    Returns:
        An adjusted threshold value.
    """
    bubble_regions = []

    # Loop over the contours and create a mask for each
    for c in bubble_contours:
        (x, y, w, h) = cv2.boundingRect(c)

        # Create a mask for the current bubble contour
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # Apply the mask and count the number of non-zero pixels
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        bubble_regions.append((total, (x, y, w, h)))

    # Sort bubble regions by the total number of non-zero pixels
    bubble_regions = sorted(bubble_regions, key=lambda ics: ics[0], reverse=True)

    # Return an adjusted threshold based on the highest count
    return int(bubble_regions[0][0] * 0.5) if int(bubble_regions[0][0] * 0.5) > 700 else 700


def unsharp_mask(image: MatLike, ketnel=(5, 5), sigma=1.0, amount=1.0, threshold=0) -> MatLike:
    """
    Applies an unsharp mask to sharpen the image.

    Args:
        image: The input image.
        ketnel: The kernel size for the Gaussian blur.
        sigma: The standard deviation for the Gaussian blur.
        amount: The amount to enhance the sharpness.
        threshold: The threshold to determine where sharpening is applied.

    Returns:
        The sharpened image.
    """
    blurred = cv2.GaussianBlur(image, ketnel, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)

    if threshold > 0:
        low_contrast_mask = np.abs(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)

    return sharpened


def solve_quiz(image: MatLike, ans: List[List[int]]):
    """
    Solves a quiz by detecting and analyzing the bubbled answers in the image.

    Args:
        image: The input image of the quiz sheet.
        ans: The list of correct answers for each question.

    Returns:
        A tuple with the answers and the score.
    """
    image = unsharp_mask(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Detect bubble contours and adjust threshold level
    bubble_contours = [c for c in retry_bubble_contours(thresh)]
    thresh_level = stabilize_threshold_level(bubble_contours, thresh)

    # Solve the quiz by comparing detected bubbles with the correct answers
    return solve(thresh, bubble_contours, ans, nz_threshold=thresh_level)


def solve(thresh: MatLike, bubble_contours: List[MatLike], questions: List[List[int]], nz_threshold: int = 1000) -> (
        tuple)[Dict[int, List[int]], float]:
    """
    Solves the quiz by iterating through the bubbles and comparing with the correct answers.

    Args:
        thresh: The thresholded binary image.
        bubble_contours: The contours of the bubbles.
        questions: The list of correct answers for each question.
        nz_threshold: The minimum number of non-zero pixels required to consider an answer as bubbled.

    Returns:
        A tuple containing the detected answers and the score.
    """
    num_correct = 0
    a = {}

    # Loop over the questions and check each set of 5 possible answers
    for (q, i) in enumerate(np.arange(0, len(bubble_contours), 5)):
        if q >= len(questions):
            break
        cnts = contours.sort_contours(bubble_contours[i:i + 5])[0]
        bubbled = None

        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)

            if total > nz_threshold:
                if bubbled is None:
                    bubbled = [(total, j)]
                else:
                    bubbled.append((total, j))

        if bubbled is None:
            continue

        k = questions[q]
        current_correct = 0

        for ans in k:
            if ans >= len(cnts):
                continue
            if ans in [b[1] for b in bubbled]:
                current_correct += 1

        if current_correct == len(k) and current_correct == len(bubbled):
            num_correct += 1

        for b in bubbled:
            if a.get(q) is None:
                a[q] = [b[1]]
            else:
                a[q].append(b[1])

    sc = (num_correct / len(questions)) * 100
    return a, num_correct


if __name__ == '__main__':
    answers, score = solve_quiz(cv2.imread("../cmpl-sheet.png"), QUESTIONS)
    print(answers, score)

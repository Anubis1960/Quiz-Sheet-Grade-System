import os
import cv2
import imutils
import numpy as np
from cv2.typing import MatLike
from imutils.perspective import four_point_transform
from tensorflow.keras import models


# Load the model
def load_model(name: str) -> models.Model:
    model = models.load_model(name)
    return model


def get_box_contours(image: MatLike) -> MatLike:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    contour = contours[0]
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:  # Ensure it's a quadrilateral
        # Step 2: Define the source points (contour corners)
        pts_src = np.float32([point[0] for point in approx])  # Extract the 4 points

        # Step 3: Define the destination points (rectangle)
        # Sort the points to ensure consistent mapping
        pts_src = sorted(pts_src, key=lambda x: (x[1], x[0]))  # Sort by y, then x
        top_left, top_right = sorted(pts_src[:2], key=lambda x: x[0])
        bottom_left, bottom_right = sorted(pts_src[2:], key=lambda x: x[0])
        pts_src = np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.float32)

        width = int(max(
            np.linalg.norm(top_right - top_left),
            np.linalg.norm(bottom_right - bottom_left)
        ))
        height = int(max(
            np.linalg.norm(top_left - bottom_left),
            np.linalg.norm(top_right - bottom_right)
        ))
        pts_dst = np.float32([
            [0, 0],
            [width - 1, 0],
            [0, height - 1],
            [width - 1, height - 1]
        ])

        # Step 4: Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

        # Step 5: Apply the warp
        warped_image = cv2.warpPerspective(image, matrix, (width-2, height-2))

        # Display or save results
        # cv2.imshow("Warped Image", warped_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return warped_image
    else:
        print("Contour cannot be approximated to a quadrilateral.")
        return image


def read_id(image: MatLike) -> str:
    model = load_model(os.path.dirname(__file__) + "/text-recognizer.keras")

    image = get_box_contours(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Preprocess the image
    _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    assert thresh.dtype == "uint8", "Input to findContours must be of type uint8"

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    if len(dilated.shape) > 2:
        dilated = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    margin = 2
    min_width, min_height = 5, 5
    max_width, max_height = 60, 60
    char_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        ar = w / h
        print(f"Width {w}; Height {h}; Aspect Ratio {ar} X {x} Y {y}")
        if min_width <= w <= max_width and min_height <= h <= max_height and 0.5 <= ar <= 2.0:
            x = max(0, x - margin)
            y = max(0, y - margin)
            w += 2 * margin
            h += 2 * margin

            char_boxes.append((x, y, w, h))

    id_prediction = ""

    for box in sorted(char_boxes, key=lambda x: x[0]):
        x, y, w, h = box
        char_image = dilated[y:y + h, x:x + w]
        char_image = cv2.resize(char_image, (20, 20))
        char_image = cv2.copyMakeBorder(char_image, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)
        char_image = cv2.resize(char_image, (28, 28))

        char_image = char_image.reshape(1, 28, 28, 1)
        char_image = char_image / 255.0

        prediction = model.predict(char_image)
        id_prediction += chr(prediction.argmax() + 55) if prediction.argmax() >= 10 else str(prediction.argmax())

    print(f"Predicted ID: {id_prediction}")

    return id_prediction

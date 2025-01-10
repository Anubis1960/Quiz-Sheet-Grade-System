import os
import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform
from tensorflow.keras import models


# Load the model
def load_model(name: str) -> models.Model:
    model = models.load_model(name)
    return model


def get_box_contours(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cnts = cv2.findContours(
        image.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)
    doc_cnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            print(len(approx))
            if len(approx) == 4:
                doc_cnt = approx
    else:
        print("No contours found")
        return None

    if doc_cnt is None:
        print("No document found")
        return None

    return doc_cnt


def read_id(image) -> str:
    model = load_model(os.path.dirname(__file__) + "/text-recognizer.keras")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cv2.imshow("Edge", edged)
    cv2.waitKey(0)

    doc_cnts = get_box_contours(edged)

    if doc_cnts is None:
        paper = image
    else:
        paper = four_point_transform(image, doc_cnts.reshape(4, 2))

    # Preprocess the image
    _, thresh = cv2.threshold(paper, 128, 255, cv2.THRESH_BINARY_INV)
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
    min_width, min_height = 10, 10
    char_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w >= min_width and h >= min_height:
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

        cv2.imshow("Char", char_image)
        cv2.waitKey(0)

        char_image = char_image.reshape(1, 28, 28, 1)
        char_image = char_image / 255.0

        prediction = model.predict(char_image)
        id_prediction += chr(prediction.argmax() + 55) if prediction.argmax() >= 10 else str(prediction.argmax())

    print(f"Predicted ID: {id_prediction}")

    return id_prediction


if __name__ == "__main__":
    img = cv2.imread("hello.png")
    print(img.shape)
    txt = read_id(img)
    print(txt)

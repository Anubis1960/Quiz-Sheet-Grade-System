import os
import cv2
import numpy as np
from tensorflow.keras import models


# Load the model
def load_model(name: str) -> models.Model:
    model = models.load_model(name)
    return model


def non_max_suppression_fast(boxes: np.ndarray, overlap_thresh: float = 0.3) -> np.ndarray:
    if len(boxes) == 0:
        return np.ndarray(0)

    boxes = np.array(boxes)
    pick = []

    # Coordinates of bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 0] + boxes[:, 2]
    y2 = boxes[:, 1] + boxes[:, 3]

    # Compute areas and sort by bottom-right y-coordinate
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # Find intersection
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Compute width and height of intersection
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute overlap ratio
        overlap = (w * h) / area[idxs[:last]]

        # Remove indices where overlap > threshold
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))

    return boxes[pick].astype("int")


def read_id(image) -> str:
    model = load_model(os.path.dirname(__file__) + "/text-recognizer.keras")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocess the image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    assert thresh.dtype == "uint8", "Input to findContours must be of type uint8"

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

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
            char_image = dilated[y:y + h, x:x + w]

            # Resize with padding
            char_image = cv2.resize(char_image, (20, 20))
            char_image = cv2.copyMakeBorder(char_image, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)
            char_image = cv2.resize(char_image, (28, 28))

            char_boxes.append((x, y, w, h))

            # Visualize for debugging
            cv2.imshow("Character", char_image)
            cv2.waitKey(0)

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


if __name__ == "__main__":
    img = cv2.imread("hello.png")
    print(img.shape)
    txt = read_id(img)
    print(txt)

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


def process_image(img) -> tuple:
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to the gray image to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection to find the edges in the image
    edged = cv2.Canny(blurred, 30, 150)

    return gray, blurred, edged


def read_id(img) -> str:
    model = load_model(os.path.dirname(__file__) + "/text-recognizer.keras")

    gray, blurred, edged = process_image(img)

    # Find contours and hierarchy
    cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = []
    for i, h in enumerate(hierarchy[0]):
        if h[3] == -1:  # Include only outermost contours
            valid_contours.append(cnts[i])

    # Extract bounding boxes and apply NMS
    boxes = [cv2.boundingRect(c) for c in valid_contours]

    chrs = []
    for box in boxes:
        (x, y, w, h) = box
        ar = w / float(h)
        # print(f"Width: {w}, Height: {h}, Aspect Ratio: {ar}")
        if w >= 5 and h >= 5 and 0.38 <= ar <= 2.0:
            # print(f"Width: {w}, Height: {h}, Aspect Ratio: {ar}")
            roi = gray[y:y + h, x:x + w]
            thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            (tH, tW) = thresh.shape
            if tW > tH:
                thresh = cv2.resize(thresh, (28, int(28 * tH / tW)))
            else:
                thresh = cv2.resize(thresh, (int(28 * tW / tH), 28))

            # Pad and reshape to (28, 28)
            padded = cv2.copyMakeBorder(thresh, top=8, bottom=8, left=8, right=8, borderType=cv2.BORDER_CONSTANT,
                                        value=(0, 0, 0))
            padded = cv2.resize(padded, (28, 28))

            # cv2.imshow("Padded Image", padded)
            # cv2.waitKey(0)

            padded = padded.astype("float32") / 255.0
            chrs.append((padded, box))

    if not chrs:
        print("No characters detected.")
        return ""

    chrs_data = np.array([c[0] for c in chrs], dtype="float32")
    predictions = model.predict(chrs_data)
    text = ""
    for i, (padded, (x, y, w, h)) in sorted(enumerate(chrs), key=lambda _: _[1][1][0]):
        prediction = np.argmax(predictions[i])
        label = chr(prediction + 55) if prediction >= 10 else str(prediction)

        text += label

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Processed Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return text


if __name__ == "__main__":
    img = cv2.imread("hello.png")
    print(img.shape)
    txt = read_id(img)
    print(txt)

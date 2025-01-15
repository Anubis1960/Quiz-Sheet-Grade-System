import os
import cv2
import numpy as np
from cv2.typing import MatLike
from tensorflow.keras import models


def load_model(name: str) -> models.Model:
    """
    Load a pre-trained Keras model from a file.

    Args:
        name (str): The file path to the model file.

    Returns:
        models.Model: The loaded Keras model.
    """
    model = models.load_model(name)
    return model


def get_box_contours(image: MatLike) -> MatLike:
    """
    Extracts the largest contour from an image and applies a perspective transformation to
    obtain a rectangular region of interest (ROI).

    Args:
        image (MatLike): The input image on which the contour extraction and transformation will be performed.

    Returns:
        MatLike: The warped image (rectangular region of interest), or the original image if no quadrilateral is found.
    """
    # Convert the image to grayscale for easier processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to highlight the contours
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)

    # Find external contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area in descending order to find the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Approximate the largest contour to a polygon
    contour = contours[0]
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # If the contour is a quadrilateral, proceed to extract the perspective transform
    if len(approx) == 4:  # Ensure it's a quadrilateral
        # Define the source points as the corners of the quadrilateral
        pts_src = np.float32([point[0] for point in approx])

        # Sort the points to ensure consistent mapping to destination points
        pts_src = sorted(pts_src, key=lambda x: (x[1], x[0]))  # Sort by y, then x
        top_left, top_right = sorted(pts_src[:2], key=lambda x: x[0])
        bottom_left, bottom_right = sorted(pts_src[2:], key=lambda x: x[0])
        pts_src = np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.float32)

        # Compute the dimensions for the destination image (rectangle)
        width = int(max(
            np.linalg.norm(top_right - top_left),
            np.linalg.norm(bottom_right - bottom_left)
        ))
        height = int(max(
            np.linalg.norm(top_left - bottom_left),
            np.linalg.norm(top_right - bottom_right)
        ))

        # Define the destination points (standard rectangular coordinates)
        pts_dst = np.float32([
            [0, 0],
            [width - 1, 0],
            [0, height - 1],
            [width - 1, height - 1]
        ])

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

        # Apply the perspective warp to the image
        warped_image = cv2.warpPerspective(image, matrix, (width - 2, height - 2))

        return warped_image
    else:
        # If no quadrilateral is found, return the original image
        return image


def read_id(image: MatLike) -> str:
    """
    Extracts an alphanumeric ID from an image containing a text-based ID. This function uses
    contour detection and a pre-trained machine learning model to identify each character in
    the ID and return the corresponding text string.

    Args:
        image (MatLike): The input image containing the ID to be read.

    Returns:
        str: The predicted alphanumeric ID as a string.
    """
    # Load the pre-trained text recognition model
    model = load_model(os.path.dirname(__file__) + "/text-recognizer.keras")

    # Extract the region of interest (ROI) from the image using contours
    image = get_box_contours(image)

    # Crop the image to exclude border artifacts
    image = image[2: -2, 2: -2]

    # Convert the image to grayscale for easier character detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocess the grayscale image using binary thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Apply morphological operations to close small gaps in the characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    assert thresh.dtype == "uint8", "Input to findContours must be of type uint8"

    # Dilate the thresholded image to make characters more distinct
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # If the image has more than one channel, convert it to grayscale
    if len(dilated.shape) > 2:
        dilated = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)

    # Find contours in the dilated image to detect characters
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define margin and size constraints for character bounding boxes
    margin = 2
    min_width, min_height = 5, 5
    max_width, max_height = 60, 60
    char_boxes = []

    # Process each contour and determine valid character bounding boxes
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        ar = w / h  # Aspect ratio of the bounding box
        if min_width <= w <= max_width and min_height <= h <= max_height and 0.5 <= ar <= 2.0:
            # Apply margin to bounding box to ensure full character inclusion
            x = max(0, x - margin)
            y = max(0, y - margin)
            w += 2 * margin
            h += 2 * margin

            # Append valid bounding box to the list
            char_boxes.append((x, y, w, h))

    # Initialize the predicted ID string
    id_prediction = ""

    # Sort character bounding boxes from left to right and extract each character
    for box in sorted(char_boxes, key=lambda x: x[0]):
        x, y, w, h = box
        char_image = dilated[y:y + h, x:x + w]

        # Resize character image to a fixed size
        char_image = cv2.resize(char_image, (20, 20))

        # Add padding to the character image for model compatibility
        char_image = cv2.copyMakeBorder(char_image, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)

        # Resize to match input dimensions for the model (28x28)
        char_image = cv2.resize(char_image, (28, 28))

        # Reshape the character image for prediction and normalize the pixel values
        char_image = char_image.reshape(1, 28, 28, 1)
        char_image = char_image / 255.0

        # Predict the character using the loaded model
        prediction = model.predict(char_image)

        # Convert prediction to a character and append to the result string
        id_prediction += chr(prediction.argmax() + 55) if prediction.argmax() >= 10 else str(prediction.argmax())

    # Return the final predicted ID as a string
    return id_prediction

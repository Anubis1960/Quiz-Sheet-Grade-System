Module src.util.text_recognition.process_text
=============================================

Functions
---------

`get_box_contours(image: cv2.Mat | numpy.ndarray) ‑> cv2.Mat | numpy.ndarray`
:   Extracts the largest contour from an image and applies a perspective transformation to
    obtain a rectangular region of interest (ROI).
    
    Args:
        image (MatLike): The input image on which the contour extraction and transformation will be performed.
    
    Returns:
        MatLike: The warped image (rectangular region of interest), or the original image if no quadrilateral is found.

`load_model(name: str) ‑> keras.src.models.model.Model`
:   Load a pre-trained Keras model from a file.
    
    Args:
        name (str): The file path to the model file.
    
    Returns:
        models.Model: The loaded Keras model.

`read_id(image: cv2.Mat | numpy.ndarray) ‑> str`
:   Extracts an alphanumeric ID from an image containing a text-based ID. This function uses
    contour detection and a pre-trained machine learning model to identify each character in
    the ID and return the corresponding text string.
    
    Args:
        image (MatLike): The input image containing the ID to be read.
    
    Returns:
        str: The predicted alphanumeric ID as a string.
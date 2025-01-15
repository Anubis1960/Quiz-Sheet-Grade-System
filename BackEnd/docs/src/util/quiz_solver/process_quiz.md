Module src.util.quiz_solver.process_quiz
========================================

Functions
---------

`crop_bubble_sheet(paper: cv2.Mat | numpy.ndarray) ‑> list[numpy.ndarray]`
:   Crops the bubble sheet section from the document based on predefined coordinates.
    
    Args:
        paper (MatLike): The document image from which to extract the bubble sheet.
    
    Returns:
        list[ndarray]: A list of cropped bubble sheets.

`crop_id_box(paper: cv2.Mat | numpy.ndarray) ‑> cv2.Mat | numpy.ndarray`
:   Crops the student ID box section from the document.
    
    Args:
        paper (MatLike): The document image from which to extract the student ID box.
    
    Returns:
        MatLike: The cropped student ID box.

`get_document_contours(image: cv2.Mat | numpy.ndarray) ‑> None | numpy.ndarray`
:   Attempts to extract the document from an image by detecting its contours.
    This function is used to detect the document region, resize it, and apply edge detection.
    
    Args:
        image (MatLike): The input image to process.
    
    Returns:
        None | ndarray: The extracted document region, or None if extraction fails.

`parser(image: cv2.Mat | numpy.ndarray) ‑> tuple[numpy.ndarray | None, str, str]`
:   Processes an image, scans for a QR code, detects the document, extracts the student ID,
    and returns the processed data including bubble sheet and quiz ID.
    
    Args:
        image (MatLike): The input image to process.
    
    Returns:
        tuple: A tuple containing the bubble sheet (ndarray), student ID (str), and quiz ID (str).

`rescale_image(image: cv2.Mat | numpy.ndarray, width: int = 595, height: int = 842) ‑> cv2.Mat | numpy.ndarray`
:   Rescales the image to a specified width and height.
    
    Args:
        image (MatLike): The input image to be rescaled.
        width (int): The target width.
        height (int): The target height.
    
    Returns:
        MatLike: The rescaled image.

`retry_on_failure(image: cv2.Mat | numpy.ndarray) ‑> None | numpy.ndarray`
:   Attempts to process an image and extract the document region even if initial processing fails.
    It applies several image processing techniques to find and extract the document.
    
    Args:
        image (MatLike): The input image to process.
    
    Returns:
        ndarray | None: The extracted document region, or None if extraction fails.

`scan_qr_code(image: cv2.Mat | numpy.ndarray) ‑> str`
:   Scans a QR code from the given image using the QReader library.
    
    Args:
        image (MatLike): The image to scan for a QR code.
    
    Returns:
        str: The QR code data, if found, otherwise an empty string.
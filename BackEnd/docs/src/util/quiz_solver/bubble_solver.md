Module src.util.quiz_solver.bubble_solver
=========================================

Functions
---------

`filter_bubble_contours(cnts: List[cv2.Mat | numpy.ndarray]) ‑> List[cv2.Mat | numpy.ndarray]`
:   Filters the contours to keep only those that correspond to bubbles, based on their size and aspect ratio.
    
    Args:
        cnts: The list of contours extracted from the image.
    
    Returns:
        A filtered list of contours that are likely to be bubbles.

`get_bubble_contours(thresh: cv2.Mat | numpy.ndarray) ‑> cv2.Mat | numpy.ndarray`
:   Extracts the bubble contours from the thresholded image. This function will retry if it doesn't find exactly
    50 bubbles (one for each possible question).
    
    Args:
        thresh: The thresholded binary image.
    
    Returns:
        A list of bubble contours.

`retry_bubble_contours(thresh: cv2.Mat | numpy.ndarray) ‑> cv2.Mat | numpy.ndarray`
:   Attempts to refine the bubble contours by preprocessing the thresholded image and applying morphological
    operations to close gaps. If the initial contour extraction fails, this method tries again to improve the detection.
    
    Args:
        thresh: The thresholded binary image.
    
    Returns:
        The filtered list of contours that correspond to the bubbles.

`solve(thresh: cv2.Mat | numpy.ndarray, bubble_contours: List[cv2.Mat | numpy.ndarray], questions: List[List[int]], nz_threshold: int = 1000) ‑> tuple[typing.Dict[int, typing.List[int]], float]`
:   Solves the quiz by iterating through the bubbles and comparing with the correct answers.
    
    Args:
        thresh: The thresholded binary image.
        bubble_contours: The contours of the bubbles.
        questions: The list of correct answers for each question.
        nz_threshold: The minimum number of non-zero pixels required to consider an answer as bubbled.
    
    Returns:
        A tuple containing the detected answers and the score.

`solve_quiz(image: cv2.Mat | numpy.ndarray, ans: List[List[int]])`
:   Solves a quiz by detecting and analyzing the bubbled answers in the image.
    
    Args:
        image: The input image of the quiz sheet.
        ans: The list of correct answers for each question.
    
    Returns:
        A tuple with the answers and the score.

`stabilize_threshold_level(bubble_contours: List[cv2.Mat | numpy.ndarray], thresh: cv2.Mat | numpy.ndarray) ‑> int`
:   Adjusts the threshold level based on the bubble contours by calculating the number of non-zero pixels in the
    detected bubble regions. This helps refine the detection of the bubbles.
    
    Args:
        bubble_contours: The contours of the detected bubbles.
        thresh: The thresholded binary image.
    
    Returns:
        An adjusted threshold value.

`unsharp_mask(image: cv2.Mat | numpy.ndarray, ketnel=(5, 5), sigma=1.0, amount=1.0, threshold=0) ‑> cv2.Mat | numpy.ndarray`
:   Applies an unsharp mask to sharpen the image.
    
    Args:
        image: The input image.
        ketnel: The kernel size for the Gaussian blur.
        sigma: The standard deviation for the Gaussian blur.
        amount: The amount to enhance the sharpness.
        threshold: The threshold to determine where sharpening is applied.
    
    Returns:
        The sharpened image.
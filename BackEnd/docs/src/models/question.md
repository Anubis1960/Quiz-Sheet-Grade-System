Module src.models.question
==========================

Classes
-------

`Question(text: str, options: list[str] = None, correct_answers: list[int] = None)`
:   Represents a multiple-choice question with text, options, and correct answers.
    Provides methods to convert the question object to and from a dictionary format.
    
    Attributes:
        text (str): The question text.
        options (list[str]): A list of possible answer options for the question.
        correct_answers (list[int]): A list of indices representing the correct answer options.
    
    Initializes a new Question object with the provided text, options, and correct answers.
    
    Args:
        text (str): The question text.
        options (list[str], optional): A list of possible answer options for the question. Defaults to an empty list.
        correct_answers (list[int], optional): A list of indices of the correct options. Defaults to an empty list.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.question.Question`
    :   Creates a Question object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the question's attributes. Expected keys:
                         'text', 'options', and 'correct_answers'.
        
        Returns:
            Question: A new Question object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the Question object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the question's attributes ('text', 'options', 'correct_answers').
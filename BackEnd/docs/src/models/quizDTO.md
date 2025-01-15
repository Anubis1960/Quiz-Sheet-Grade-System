Module src.models.quizDTO
=========================

Classes
-------

`QuizDTO(quiz_id: str, title: str, description: str, questions: list[dict])`
:   Data Transfer Object (DTO) for the Quiz entity.
    This class represents a simplified version of the Quiz model used for data transfer.
    
    Attributes:
        id (str): The unique identifier for the quiz.
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        questions (list[dict]): A list of questions in the quiz, where each question is represented as a dictionary.
    
    Initializes a new QuizDTO object with the provided quiz_id, title, description, and questions.
    
    Args:
        quiz_id (str): The unique identifier for the quiz.
        title (str): The title of the quiz.
        description (str): The description of the quiz.
        questions (list[dict]): A list of questions represented as dictionaries.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.quizDTO.QuizDTO`
    :   Creates a QuizDTO object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the quiz's attributes. Expected keys:
                         'id', 'title', 'description', and 'questions'.
        
        Returns:
            QuizDTO: A new QuizDTO object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the QuizDTO object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the QuizDTO's attributes ('id', 'title', 'description', 'questions').
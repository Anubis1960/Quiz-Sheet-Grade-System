Module src.models.quiz
======================

Classes
-------

`Quiz(title: str, description: str, teacher: str, questions: list[src.models.question.Question] = None)`
:   Represents a quiz with a title, description, teacher, and a list of questions.
    Provides methods to convert the quiz object to and from a dictionary format.
    
    Attributes:
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        teacher (str): The name of the teacher who created the quiz.
        questions (list[Question]): A list of `Question` objects associated with the quiz.
    
    Initializes a new Quiz object with the provided title, description, teacher, and questions.
    
    Args:
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        teacher (str): The name of the teacher.
        questions (list[Question], optional): A list of `Question` objects for the quiz. Defaults to an empty list.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.quiz.Quiz`
    :   Creates a Quiz object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the quiz's attributes. Expected keys:
                         'title', 'description', 'teacher', and 'questions'.
        
        Returns:
            Quiz: A new Quiz object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the Quiz object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the quiz's attributes ('title', 'description', 'teacher', 'questions').
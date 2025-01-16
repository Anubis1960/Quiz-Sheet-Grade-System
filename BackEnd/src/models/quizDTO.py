class QuizDTO:
    """
    Data Transfer Object (DTO) for the Quiz entity.
    This class represents a simplified version of the Quiz model used for data transfer.

    Attributes:
        id (str): The unique identifier for the quiz.
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        questions (list[dict]): A list of questions in the quiz, where each question is represented as a dictionary.
    """

    def __init__(self, quiz_id: str, title: str, description: str, questions: list[dict]):
        """
        Initializes a new QuizDTO object with the provided quiz_id, title, description, and questions.

        Args:
            quiz_id (str): The unique identifier for the quiz.
            title (str): The title of the quiz.
            description (str): The description of the quiz.
            questions (list[dict]): A list of questions represented as dictionaries.
        """
        self.id = quiz_id
        self.title = title
        self.description = description
        self.questions = questions

    def to_dict(self) -> dict:
        """
        Converts the QuizDTO object to a dictionary representation.

        Returns:
            dict: A dictionary containing the QuizDTO's attributes ('id', 'title', 'description', 'questions').
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "questions": [question for question in self.questions],  # Copying the question list
        }

    @staticmethod
    def from_dict(data: dict) -> "QuizDTO":
        """
        Creates a QuizDTO object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the quiz's attributes. Expected keys:
                         'id', 'title', 'description', and 'questions'.

        Returns:
            QuizDTO: A new QuizDTO object initialized with data from the dictionary.
        """
        return QuizDTO(
            quiz_id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            questions=data.get("questions", []),
        )
from src.models.question import Question

class Quiz:
    """
    Represents a quiz with a title, description, teacher, and a list of questions.
    Provides methods to convert the quiz object to and from a dictionary format.

    Attributes:
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        teacher (str): The name of the teacher who created the quiz.
        questions (list[Question]): A list of `Question` objects associated with the quiz.
    """

    def __init__(self, title: str, description: str, teacher: str, questions: list[Question] = None):
        """
        Initializes a new Quiz object with the provided title, description, teacher, and questions.

        Args:
            title (str): The title of the quiz.
            description (str): A description of the quiz.
            teacher (str): The name of the teacher.
            questions (list[Question], optional): A list of `Question` objects for the quiz. Defaults to an empty list.
        """
        self.title = title
        self.description = description
        self.teacher = teacher
        self.questions = questions or []

    def to_dict(self) -> dict:
        """
        Converts the Quiz object to a dictionary representation.

        Returns:
            dict: A dictionary containing the quiz's attributes ('title', 'description', 'teacher', 'questions').
        """
        return {
            "title": self.title,
            "description": self.description,
            "teacher": self.teacher,
            "questions": [question.to_dict() for question in self.questions],
        }

    @staticmethod
    def from_dict(data: dict) -> "Quiz":
        """
        Creates a Quiz object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the quiz's attributes. Expected keys:
                         'title', 'description', 'teacher', and 'questions'.

        Returns:
            Quiz: A new Quiz object initialized with data from the dictionary.
        """
        return Quiz(
            title=data.get("title"),
            description=data.get("description"),
            teacher=data.get("teacher"),
            questions=[Question.from_dict(q) for q in data.get("questions", [])]
        )
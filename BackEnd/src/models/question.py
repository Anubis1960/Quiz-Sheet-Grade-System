class Question:
    """
    Represents a multiple-choice question with text, options, and correct answers.
    Provides methods to convert the question object to and from a dictionary format.

    Attributes:
        text (str): The question text.
        options (list[str]): A list of possible answer options for the question.
        correct_answers (list[int]): A list of indices representing the correct answer options.
    """

    def __init__(self, text: str, options: list[str] = None, correct_answers: list[int] = None):
        """
        Initializes a new Question object with the provided text, options, and correct answers.

        Args:
            text (str): The question text.
            options (list[str], optional): A list of possible answer options for the question. Defaults to an empty list.
            correct_answers (list[int], optional): A list of indices of the correct options. Defaults to an empty list.
        """
        self.text = text
        self.options = options or []
        self.correct_answers = correct_answers or []

    def to_dict(self) -> dict:
        """
        Converts the Question object to a dictionary representation.

        Returns:
            dict: A dictionary containing the question's attributes ('text', 'options', 'correct_answers').
        """
        return {
            "text": self.text,
            "options": self.options,
            "correct_answers": self.correct_answers
        }

    @staticmethod
    def from_dict(data: dict) -> "Question":
        """
        Creates a Question object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the question's attributes. Expected keys:
                         'text', 'options', and 'correct_answers'.

        Returns:
            Question: A new Question object initialized with data from the dictionary.
        """
        return Question(
            text=data.get("text"),
            options=data.get("options", []),
            correct_answers=data.get("correct_answers", [])
        )
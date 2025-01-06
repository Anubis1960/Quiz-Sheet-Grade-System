class Question:
    def __init__(self, text: str, options: list[str] = None, correct_answers: list[int] = None):
        self.text = text
        self.options = options or []
        self.correct_answers = correct_answers or []

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "options": self.options,
            "correct_answers": self.correct_answers
        }

    @staticmethod
    def from_dict(data: dict) -> "Question":
        return Question(
            text=data.get("text"),
            options=data.get("options", []),
            correct_answers=data.get("correct_answers", [])
        )

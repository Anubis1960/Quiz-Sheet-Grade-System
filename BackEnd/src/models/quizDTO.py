class QuizDTO:
    def __init__(self, quiz_id: str, title: str, description: str, questions: list[dict]):
        self.id = quiz_id
        self.title = title
        self.description = description
        self.questions = questions

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "questions": [question for question in self.questions],
        }

    @staticmethod
    def from_dict(data: dict) -> "QuizDTO":
        return QuizDTO(
            quiz_id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            questions=data.get("questions", [])
        )

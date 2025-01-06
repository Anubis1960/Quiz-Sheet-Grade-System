from src.models.quiz import Quiz


class QuizDTO:
    def __init__(self, quiz_id: str, quiz: dict):
        self.id = quiz_id
        self.quiz = quiz

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "quiz": self.quiz
        }

    @staticmethod
    def from_dict(data: dict) -> "QuizDTO":
        return QuizDTO(
            quiz_id=data.get("id"),
            quiz=data.get("quiz")
        )



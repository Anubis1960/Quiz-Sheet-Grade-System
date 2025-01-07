from src.models.question import Question


class Quiz:
    def __init__(self, title: str, description: str, teacher: str, questions: list[Question] = None):
        self.title = title
        self.description = description
        self.teacher = teacher
        self.questions = questions or []

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "teacher": self.teacher,
            "questions": [question.to_dict() for question in self.questions],
        }

    @staticmethod
    def from_dict(data: dict) -> "Quiz":
        return Quiz(
            title=data.get("title"),
            description=data.get("description"),
            teacher=data.get("teacher"),
            questions=data.get("questions", [])
        )

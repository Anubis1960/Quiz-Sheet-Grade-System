from entities.Question import Question

class Quiz:
    def __init__(self, title, description, teacher, questions = None):
        self.title = title
        self.description = description
        self.teacher = teacher
        if questions is None:
            self.questions = []
        else:
            self.questions = list(questions)
    
    def to_dict(self):
        return {
            "title":self.title,
            "description":self.description,
            "teacher":self.teacher,
            "questions":[question.to_dict() for question in self.questions],
        }
    @staticmethod
    def from_dict(data):
        questions = [Question.from_dict(q) if isinstance(q,dict) else q for q in data.get("questions",[])]
        return Quiz(
            title = data["title"],
            description = data["description"],
            teacher = data["teacher"],
            questions = questions
        )
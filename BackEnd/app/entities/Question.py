from entities.Option import Option

class Question:
    def __init__(self,text, options = None, correct_answers = None):
        self.text = text
        if options is None:
            self.options = []
        else:
            self.options = list(options)
        if correct_answers is None:
            self.correct_answers = []
        else:
            self.correct_answers = list(correct_answers)

    def to_dict(self):
        return {
            "text":self.text,
            "options":[option.to_dict() for option in self.options],
            "correct_answers":self.correct_answers
        }
    
    @staticmethod
    def from_dict(data):
        options = [Option.from_dict(opt) for opt in data.get("options",[])]
        return Question(
            text = data["text"],
            options = options,
            correct_answers = data.get("correct_answers",[])
        )
class Question:
	def __init__(self,text, options = None, correct_answers = None):
		self.text = text
		self.options = options or []
		self.correct_answers = correct_answers or []

	def to_dict(self):
		return {
			"text": self.text,
			"options": self.options,
			"correct_answers": self.correct_answers
		}
	
	@staticmethod
	def from_dict(data):
		return Question(
			text = data["text"],
			options = data.get("options", []),
			correct_answers = data.get("correct_answers",[])
		)
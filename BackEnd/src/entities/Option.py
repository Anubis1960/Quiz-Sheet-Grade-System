class Option:
	def __init__(self,answer):
		self.answer = answer

	def to_dict(self):
		return{
			"answer":self.answer
		}
	
	@staticmethod
	def from_dict(data):
		return Option(
			answer = data["answer"]
		)
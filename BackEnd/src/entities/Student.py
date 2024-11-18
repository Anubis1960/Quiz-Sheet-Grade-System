class Student:
    def __init__(self,unique_id, email):
        self.unique_id = unique_id
        self.email = email
    
    def to_dict(self):
        return {
            "unique_id":self.unique_id,
            "email":self.email
        }
    @staticmethod
    def from_dict(data):
        return Student(
            unique_id = data.get("unique_id"),
            email = data.get('email')
        )
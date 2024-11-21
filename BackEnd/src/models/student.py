class Student:
    def __init__(self, unique_id: str, email: str):
        self.unique_id = unique_id
        self.email = email

    def to_dict(self) -> dict:
        return {
            "unique_id": self.unique_id,
            "email": self.email
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            unique_id=data.get("unique_id"),
            email=data.get('email')
        )

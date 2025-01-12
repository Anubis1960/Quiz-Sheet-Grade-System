class TeacherDTO:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict) -> "TeacherDTO":
        return TeacherDTO(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
        )

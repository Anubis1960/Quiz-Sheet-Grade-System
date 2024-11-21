class Teacher:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_dict(data: dict) -> "Teacher":
        return Teacher(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )

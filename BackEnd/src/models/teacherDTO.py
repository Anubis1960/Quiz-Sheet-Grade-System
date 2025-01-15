class TeacherDTO:
    """
    Data Transfer Object (DTO) for the Teacher entity.
    This class represents a simplified version of the Teacher model used for data transfer.

    Attributes:
        id (str): The unique identifier for the teacher.
        name (str): The name of the teacher.
        email (str): The email address of the teacher.
    """

    def __init__(self, id: str, name: str, email: str):
        """
        Initializes a new TeacherDTO object with the provided id, name, and email.

        Args:
            id (str): The unique identifier for the teacher.
            name (str): The name of the teacher.
            email (str): The email address of the teacher.
        """
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        """
        Converts the TeacherDTO object to a dictionary representation.

        Returns:
            dict: A dictionary containing the TeacherDTO's attributes ('id', 'name', 'email').
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict) -> "TeacherDTO":
        """
        Creates a TeacherDTO object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the teacher's attributes. Expected keys:
                         'id', 'name', and 'email'.

        Returns:
            TeacherDTO: A new TeacherDTO object initialized with data from the dictionary.
        """
        return TeacherDTO(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
        )

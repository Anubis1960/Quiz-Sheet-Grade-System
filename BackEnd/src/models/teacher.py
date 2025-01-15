class Teacher:
    """
    Represents a teacher with a name, email, and password. Provides methods to convert the
    teacher object to and from a dictionary format.

    Attributes:
        name (str): The name of the teacher.
        email (str): The email address of the teacher.
        password (str): The password associated with the teacher.
    """

    def __init__(self, name: str, email: str, password: str):
        """
        Initializes a new Teacher object with the provided name, email, and password.

        Args:
            name (str): The name of the teacher.
            email (str): The email address of the teacher.
            password (str): The password for the teacher.
        """
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        """
        Converts the Teacher object to a dictionary representation.

        Returns:
            dict: A dictionary containing the teacher's attributes ('name', 'email', 'password').
        """
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_dict(data: dict) -> "Teacher":
        """
        Creates a Teacher object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the teacher's attributes. Expected keys:
                         'name', 'email', 'password'.

        Returns:
            Teacher: A new Teacher object initialized with data from the dictionary.
        """
        return Teacher(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )

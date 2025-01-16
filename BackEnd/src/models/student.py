class Student:
    """
    Represents a student with a unique ID and an email address. Provides methods to convert the
    student object to and from a dictionary format.

    Attributes:
        unique_id (str): The unique identifier for the student.
        email (str): The email address of the student.
    """

    def __init__(self, unique_id: str, email: str):
        """
        Initializes a new Student object with the provided unique ID and email.

        Args:
            unique_id (str): The unique identifier for the student.
            email (str): The email address of the student.
        """
        self.unique_id = unique_id
        self.email = email

    def to_dict(self) -> dict:
        """
        Converts the Student object to a dictionary representation.

        Returns:
            dict: A dictionary containing the student's attributes ('unique_id' and 'email').
        """
        return {
            "unique_id": self.unique_id,
            "email": self.email
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        """
        Creates a Student object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the student's attributes. Expected keys:
                         'unique_id' and 'email'.

        Returns:
            Student: A new Student object initialized with data from the dictionary.
        """
        return Student(
            unique_id=data.get("unique_id"),
            email=data.get('email')
        )

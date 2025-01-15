Module src.models.teacher
=========================

Classes
-------

`Teacher(name: str, email: str, password: str)`
:   Represents a teacher with a name, email, and password. Provides methods to convert the
    teacher object to and from a dictionary format.
    
    Attributes:
        name (str): The name of the teacher.
        email (str): The email address of the teacher.
        password (str): The password associated with the teacher.
    
    Initializes a new Teacher object with the provided name, email, and password.
    
    Args:
        name (str): The name of the teacher.
        email (str): The email address of the teacher.
        password (str): The password for the teacher.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.teacher.Teacher`
    :   Creates a Teacher object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the teacher's attributes. Expected keys:
                         'name', 'email', 'password'.
        
        Returns:
            Teacher: A new Teacher object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the Teacher object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the teacher's attributes ('name', 'email', 'password').
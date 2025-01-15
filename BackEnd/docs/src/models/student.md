Module src.models.student
=========================

Classes
-------

`Student(unique_id: str, email: str)`
:   Represents a student with a unique ID and an email address. Provides methods to convert the
    student object to and from a dictionary format.
    
    Attributes:
        unique_id (str): The unique identifier for the student.
        email (str): The email address of the student.
    
    Initializes a new Student object with the provided unique ID and email.
    
    Args:
        unique_id (str): The unique identifier for the student.
        email (str): The email address of the student.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.student.Student`
    :   Creates a Student object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the student's attributes. Expected keys:
                         'unique_id' and 'email'.
        
        Returns:
            Student: A new Student object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the Student object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the student's attributes ('unique_id' and 'email').
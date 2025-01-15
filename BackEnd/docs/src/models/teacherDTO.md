Module src.models.teacherDTO
============================

Classes
-------

`TeacherDTO(id: str, name: str, email: str)`
:   Data Transfer Object (DTO) for the Teacher entity.
    This class represents a simplified version of the Teacher model used for data transfer.
    
    Attributes:
        id (str): The unique identifier for the teacher.
        name (str): The name of the teacher.
        email (str): The email address of the teacher.
    
    Initializes a new TeacherDTO object with the provided id, name, and email.
    
    Args:
        id (str): The unique identifier for the teacher.
        name (str): The name of the teacher.
        email (str): The email address of the teacher.

    ### Static methods

    `from_dict(data: dict) ‑> src.models.teacherDTO.TeacherDTO`
    :   Creates a TeacherDTO object from a dictionary representation.
        
        Args:
            data (dict): A dictionary containing the teacher's attributes. Expected keys:
                         'id', 'name', and 'email'.
        
        Returns:
            TeacherDTO: A new TeacherDTO object initialized with data from the dictionary.

    ### Methods

    `to_dict(self) ‑> dict`
    :   Converts the TeacherDTO object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the TeacherDTO's attributes ('id', 'name', 'email').
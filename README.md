
# QuizGrade

This project is a comprehensive solution designed to handle automated quiz grading using image processing techniques. The application processes images containing bubble sheet forms and extracts information about student IDs, quiz IDs, and answers. The system uses advanced image processing techniques, including contour detection and thresholding, to accurately detect and analyze the bubble sheet, ensuring robust recognition of answers despite varying image quality.


# Versioning

The project was developed using Angular 17, Python 3.12, and Firebase.


# Installation
### 1. Clone the repository:
```bash
git clone https://github.com/Anubis1960/Quiz-Sheet-Grade-System.git
```
### 2. Install dependencies

```
pip install -r .\Backend\src\dependencies.txt
npm install
```

### 3. Configure firebase API key
```
./Backend/src/database.py

cred = credentials.Certificate(key) # switch 'key' with your API key
```

## Usage
To run the project, use the following commands:
```
cd .\FrontEnd\ | ng serve
cd ..\BackEnd\ | py main.py
```

## Documentation
To generate the documentation, run the following:
```bash
  pdoc --html ./Backend/src/ --output-dir <output-directory>
  typedoc --entryPointStrategy expand ./Frontend/src --out <output-directory>
```
    
## Features

- Customizable Quiz Creation: Design and create quizzes tailored to your needs. Customize questions, answer choices, and easily export the quiz to a PDF format for distribution.
- Google Authentication with OAuth2: Implement secure login functionality using Google’s OAuth2 protocol, allowing users to sign in with their Google accounts for a seamless and trustworthy experience.
- Automatic Quiz Grading Algorithm: An advanced image recognition system that automates the grading of multiple-choice bubble sheets. The algorithm detects filled bubbles, interprets answers, and calculates scores.
- User-Friendly Interface: A simple and intuitive interface for quiz creation, grading, and result management, making the system accessible for teachers, students, and administrators.


## Screenshots

![Login](https://imgur.com/KjHg1UW)
![Home](https://imgur.com/iC3AsT5)
![Upload](https://imgur.com/6XT18W1)


## Authors

- [@Anubis1960](https://github.com/Anubis1960)
- [@LzrCatalin](https://github.com/LzrCatalin)
- [@RobertIlea](https://github.com/RobertIlea)


## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/)


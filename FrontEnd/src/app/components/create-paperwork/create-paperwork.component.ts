import { Component } from '@angular/core';
import { Quiz } from '../../models/quiz-model';
import { Question } from '../../models/question-model';
import { QuizService } from '../../services/quiz.service';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-create-paperwork',
  templateUrl: './create-paperwork.component.html',
  styleUrls: ['./create-paperwork.component.css']
})
export class CreatePaperworkComponent {
  quizForm: FormGroup;
  errorMessage: string = '';
  new_question_text: string = '';

  constructor(
    private quiz_service: QuizService,
    private fb: FormBuilder,
    private router: Router,
    private messageService: MessageService
  ) {
    this.quizForm = this.fb.group({
      title: [null, Validators.required],
      description: [null, Validators.required],
      teacher: [null, Validators.required],
      questions: this.fb.array([])
    });
  }

  ngOnInit() {}

  get questions() {
    return (this.quizForm.get('questions') as FormArray);
  }

  getAnswers(questionIndex: number): FormArray {
    return (this.questions.at(questionIndex).get('answers') as FormArray);
  }

  showMessage(severity: string, summary: string, detail: string): void {
    this.messageService.add({ severity, summary, detail });
  }
  addAnswer(questionIndex: number) {
    const answerGroup = this.fb.group({
      answer: ['', Validators.required],
      isCorrect: [false]
    });
    this.getAnswers(questionIndex).push(answerGroup);
  }
  addQuestion(questionText: string) {
    const questionGroup = this.fb.group({
      text: [questionText, Validators.required],
      answers: this.fb.array([]),
      correct_answers: this.fb.array([])
    });
    this.questions.push(questionGroup);
  }

  removeQuestion(questionIndex: number) {
    this.questions.removeAt(questionIndex);
  }

  removeAnswer(questionIndex: number, answerIndex: number) {
    this.getAnswers(questionIndex).removeAt(answerIndex);
  }


  toggleCorrectAnswer(questionIndex: number, answerIndex: number, event: any) {
    const checked = event.target.checked;
    const correctAnswersArray = this.questions.at(questionIndex).get('correct_answers') as FormArray;
    if (checked) {
      correctAnswersArray.push(this.fb.control(answerIndex));
    } else {
      const index = correctAnswersArray.value.indexOf(answerIndex);
      if (index !== -1) {
        correctAnswersArray.removeAt(index);
      }
    }
  }

  createQuiz() {
    console.log('Inside create_quiz...');
    this.quiz_service
      .post_quiz(
        this.quizForm.value.title,
        this.quizForm.value.description,
        this.quizForm.value.teacher,
        this.quizForm.value.questions
      )
      .subscribe(
        (res: any) => {
          console.log(res);
          this.router.navigate(['/quizes/']);
        },
        (error) => {
          console.log('Error ! ! !');
          this.errorMessage = error.error;
          this.showMessage('error', 'Add Quiz Error', this.errorMessage);
        }
      );
  }

  savePaperwork() {
    console.log('Paperwork saved:', this.quizForm.value);
  }
}

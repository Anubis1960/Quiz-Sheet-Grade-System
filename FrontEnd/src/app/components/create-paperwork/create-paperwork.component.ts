import {Component, OnInit} from '@angular/core';
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
export class CreatePaperworkComponent implements OnInit {
  quizForm!: FormGroup;
  errorMessage: string = '';
  new_question_text: string = '';

  constructor(
    private quiz_service: QuizService,
    private fb: FormBuilder,
    private router: Router,
    private messageService: MessageService
  ) {
  }

  ngOnInit() {
    this.quizForm = this.fb.group({
      title: [null, Validators.required],
      description: [null, Validators.required],
      questions: this.fb.array([
        this.fb.group({
          text: ['', Validators.required],
          answers: this.fb.array([
            this.fb.group({
              a_text: ['', Validators.required],
              is_correct: [false]
            })
          ]),
        })
      ])
    });
  }

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
    console.log('Adding answer to question:', questionIndex);
    console.log(this.quizForm.value);
    const answers = this.questions.at(questionIndex).get('answers') as FormArray;
    answers.push(this.fb.group({
      a_text: [null, Validators.required],
      is_correct: [false]
    }));
  }

  addQuestion() {
    console.log(this.quizForm.value);
    this.questions.push(this.fb.group({
      text: [null, Validators.required],
      answers: this.fb.array([
        this.fb.group({
          a_text: [null, Validators.required],
          is_correct: [false]
        })
      ]),
    }));
  }

  removeQuestion(questionIndex: number) {
    this.questions.removeAt(questionIndex);
  }

  removeAnswer(questionIndex: number, answerIndex: number) {
    this.getAnswers(questionIndex).removeAt(answerIndex);
  }


  toggleCorrectAnswer(questionIndex: number, answerIndex: number) {
    let is_correct = this.getAnswers(questionIndex).at(answerIndex).get('is_correct')?.get('value');
    if (is_correct) {
      if (is_correct.value) {
        is_correct.setValue(false);
      }
      else {
        is_correct.setValue(true);
      }
    }
  }

  createQuiz() {
    let title = this.quizForm.value.title;
    let description = this.quizForm.value.description;
    let teacher = 'teacher';
    let questions = this.quizForm.value.questions.map((question: any) => {
      let text = question.text;
      let answers: string[] = question.answers.map((answer: any) => answer.a_text); // Collect answer texts
      let correct_answers: number[] = question.answers
        .map((answer: any, index: number) => {
          if (answer.is_correct) {
            return index;
          }
          return null;
        })
        .filter((index: number | null) => index !== null) as number[];
      return {
        text,
        answers,
        correct_answers
      };
    });
    console.log('Creating quiz:', title, description, teacher, questions);
    this.quiz_service
      .post_quiz(
        this.quizForm.value.title,
        this.quizForm.value.description,
        teacher,
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

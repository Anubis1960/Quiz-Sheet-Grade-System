import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormArray, FormBuilder, FormGroup, Validators} from "@angular/forms";
import {QuizService} from "../../services/quiz.service";
import {MessageService} from "primeng/api";
import {Question} from "../../models/question-model";
import {Quiz} from "../../models/quiz-model";
import { User } from '../../models/user-model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-paperwork-form',
  templateUrl: './paperwork-form.component.html',
  styleUrl: './paperwork-form.component.css'
})
export class PaperworkFormComponent implements OnInit {

  @Input() quiz: Quiz | null = null;
  @Output() formSubmitted = new EventEmitter<Quiz>();

  quizForm!: FormGroup;
  errorMessage: string = '';
  maxAnswers: number = 5;
  maxQuestions: number = 10;
  user: User | undefined;

  constructor(
    private quiz_service: QuizService,
    private router: Router,
    private fb: FormBuilder,
    private messageService: MessageService,
  ) {}

  ngOnInit() {
    this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

    if (this.quiz) {
      console.log('Quiz:', this.quiz);
      this.quizForm = this.fb.group({
        title: [this.quiz.title, Validators.required],
        description: [this.quiz.description, Validators.required],
        questions: this.fb.array(
          this.quiz.questions!.map((question: Question) => {
            return this.fb.group({
              text: [question.text, Validators.required],
              answers: this.fb.array(
                question.options!.map((option: string, index: number) => {
                  return this.fb.group({
                    a_text: [option, Validators.required],
                    is_correct: [question.correct_answers!.includes(index)]
                  });
                })
              )
            });
          })
        )
      });
    }

    else {
      this.refreshForm();
    }
  }

  refreshForm() {
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
    const answers = this.questions.at(questionIndex).get('answers') as FormArray;
    answers.push(this.fb.group({
      a_text: [null, Validators.required],
      is_correct: [false]
    }));
  }

  addQuestion() {
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

  saveQuiz() {
    let title: string= this.quizForm.value.title;
    let description: string = this.quizForm.value.description;
    let teacher_id: string = this.user?.id!;
    let questions: Question[] = this.quizForm.value.questions.map((question: any) => {

      let text: string = question.text;
      let options: string[] = question.answers.map((answer: any) => answer.a_text); // Collect answer texts
      let correct_answers: number[] = question.answers

        .map((answer: any, index: number) => {
          if (answer.is_correct) return index;
          return null;
        })

        .filter((index: number | null) => index !== null) as number[];
      return {
        text,
        options,
        correct_answers
      };
    });
    if (this.quiz) {
      this.quiz_service.update_quiz(this.quiz.id!, title, description, questions).subscribe({
        next: (data: Object) => {
          data = JSON.parse(data as string);
          let n_quiz = Quiz.fromJSON(data);
          this.formSubmitted.emit(n_quiz);
        },
        error: (error) => {
          console.error('Error updating quiz:', error);
          this.errorMessage = 'Could not update quiz. Please try again later.';
        }
      });
    }
    else {
      this.quiz_service
        .post_quiz(
          title,
          description,
          teacher_id,
          questions
        )
        .subscribe({
          next: (data) => {
            console.log('Quiz created:', data);
            // this.refreshForm();
            this.router.navigateByUrl('/home')
          },
          error : (error) => {
            this.errorMessage = error.error;
            this.showMessage('error', 'Create Quiz Error', this.errorMessage);
          }
        });
      this.formSubmitted.emit();
    }
  }

  protected readonly String = String;
}

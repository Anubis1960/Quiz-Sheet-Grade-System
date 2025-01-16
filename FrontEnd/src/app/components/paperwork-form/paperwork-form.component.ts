import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from "@angular/forms";
import { QuizService } from "../../services/quiz.service";
import { MessageService } from "primeng/api";
import { Question } from "../../models/question-model";
import { Quiz } from "../../models/quiz-model";
import { User } from '../../models/user-model';

/**
 * PaperworkFormComponent handles the creation and updating of quizzes.
 * It allows users to add and remove questions, define multiple answers, and mark correct answers.
 *
 * It supports both creating new quizzes and editing existing ones by populating the form with data.
 */
@Component({
  selector: 'app-paperwork-form',
  templateUrl: './paperwork-form.component.html',
  styleUrl: './paperwork-form.component.css'
})
export class PaperworkFormComponent implements OnInit {

  /**
   * The quiz to be edited if provided. Defaults to `null` if creating a new quiz.
   *
   * @type {Quiz | null}
   */
  @Input() quiz: Quiz | null = null;

  /**
   * Emits the updated or new quiz when the form is successfully submitted.
   *
   * @type {EventEmitter<Quiz>}
   */
  @Output() formSubmitted: EventEmitter<Quiz> = new EventEmitter<Quiz>();

  /**
   * The form group representing the quiz form.
   *
   * @type {FormGroup}
   */
  quizForm!: FormGroup;

  /**
   * A string that holds error messages when something goes wrong.
   *
   * @type {string}
   */
  errorMessage: string = '';

  /**
   * The maximum number of answers a question can have.
   *
   * @type {number}
   */
  maxAnswers: number = 5;

  /**
   * The maximum number of questions a quiz can have.
   *
   * @type {number}
   */
  maxQuestions: number = 10;

  /**
   * The logged-in user object containing user details.
   *
   * @type {User | undefined}
   */
  user: User | undefined;

  /**
   * Creates an instance of PaperworkFormComponent.
   *
   * @param quiz_service - The service used to interact with the backend for quiz operations.
   * @param fb - The FormBuilder to manage form controls.
   * @param messageService - The service used to show messages to the user.
   */
  constructor(
    private quiz_service: QuizService,
    private fb: FormBuilder,
    private messageService: MessageService,
  ) {}

  /**
   * Initializes the form with either a provided quiz or a blank one for new quiz creation.
   *
   * @returns {void}
   */
  ngOnInit(): void {
    this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

    if (this.quiz) {
      this.quizForm = this.fb.group({
        title: [this.quiz.title, Validators.required],
        description: [this.quiz.description, Validators.required],
        questions: this.fb.array(
          this.quiz.questions!.map((question: Question) => {
            return this.fb.group({
              text: [question.text, Validators.required],
              answers: this.fb.array(
                question.options!.map((option: string, index: number) => {
                  const isCorrect = question.correct_answers && question.correct_answers.includes(index);
                  return this.fb.group({
                    a_text: [option, Validators.required],
                    is_correct: [isCorrect]
                  });
                })
              )
            });
          })
        )
      });
    } else {
      this.refreshForm();
    }
  }

  /**
   * Refreshes the form with a blank state for a new quiz.
   *
   * @returns {void}
   */
  refreshForm(): void {
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

  /**
   * Gets the form array of questions.
   *
   * @returns {FormArray} The form array of questions.
   */
  get questions(): FormArray {
    return (this.quizForm.get('questions') as FormArray);
  }

  /**
   * Gets the form array of answers for a specific question.
   *
   * @param {number} questionIndex - The index of the question.
   *
   * @returns {FormArray} The form array of answers for the question.
   */
  getAnswers(questionIndex: number): FormArray {
    return (this.questions.at(questionIndex).get('answers') as FormArray);
  }

  /**
   * Displays a message using the `MessageService`.
   *
   * @param {string} severity - The severity level of the message (e.g., 'success', 'error').
   * @param {string} summary - The title or summary of the message.
   * @param {string} detail - The detailed content of the message.
   *
   * @returns {void}
   */
  showMessage(severity: string, summary: string, detail: string): void {
    this.messageService.add({ severity, summary, detail });
  }

  /**
   * Adds a new answer to the specified question.
   *
   * @param {number} questionIndex - The index of the question to which the answer should be added.
   *
   * @returns {void}
   */
  addAnswer(questionIndex: number): void {
    const answers = this.questions.at(questionIndex).get('answers') as FormArray;
    answers.push(this.fb.group({
      a_text: [null, Validators.required],
      is_correct: [false]
    }));
  }

  /**
   * Adds a new question to the quiz.
   *
   * @returns {void}
   */
  addQuestion(): void {
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

  /**
   * Removes a question from the quiz.
   *
   * @param {number} questionIndex - The index of the question to be removed.
   *
   * @returns {void}
   */
  removeQuestion(questionIndex: number): void {
    const updatedQuestions = this.questions.controls.filter((_, index) => index !== questionIndex);
    this.quizForm.setControl('questions', this.fb.array(updatedQuestions));
  }

  /**
   * Removes an answer from a specific question.
   *
   * @param {number} questionIndex - The index of the question whose answer should be removed.
   * @param {number} answerIndex - The index of the answer to be removed.
   *
   * @returns {void}
   */
  removeAnswer(questionIndex: number, answerIndex: number): void {
    const answers = this.getAnswers(questionIndex);
    for (let i = answerIndex; i < answers.length - 1; i++) {
      answers.at(i).setValue(answers.at(i + 1).value || null);
    }
    answers.removeAt(answers.length - 1);
  }

  /**
   * Toggles whether a specific answer is marked as correct.
   *
   * @param {number} questionIndex - The index of the question.
   * @param {number} answerIndex - The index of the answer to be toggled.
   *
   * @returns {void}
   */
  toggleCorrectAnswer(questionIndex: number, answerIndex: number): void {
    let is_correct = this.getAnswers(questionIndex).at(answerIndex).get('is_correct')?.get('value');
    if (is_correct) {
      if (is_correct.value) {
        is_correct.setValue(false);
      } else {
        is_correct.setValue(true);
      }
    }
  }

  /**
   * Saves the quiz by sending it to the backend for either creation or update.
   *
   * @returns {void}
   */
  saveQuiz(): void {
    let title: string = this.quizForm.value.title;
    let description: string = this.quizForm.value.description;
    let teacher_id: string = this.user?.id!;
    let questions: Question[] = this.quizForm.value.questions.map((question: any) => {
      let text: string = question.text;
      let options: string[] = question.answers.map((answer: any) => answer.a_text);
      let correct_answers: number[] = question.answers
        .map((answer: any, index: number) => {
          if (answer.is_correct) return index;
          return null;
        })
        .filter((index: number | null) => index !== null) as number[];
      return { text, options, correct_answers };
    });

    if (this.quiz) {
      this.quiz_service.update_quiz(this.quiz.id!, title, description, questions).subscribe({
        next: (data: Object) => {
          data = JSON.parse(data as string);
          let n_quiz = Quiz.fromJSON(data);
          this.formSubmitted.emit(n_quiz);
        },
        error: (error) => {
          console.error(error);
          this.errorMessage = 'Could not update quiz. Please try again later.';
        }
      });
    } else {
      this.quiz_service
        .post_quiz(title, description, teacher_id, questions)
        .subscribe({
          next: () => {
            this.refreshForm();
          },
          error: (error) => {
            this.errorMessage = error.error;
            this.showMessage('error', 'Create Quiz Error', this.errorMessage);
          }
        });
      this.formSubmitted.emit();
    }
  }

  protected readonly String = String;
}

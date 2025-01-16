import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Quiz } from '../../models/quiz-model';
import { User } from '../../models/user-model';

/**
 * HomePageComponent is responsible for displaying quizzes created by a teacher.
 * It handles fetching quizzes, deleting quizzes, and exporting quizzes as PDFs.
 * It also provides functionality for dialog visibility and description truncation.
 */
@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  /**
   * The list of quizzes retrieved for the teacher.
   *
   * @type {Quiz[]}
   */
  quizzes: Quiz[] = [];

  /**
   * The current index of the selected quiz.
   *
   * @type {number}
   */
  currentIdx: number = 0;

  /**
   * A string to hold error messages.
   *
   * @type {string}
   */
  errorMessage: string = '';

  /**
   * The logged-in user object containing user details.
   *
   * @type {User | undefined}
   */
  user: User | undefined;

  /**
   * An array that holds the visibility status of the dialog for each quiz.
   *
   * @type {boolean[]}
   */
  visibleDialogs: boolean[] = [false];

  /**
   * The quiz currently selected for viewing or editing.
   *
   * @type {Quiz}
   */
  selectedQuiz: Quiz = new Quiz("","","",[]);

  /**
   * Creates an instance of HomePageComponent.
   *
   * @param quizService - The service used to interact with the backend for quiz operations.
   */
  constructor(
    private quizService: QuizService,
  ) {}

  /**
   * Initializes the component by fetching quizzes created by the logged-in teacher.
   *
   * @returns {void}
   */
  ngOnInit(): void {
    this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;
    console.log(this.user);
    if (this.user.id !== undefined) {
      console.log("Fetching quizzes by teacher id: " + this.user.id);
      this.getQuizzesByTeacher(this.user.id)
    }
  }

  /**
   * Fetches the quizzes created by the teacher with the provided ID.
   *
   * @param {string} teacher_id - The ID of the teacher to fetch quizzes for.
   *
   * @returns {void}
   */
  getQuizzesByTeacher(teacher_id: string): void {
    this.quizService.get_quizzes_by_teacher(teacher_id).subscribe({
      next: (data) => {
        this.quizzes = data as Quiz[];
        console.log(this.quizzes);
        this.visibleDialogs = new Array(this.quizzes.length).fill(false);
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = 'Could not fetch quizzes. Please try again later.';
      }
    });
  }

  /**
   * Deletes a quiz by its ID, confirming the action with the user.
   *
   * @param {string} id - The ID of the quiz to delete.
   * @param {number} idx - The index of the quiz in the `quizzes` array to remove.
   *
   * @returns {void}
   */
  deleteQuiz(id: string, idx: number): void{
    if(confirm("Are you sure that you want to delete this quiz?")){
      this.quizService.delete_quiz(id).subscribe({
        next: () => {
          this.quizzes.splice(idx, 1);
        },
        error: (error) => {
          console.error(error);
          this.errorMessage = 'Could not delete quiz. Please try again later.';
        }
      });
    }
  }

  /**
   * Displays the dialog for viewing or editing the selected quiz.
   *
   * @param {number} idx - The index of the quiz in the `quizzes` array to display.
   *
   * @returns {void}
   */
  showDialog(idx: number): void{
    this.selectedQuiz = this.quizzes[idx];
    this.currentIdx = idx;
    this.visibleDialogs[idx] = true;
  }

  /**
   * Closes the currently visible dialog and updates the quiz if modified.
   *
   * @param {Quiz} q - The updated quiz object, if applicable.
   *
   * @returns {void}
   */
  closeDialog(q: Quiz): void{
    this.visibleDialogs = new Array(this.quizzes.length).fill(false);
    if(q){
      this.quizzes[this.currentIdx] = q;
    }
  }

  /**
   * Exports a quiz as a PDF.
   *
   * @param {string} id - The ID of the quiz to export.
   *
   * @returns {void}
   */
  exportPDF(id: string): void{
    this.quizService.export_pdf(id).subscribe({
      next: (data) => {
        const blob = new Blob([data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        window.open(url);
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = 'Could not export PDF. Please try again later.';
      }
    });
  }

  /**
   * Truncates the quiz description to a specified character limit.
   *
   * @param {string} description - The description to truncate.
   * @param {number} limit - The character limit to truncate the description to.
   *
   * @returns {string} The truncated description.
   */
  truncateDescription(description: string, limit: number): string {
    return description.length > limit ? description.substring(0, limit) : description;
  }

  protected readonly String = String;
}

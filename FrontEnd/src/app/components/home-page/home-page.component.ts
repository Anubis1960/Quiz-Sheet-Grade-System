import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Quiz } from '../../models/quiz-model';
import { User } from '../../models/user-model';


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{
  quizzes: Quiz[] = [];
  currentIdx: number = 0;
  errorMessage: string = '';
  user: User | undefined;
  visibleDialogs: boolean[] = [false];
  selectedQuiz: Quiz = new Quiz("","","",[]);
  constructor(
    private quizService: QuizService,
  ){}

  // TODO: DISPLAY QUIZZES BY LOGGED IN USER TO RESOLVE !!!!!!!!!!!!

  ngOnInit(){
    this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

    console.log("User:", this.user)

    if (this.user.id !== undefined) {
      console.log("Searching quizzes called.")
      this.getQuizzesByTeacher(this.user.id)
    }
    console.log("Finished.")
  }

  getQuizzesByTeacher(teacher_id: string) {
    console.log("Searching quizzes for teacher_id: " + teacher_id)
    this.quizService.get_quizzes_by_teacher(teacher_id).subscribe({

      next: (data) => {
        console.log('Quizzes:', data);
        this.quizzes = data as Quiz[];
        this.visibleDialogs = new Array(this.quizzes.length).fill(false);
      },

      error: (error) => {
        console.error('Error fetching quizzes:', error);
        this.errorMessage = 'Could not fetch quizzes. Please try again later.';
      }
    });
  }

  deleteQuiz(id: string, idx: number){
    if(confirm("Are you sure that you want to delete this quiz?")){
      this.quizService.delete_quiz(id).subscribe({
        next: (data) => {
          console.log('Quiz deleted:', data);
          this.quizzes.splice(idx, 1);
        },
        error: (error) => {
          console.error('Error deleting quiz:', error);
          this.errorMessage = 'Could not delete quiz. Please try again later.';
        }
      });
    }
  }

  showDialog(idx: number){
    this.selectedQuiz = this.quizzes[idx];
    this.currentIdx = idx;
    this.visibleDialogs[idx] = true;
  }

  protected readonly String = String;

  closeDialog(q: Quiz){
    this.visibleDialogs = new Array(this.quizzes.length).fill(false);
    if(q){
      this.quizzes[this.currentIdx] = q;
    }

    console.log('Quizzes:', this.quizzes);

  }


  exportPDF(id: string){
    this.quizService.export_pdf(id).subscribe({
      next: (data) => {
        console.log('PDF:', data);
        const blob = new Blob([data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        window.open(url);
      },
      error: (error) => {
        console.error('Error exporting PDF:', error);
        this.errorMessage = 'Could not export PDF. Please try again later.';
      }
    });
  }

  truncateDescription(description: string, limit: number): string {
    return description.length > limit ? description.substring(0, limit) : description;
  }
}

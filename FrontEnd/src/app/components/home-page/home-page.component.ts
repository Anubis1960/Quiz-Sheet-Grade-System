import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Quiz } from '../../models/quiz-model';
import { MessageService } from 'primeng/api';
import { FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Question } from '../../models/question-model';
import { User } from '../../models/user-model';


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{

  teacher_id:string ='mdxM9K6c3H3wFvZLmEbE';
  quizzes: Quiz[] = [];
  errorMessage: string = '';
  quizForm!: FormGroup;
  selectedQuiz!: Quiz;
  visible: boolean = false;
  user: User | undefined;

  constructor(private quizService: QuizService,
    private messageService: MessageService,
    private router: Router,
    ){}

  ngOnInit(){
    this.getQuizzesByTeacher(this.teacher_id);
  }
  showMessage(severity: string, summary: string, detail: string): void {
    this.messageService.add({ severity, summary, detail });
  }
  
  getQuizzesByTeacher(teacher_id: string) {
    this.quizService.get_quizzes_by_teacher(teacher_id).subscribe(
      (data: Object) => { 
        this.quizzes = data as Quiz[];
        console.log('Quizzes fetched:', this.quizzes);
      },
      (error) => {
        console.error('Error fetching quizzes:', error);
        this.errorMessage = 'Could not fetch quizzes. Please try again later.';
      }
    );
  }
  
  deleteQuiz(id:string){
    console.log("Inside deleteQuiz...");
    if(confirm("Are you sure that you want to delete this quiz?")){
      this.quizService.delete_quiz(id).subscribe(()=>{
        console.log("Quiz with id " + id + " deleted successfully!");
        location.reload()
      },(error: any) =>{
        console.log("Error deleting the quiz!");
        this.errorMessage = error.error;
        this.showMessage('error', 'Delete Quiz Error', this.errorMessage);
        location.reload()
      });
    }
  }
  updateQuiz(id:string){
    const updateQuiz = {
      id:this.selectedQuiz.id,
      title:this.selectedQuiz.title,
      description:this.selectedQuiz.description,
      questions: (this.selectedQuiz.questions || []).map((question: any) => {
        const answers = question.options.map((option: string, index: number) => ({
          a_text: option,
          is_correct: question.correct_answers.includes(index)
        }));

        return {
          text: question.text,
          options: question.options,
          correct_answers: question.correct_answers || [],
          answers: answers
        };
      })
    }
    this.quizService.update_quiz(updateQuiz.id!, updateQuiz.title ?? '', updateQuiz.description ?? '', updateQuiz.questions).subscribe((
      res) =>{
        console.log("Quiz updated:",res);
        location.reload();
      },
      (error) =>{
        console.log("Update error:",error)
      }
    )
  }
}

import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Quiz } from '../../models/quiz-model';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{

  teacher_id:string ='asda';
  quizzes: Quiz[] = []
  errorMessage: string = '';

  constructor(private quizService: QuizService,
    private messageService: MessageService
    ){}

  ngOnInit(){
    this.getQuizzesByTeacher(this.teacher_id);
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
}

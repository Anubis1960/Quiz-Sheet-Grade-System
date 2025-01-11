import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Question } from '../models/question-model';

const BASE_URL = 'http://localhost:5000'

@Injectable({
  providedIn: 'root'
})

export class QuizService {

  constructor(private http:HttpClient) { }

  post_quiz(title:string, description:string, teacher: string, question: Question[]){
    const body = {
      title: title,
      description: description,
      teacher: teacher,
      questions: question,
    };
    return this.http.post(`${BASE_URL}/api/quizzes/`,body,{responseType:'text'});
  }

  delete_quiz(id:string){
    return this.http.delete(`${BASE_URL}/api/quizzes/${id}`)
  }

  get_quizzes_by_teacher(teacher_id:string){
    return this.http.get(`${BASE_URL}/api/quizzes/all/${teacher_id}`)
  }
}

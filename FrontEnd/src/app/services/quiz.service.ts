import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Question } from '../models/question-model';
import {Observable} from "rxjs";

const BASE_URL = 'http://localhost:5000';

/**
 * Service for managing quizzes in the system.
 * Provides methods for creating, updating, deleting, retrieving, and grading quizzes.
 */
@Injectable({
  providedIn: 'root'
})
export class QuizService {

  /**
   * Creates an instance of the QuizService.
   * @param http - The `HttpClient` used for making HTTP requests.
   */
  constructor(private http: HttpClient) { }

  /**
   * Posts a new quiz to the system.
   *
   * @param title - The title of the quiz.
   * @param description - A description of the quiz.
   * @param teacher_id - The ID of the teacher who owns the quiz.
   * @param question - An array of `Question` objects that belong to the quiz.
   * @returns {Observable<string>} An Observable that returns the response as text (indicating success or failure).
   *
   * @example
   * quizService.post_quiz('Math Quiz', 'A basic math quiz', 'teacher123', questions).subscribe(response => {
   *   console.log(response); // Response text (success or error)
   * });
   */
  post_quiz(title: string, description: string, teacher_id: string, question: Question[]): Observable<string> {
    const body = {
      title: title,
      description: description,
      teacher: teacher_id,
      questions: question,
    };
    return this.http.post(`${BASE_URL}/api/quizzes/`, body, { responseType: 'text' });
  }

  /**
   * Deletes a quiz by its ID.
   *
   * @param id - The ID of the quiz to be deleted.
   * @returns {Observable<Object>} An Observable that completes once the quiz is deleted.
   *
   * @example
   * quizService.delete_quiz('quiz123').subscribe(() => {
   *   console.log('Quiz deleted successfully');
   * });
   */
  delete_quiz(id: string): Observable<Object> {
    return this.http.delete(`${BASE_URL}/api/quizzes/${id}`);
  }

  /**
   * Retrieves all quizzes for a specific teacher.
   *
   * @param teacher_id - The ID of the teacher whose quizzes are to be retrieved.
   * @returns {Observable<Object>} An Observable that returns an array of quizzes.
   *
   * @example
   * quizService.get_quizzes_by_teacher('teacher123').subscribe(quizzes => {
   *   console.log(quizzes); // Array of quizzes for the teacher
   * });
   */
  get_quizzes_by_teacher(teacher_id: string): Observable<Object> {
    return this.http.get(`${BASE_URL}/api/quizzes/all/${teacher_id}`);
  }

  /**
   * Updates an existing quiz by its ID.
   *
   * @param id - The ID of the quiz to update.
   * @param title - The updated title of the quiz.
   * @param description - The updated description of the quiz.
   * @param question - An array of updated `Question` objects for the quiz.
   * @returns {Observable<string>} An Observable that returns the response as text (indicating success or failure).
   *
   * @example
   * quizService.update_quiz('quiz123', 'Updated Math Quiz', 'An updated math quiz description', questions).subscribe(response => {
   *   console.log(response); // Response text (success or error)
   * });
   */
  update_quiz(id: string, title: string, description: string, question: Question[]): Observable<string> {
    const body = {
      title: title,
      description: description,
      questions: question,
    };
    return this.http.put(`${BASE_URL}/api/quizzes/${id}`, body, { responseType: 'text' });
  }

  /**
   * Exports a quiz as a PDF.
   *
   * @param id - The ID of the quiz to export.
   * @returns {Observable<Blob>} An Observable that returns a `Blob` containing the PDF data.
   *
   * @example
   * quizService.export_pdf('quiz123').subscribe(pdfBlob => {
   *   // Handle the PDF Blob
   * });
   */
  export_pdf(id: string): Observable<Blob> {
    return this.http.get(`${BASE_URL}/api/quizzes/pdf/${id}`, { responseType: 'blob' });
  }

  /**
   * Grades a paper by uploading an image file of the answer sheet.
   *
   * @param file - The file containing the image of the answer sheet.
   * @returns {Observable<string>} An Observable that returns the response as text (indicating success or failure).
   *
   * @example
   * quizService.grade_paper(file).subscribe(response => {
   *   console.log(response); // Response text (success or error)
   * });
   */
  grade_paper(file: File): Observable<string> {
    const formData = new FormData();
    formData.append('image', file);

    return this.http.post(`${BASE_URL}/api/quizzes/grade`, formData, { responseType: 'text' });
  }
}

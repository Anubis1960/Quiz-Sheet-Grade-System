import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

const BASE_URL = 'http://localhost:5000/';

/**
 * Service for managing student data in the system.
 * Provides methods to interact with the student-related API endpoints.
 */
@Injectable({
  providedIn: 'root'
})
export class StudentService {

  /**
   * Creates an instance of the StudentService.
   * @param http - The `HttpClient` used for making HTTP requests.
   */
  constructor(private http: HttpClient) {}

  /**
   * Adds a new student to the system.
   *
   * @param unique_id - The unique identifier for the student.
   * @param email - The email address of the student.
   * @returns {Observable<any>} An Observable containing the response from the API.
   *
   * @example
   * const newStudent = studentService.add_student('12345', 'student@example.com');
   * newStudent.subscribe(response => {
   *   console.log(response);
   * });
   */
  add_student(unique_id: string, email: string): Observable<any> {
    const body = {
      unique_id: unique_id,
      email: email
    };
    return this.http.post(`${BASE_URL}/api/students/`, body);
  }
}

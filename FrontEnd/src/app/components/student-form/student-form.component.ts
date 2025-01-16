import { Component } from '@angular/core';
import { StudentService } from "../../services/student.service";

/**
 * StudentFormComponent is responsible for handling the form to register a new student.
 * It collects the unique ID and email of a student and submits the data to the backend using the `StudentService`.
 */
@Component({
  selector: 'app-student-form',
  templateUrl: './student-form.component.html',
  styleUrls: ['./student-form.component.css']
})
export class StudentFormComponent {
  /**
   * The email address of the student.
   * @type {string}
   */
  email: string = '';

  /**
   * The unique ID of the student.
   * @type {string}
   */
  unique_id: string = '';

  /**
   * Creates an instance of the StudentFormComponent.
   *
   * @param studentService - The `StudentService` used to interact with the backend for student-related operations.
   */
  constructor(private studentService: StudentService) { }

  /**
   * Handles the form submission. It calls the `add_student` method from the `StudentService`
   * to add a new student with the provided unique ID and email.
   *
   * @returns {void}
   *
   * @example
   * this.onSubmit(); // Submits the student form to the backend
   */
  onSubmit(): void {
    this.studentService.add_student(this.unique_id, this.email).subscribe({
      next: () => {
      },
      error: () => {
      }
    });
  }
}

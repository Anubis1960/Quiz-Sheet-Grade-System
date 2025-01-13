import { Component } from '@angular/core';
import {StudentService} from "../../services/student.service";

@Component({
  selector: 'app-student-form',
  templateUrl: './student-form.component.html',
  styleUrl: './student-form.component.css'
})
export class StudentFormComponent {
  email: string = '';
  unique_id: string = '';
  constructor(private studentService: StudentService) { }

  onSubmit() {
    this.studentService.add_student(this.unique_id, this.email).subscribe({
      next: (data) => {
      },
      error: (error) => {
      }
    });
  }

}

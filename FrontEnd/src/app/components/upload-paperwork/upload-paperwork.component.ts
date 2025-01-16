
import { Component } from '@angular/core';
import { FileUploadEvent } from 'primeng/fileupload';
import { QuizService } from "../../services/quiz.service";

/**
 * UploadPaperworkComponent handles the functionality for uploading a quiz paper
 * and grading it based on the uploaded file.
 *
 * The component allows users to upload files, sends them to the server for grading,
 * and displays the resulting score or any error messages.
 */
@Component({
  selector: 'app-upload-paperwork',
  templateUrl: './upload-paperwork.component.html',
  styleUrls: ['./upload-paperwork.component.css']
})
export class UploadPaperworkComponent {
  /**
   * Stores the files uploaded by the user.
   * @type {any[]}
   */
  uploadedFiles: any[] = [];

  /**
   * A message to be displayed to the user, typically showing the score or an error.
   * @type {string}
   */
  msg: string = '';

  /**
   * Creates an instance of the UploadPaperworkComponent.
   *
   * @param quizService - The `QuizService` used to interact with the backend for paper grading.
   */
  constructor(private quizService: QuizService) { }

  /**
   * Handles the file upload event. This method pushes the uploaded files into an array
   * and sends each file to the backend for grading using the `QuizService`.
   * After grading, it sets the `msg` property with the resulting score or error message.
   *
   * @param $event - The file upload event that contains the uploaded files.
   *
   * @returns {void}
   *
   * @example
   * this.onUpload(event); // Handles file upload and grades the paper
   */
  onUpload($event: FileUploadEvent): void {
    this.uploadedFiles = [];
    this.msg = '';

    // Collect all uploaded files
    for (let file of $event.files) {
      this.uploadedFiles.push(file);
    }

    // Process each uploaded file for grading
    for (let file of this.uploadedFiles) {
      console.log(file);
      this.quizService.grade_paper(file).subscribe({
        next: (data: Object) => {
          const response = JSON.parse(data as string);
          this.msg = "Score: " + response.score;
          if (response.message !== undefined) {
            this.msg += " - " + response.message;
          }
        },
        error: (error: any) => {
          this.msg = error?.error || 'An unknown error occurred.';
        }
      });
    }
  }
}

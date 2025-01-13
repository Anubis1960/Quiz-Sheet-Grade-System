import {Component} from '@angular/core';
import {FileUploadEvent} from 'primeng/fileupload';
import {QuizService} from "../../services/quiz.service";

@Component({
  selector: 'app-upload-paperwork',
  templateUrl: './upload-paperwork.component.html',
  styleUrls: ['./upload-paperwork.component.css']
})
export class UploadPaperworkComponent {
  uploadedFiles: any[] = [];
  msg: string = '';
  severity: string = 'info';

  constructor(private quizService: QuizService) { }

  onUpload($event: FileUploadEvent) {
    for (let file of $event.files) {
      this.uploadedFiles.push(file);
    }

    console.log('Uploaded files:', this.uploadedFiles);

    for (let file of this.uploadedFiles) {
      console.log('Processing file:', file);
      this.quizService.grade_paper(file).subscribe({
        next: (data: Object) => {
          console.log('Paper graded:', data);
          this.msg = "Score: " + JSON.parse(data as string).score;
          if (JSON.parse(data as string).message !== undefined) {
            this.msg += " - " + JSON.parse(data as string).message;
          }
          console.log('Message:', this.msg);
          this.severity = 'success';
        },
        error: (error: any) => {
          console.error('Error grading paper:', error);
          this.msg = error?.error || 'An unknown error occurred.';
          this.severity = 'error';
        }
      });
    }

    this.clear();
  }

  clear() {
    this.uploadedFiles = [];
  }

}

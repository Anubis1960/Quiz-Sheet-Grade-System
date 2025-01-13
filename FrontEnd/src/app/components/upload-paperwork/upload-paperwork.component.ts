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
        },
        error: (error: any) => {
          console.error('Error grading paper:', error);
          this.msg = error?.error || 'An unknown error occurred.';
        }
      });
    }

    this.clear();
  }

  clear() {
    this.uploadedFiles = [];
  }

  nullifyMessage() {
    this.msg = '';
  }


}

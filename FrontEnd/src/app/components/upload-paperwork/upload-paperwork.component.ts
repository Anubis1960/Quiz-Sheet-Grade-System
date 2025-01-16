import {Component} from '@angular/core';
import {FileUploadEvent} from 'primeng/fileupload';
import {QuizService} from "../../services/quiz.service";
import {MessageService} from "primeng/api";

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
    this.uploadedFiles = [];
    this.msg = '';
    for (let file of $event.files) {
      this.uploadedFiles.push(file);
    }

    for (let file of this.uploadedFiles) {
      this.quizService.grade_paper(file).subscribe({
        next: (data: Object) => {
          this.msg = "Score: " + JSON.parse(data as string).score;
          if (JSON.parse(data as string).message !== undefined) {
            this.msg += " - " + JSON.parse(data as string).message;
          }
        },
        error: (error: any) => {
          this.msg = error?.error || 'An unknown error occurred.';
        }
      });
    }
  }
}

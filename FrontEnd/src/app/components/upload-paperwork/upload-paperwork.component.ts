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

  constructor(private quizService: QuizService, private messageService: MessageService) { }

  onUpload($event: FileUploadEvent) {
    this.messageService.clear('msg');
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
          console.log('Message:', this.msg);
          this.messageService.add({severity:'success', summary:'Success', detail:this.msg, life: 5000, closable: true, id: 'msg'});
        },
        error: (error: any) => {
          console.error('Error grading paper:', error);
          this.msg = error?.error || 'An unknown error occurred.';
          this.messageService.add({severity:'error', summary:'Error', detail:this.msg, life: 5000, closable: true, id: 'msg'});
        }
      });
    }
  }
}

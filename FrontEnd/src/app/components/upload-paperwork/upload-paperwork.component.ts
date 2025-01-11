import { Component } from '@angular/core';
import { FileUploadEvent } from 'primeng/fileupload';
import { Quiz } from '../../models/quiz-model';

@Component({
  selector: 'app-upload-paperwork',
  templateUrl: './upload-paperwork.component.html',
  styleUrls: ['./upload-paperwork.component.css']
})
export class UploadPaperworkComponent {
  uploadedFiles: Quiz[] = [];

  onUpload($event: FileUploadEvent) {
    throw new Error('Method not implemented.');
  }
}

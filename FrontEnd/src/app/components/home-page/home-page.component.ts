import { Component } from '@angular/core';
import { FileUploadEvent } from 'primeng/fileupload';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent {
  uploadedFiles: any[] = [];

  onUpload($event: FileUploadEvent) {
    throw new Error('Method not implemented.');
  }

}

import {Component, OnInit} from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { MessageService } from 'primeng/api';
import {Question} from "../../models/question-model";

@Component({
  selector: 'app-create-paperwork',
  templateUrl: './create-paperwork.component.html',
  styleUrls: ['./create-paperwork.component.css']
})
export class CreatePaperworkComponent implements OnInit {
  ngOnInit() {
  }
}

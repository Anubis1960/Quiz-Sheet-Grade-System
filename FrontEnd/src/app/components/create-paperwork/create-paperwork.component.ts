import { Component } from '@angular/core';

@Component({
  selector: 'app-create-paperwork',
  templateUrl: './create-paperwork.component.html',
  styleUrl: './create-paperwork.component.css'
})
export class CreatePaperworkComponent {
  
  questions: any[] = [];

  addQuestion() {
    this.questions.push({
      text: '',
      answers: [{ text: '', isCorrect: false }],
    });
  }

  removeQuestion(index: number) {
    this.questions.splice(index, 1);
  }

  addAnswer(questionIndex: number) {
    this.questions[questionIndex].answers.push({ text: '', isCorrect: false });
  }

  removeAnswer(questionIndex: number, answerIndex: number) {
    this.questions[questionIndex].answers.splice(answerIndex, 1);
  }

  savePaperwork() {
    console.log('Paperwork saved:', this.questions);
  }
}

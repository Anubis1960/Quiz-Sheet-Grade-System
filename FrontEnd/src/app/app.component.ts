import { Component, ViewEncapsulation } from '@angular/core';

/**
 * AppComponent serves as the root component of the Angular application.
 * It sets the title for the application and configures the view encapsulation.
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {

  /**
   * The title of the application.
   * This title is bound to the template and is used as a label or heading.
   *
   * @type {string}
   */
  title: string = 'QuizGrade';
}

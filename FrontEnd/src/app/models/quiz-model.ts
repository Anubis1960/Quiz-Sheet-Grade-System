import { Question } from "./question-model";

/**
 * Represents a Quiz containing a set of questions.
 * The Quiz class holds information such as the quiz ID, title, description, and an array of questions.
 */
export class Quiz {
  /**
   * The unique identifier for the quiz.
   * @type {string | undefined}
   */
  id: string | undefined;

  /**
   * The title of the quiz.
   * @type {string | undefined}
   */
  title: string | undefined;

  /**
   * A description of the quiz.
   * @type {string | undefined}
   */
  description: string | undefined;

  /**
   * An array of questions included in the quiz.
   * @type {Question[] | undefined}
   */
  questions: Question[] | undefined;

  /**
   * Creates an instance of a Quiz.
   *
   * @param id - The unique identifier for the quiz.
   * @param title - The title of the quiz.
   * @param description - A description of the quiz.
   * @param questions - An array of `Question` objects that belong to the quiz.
   */
  constructor(id: string, title: string, description: string, questions: Question[]) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.questions = questions;
  }

  /**
   * Creates a Quiz instance from a JSON object.
   *
   * @param json - The JSON object containing the properties of the quiz.
   * @returns {Quiz} A new Quiz instance populated with data from the JSON object.
   *
   * @example
   * const quiz = Quiz.fromJSON({
   *   id: "1",
   *   title: "Math Quiz",
   *   description: "A basic math quiz",
   *   questions: [{ text: "What is 2 + 2?", options: ["3", "4", "5"], correct_answers: [1] }]
   * });
   * console.log(quiz.title); // "Math Quiz"
   */
  static fromJSON(json: any): Quiz {
    return new Quiz(json.id, json.title, json.description, json.questions);
  }
}

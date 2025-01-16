/**
 * Represents a Question in a quiz.
 * The Question class holds the text of the question, the options available, and the indices of the correct answers.
 */
export class Question {
  /**
   * The text of the question.
   * @type {string | undefined}
   */
  text: string | undefined;
  /**
   * A list of options for the question.
   * @type {string[] | undefined}
   */
  options: string[] | undefined;

  /**
   * An array of indices representing the correct answers from the options array.
   * @type {number[] | undefined}
   */
  correct_answers: number[] | undefined;

  /**
   * Creates an instance of a Question.
   *
   * @param text - The text of the question.
   * @param options - The list of options for the question.
   * @param correct_answers - An array of indices representing the correct answers from the options array.
   */
  constructor(text: string, options: string[], correct_answers: number[]) {
    this.text = text;
    this.options = options;
    this.correct_answers = correct_answers;
  }
}

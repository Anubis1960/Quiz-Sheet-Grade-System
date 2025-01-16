/**
 * Represents a User in the system.
 * The User class holds details about a user such as ID, name, and email.
 */
export class User {
  /**
   * The unique identifier for the user.
   * @type {string | undefined}
   */
  id: string | undefined;

  /**
   * The name of the user.
   * @type {string | undefined}
   */
  name: string | undefined;

  /**
   * The email address of the user.
   * @type {string | undefined}
   */
  email: string | undefined;

  /**
   * Creates an instance of a User.
   *
   * @param id - The unique identifier for the user.
   * @param name - The full name of the user.
   * @param email - The email address of the user.
   */
  constructor(id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
}

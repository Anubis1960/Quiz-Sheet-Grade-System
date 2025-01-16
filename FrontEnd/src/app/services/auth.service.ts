import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user-model';
import { Observable } from 'rxjs';

const BASE_URL = 'http://localhost:5000';

/**
 * Service for handling user authentication.
 * Provides methods for logging in and registering users.
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  /**
   * Creates an instance of the AuthService.
   * @param http - The `HttpClient` used for making HTTP requests.
   */
  constructor(private http: HttpClient) { }

  /**
   * Logs in a user with the provided email and password.
   *
   * @param email - The email address of the user attempting to log in.
   * @param password - The password of the user.
   * @returns {Observable<User>} An Observable that returns a `User` object containing user data if the login is successful.
   *
   * @example
   * authService.login('user@example.com', 'password123').subscribe(user => {
   *   console.log(user); // User object returned after successful login
   * });
   */
  login(email: string, password: string): Observable<User> {
    return this.http.post<User>(`${BASE_URL}/login`, { email, password });
  }

  /**
   * Registers a new user with the provided name, email, and password.
   *
   * @param name - The name of the user being registered.
   * @param email - The email address of the user being registered.
   * @param password - The password for the new user.
   * @returns {Observable<User>} An Observable that returns the `User` object of the newly registered user.
   *
   * @example
   * authService.register('John Doe', 'john@example.com', 'password123').subscribe(user => {
   *   console.log(user); // User object of the newly registered user
   * });
   */
  register(name: string, email: string, password: string): Observable<User> {
    return this.http.post<User>(`${BASE_URL}/api/teachers/`, { name, email, password });
  }
}

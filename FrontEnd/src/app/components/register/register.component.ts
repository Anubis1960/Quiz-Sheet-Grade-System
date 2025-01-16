import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

/**
 * Component for handling user registration functionality.
 * Allows users to register by providing their name, email, and password.
 */
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  /**
   * The newly registered user details.
   * @type {User | undefined}
   */
  user: User | undefined;

  /**
   * The user's name input for registration.
   * @type {string}
   */
  name: string;

  /**
   * The user's email input for registration.
   * @type {string}
   */
  email: string;

  /**
   * The user's password input for registration.
   * @type {string}
   */
  password: string;

  /**
   * Creates an instance of RegisterComponent.
   *
   * @param router - The `Router` service for navigating between views.
   * @param authSerrvice
   */
  constructor(private router: Router, private authSerrvice: AuthService) {
    this.name = '';
    this.email = '';
    this.password = '';
  }

  /**
   * Handles the registration process by calling the `register` method from `AuthService`.
   * On successful registration, the user is redirected to the home page.
   *
   * @returns {void}
   *
   * @example
   * this.onRegister(); // Registers the user and redirects
   */
  onRegister(): void {
    this.authSerrvice.register(this.name, this.email, this.password).subscribe({
      next: () => {

        this.router.navigateByUrl('')
      },
      error: () => {
      }
    })
  }
}

import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

/**
 * Component for handling user login functionality.
 * Allows users to log in using email/password or Google authentication.
 */
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  /**
   * The user's email input for login.
   * @type {string}
   */
  email: string;

  /**
   * The user's password input for login.
   * @type {string}
   */
  password: string;

  /**
   * The authenticated user details.
   * @type {User | undefined}
   */
  user: User | undefined;
  /**
   * Creates an instance of LoginComponent.
   *
   * @param authService - The `AuthService` for handling authentication logic.
   * @param router - The `Router` service for navigating between views.
   */
  constructor(private authService: AuthService,
              private router: Router) {
    this.email = '';
    this.password = '';
  }

  /**
   * Handles the login process by calling the `login` method from `AuthService`.
   * If login is successful, the user details are stored in sessionStorage and the user is redirected to the home page.
   * If login fails, an error message is logged.
   *
   * @returns {void}
   *
   * @example
   * this.onLogin(); // Logs the user in and redirects
   */
  onLogin(): void {
    this.authService.login(this.email, this.password).subscribe({
      next: (data: User) => {
        this.user = data;
        sessionStorage.setItem('user', JSON.stringify(this.user));
        // Redirect home
        this.router.navigateByUrl('/home');
      },
      error: (error) => {
        console.error();
      }
    });
  }

  /**
   * Initiates login with Google by redirecting to the backend login URL.
   *
   * @returns {void}
   *
   * @example
   * this.loginWithGoogle(); // Redirects user to Google login
   */
  loginWithGoogle(): void {
    console.log("Google Auth selected...");
    window.location.href = 'http://localhost:5000/login';
  }
}

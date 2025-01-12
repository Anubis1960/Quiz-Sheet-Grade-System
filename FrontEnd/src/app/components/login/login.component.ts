import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../../models/user-model';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { delay } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string;
  password: string;
  user: User | undefined;

  constructor(private http: HttpClient, private authService: AuthService, 
    private router: Router) {
      this.email = '';
      this.password = '';
  }

  onLogin(){
    console.log(this.email + " " + this.password)
    this.authService.login(this.email, this.password).subscribe({
      next: (data: User) => {
        this.user = data;
        console.log(this.user.id)
        sessionStorage.setItem('user', JSON.stringify(this.user));
        console.log(sessionStorage.getItem('user'))   
        
        // Redirect home
        this.router.navigateByUrl('/home');
      },
      error: (error) => {
        console.log("Failed to loggin.")
      }
    });
  }

  loginWithGoogle() {
    console.log("Google Auth selected...")
    window.location.href = 'http://localhost:5000/login';
    this.router.navigateByUrl('/home')
  }
}

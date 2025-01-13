import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  user: User | undefined;
  name: string;
  email: string;
  password: string;

  constructor(private httpClient: HttpClient, private router: Router, private authSerrvice: AuthService) {
    this.name = '';
    this.email = '';
    this.password = '';
  }

  onRegister() {
    this.authSerrvice.register(this.name, this.email, this.password).subscribe({
      next: (res) => {

        this.router.navigateByUrl('')
      },
      error: (error) => {
      }
    })
  }

  goToLogin() {
    this.router.navigateByUrl('')
  }
}

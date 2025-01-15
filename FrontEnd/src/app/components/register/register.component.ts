import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
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

  constructor(private router: Router, private authSerrvice: AuthService) {
    this.name = '';
    this.email = '';
    this.password = '';
  }

  onRegister() {
    this.authSerrvice.register(this.name, this.email, this.password).subscribe({
      next: () => {

        this.router.navigateByUrl('')
      },
      error: () => {
      }
    })
  }
}

import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {TokenService} from "../../services/token.service";

@Component({
  selector: 'app-redirect',
  templateUrl: './redirect.component.html',
  styleUrl: './redirect.component.css'
})
export class RedirectComponent implements OnInit{

  constructor(private router: Router, private tokenService: TokenService) {
  }

  ngOnInit() {
    const token = this.tokenService.getToken();
    if (token) {
      this.tokenService.validateToken(token).subscribe({
        next: () => {
          this.router.navigate(['/home']);
        },
        error: () => {
          this.router.navigate(['/login']);
        }
      });
    } else {
      this.router.navigate(['/login']);
    }
  }

}

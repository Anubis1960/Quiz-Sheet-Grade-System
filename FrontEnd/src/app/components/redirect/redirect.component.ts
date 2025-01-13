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
    if (this.tokenService.getToken()) {
      this.router.navigateByUrl('/create-paperwork');
    } else {
      this.router.navigateByUrl('/login');
    }
  }

  ngOnInit() {
  }

}

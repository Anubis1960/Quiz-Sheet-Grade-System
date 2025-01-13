import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-callback',
  templateUrl: './callback.component.html',
  styleUrl: './callback.component.css'
})
export class CallbackComponent implements OnInit{
  constructor(private router: Router) {}

  ngOnInit(): void {
    console.log("CallBack component");

    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('access_token');
      console.log("Token: " + token)
      const userData = urlParams.get('user_data');
      console.log("User data: " + userData)

      console.log(userData);

      if (token && userData) {
        console.log("Successfully retrieved token and userdata");
        sessionStorage.setItem('access_token', token);

        // Parse the user data from the query string
        const user = JSON.parse(userData);
        sessionStorage.setItem('user', JSON.stringify(user));

        this.router.navigateByUrl('/home');
        
      } else {
        console.error('Failed to retrieve access token or user data');
      }
    }
  }

}

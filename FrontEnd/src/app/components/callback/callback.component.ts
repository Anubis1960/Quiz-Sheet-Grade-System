import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from "../../models/user-model";

/**
 * CallbackComponent is used to handle the response from the authentication service
 * after the user has been redirected back to the application.
 * It processes the access token, user data, and token received from the authentication provider,
 * and saves the user information in the sessionStorage for later use.
 */
@Component({
  selector: 'app-callback',
  templateUrl: './callback.component.html',
  styleUrls: ['./callback.component.css']
})
export class CallbackComponent implements OnInit {

  /**
   * Constructs the CallbackComponent.
   *
   * @param {ActivatedRoute} routeSnapshot - ActivatedRoute instance for fetching query parameters.
   * @param {Router} router - Router instance for navigation.
   */
  constructor(private routeSnapshot: ActivatedRoute, private router: Router) {}

  /**
   * Lifecycle hook that is called when the component is initialized.
   * It extracts the access token, user data, and token from the URL query parameters.
   * If all parameters are available, the user data is parsed, and the user object is stored in sessionStorage.
   * The user is then redirected to the home page.
   * If the parameters are missing or sessionStorage is not available, the user is redirected to the login page.
   *
   * @returns {void}
   */
  ngOnInit(): void {
    console.log("CallBack component");

    const access_token = this.routeSnapshot.snapshot.queryParamMap.get('access_token');
    const user_data = this.routeSnapshot.snapshot.queryParamMap.get('user_data');
    const token = this.routeSnapshot.snapshot.queryParamMap.get('token');

    if (access_token && user_data && token) {
      if (typeof sessionStorage !== 'undefined') {
        // sessionStorage.setItem('access_token', access_token);
        const sanitizedUserData = user_data.replace(/'/g, '"');
        const parsedUserData = JSON.parse(sanitizedUserData);

        // Construct the user object
        const user = {
          user_data: parsedUserData as User,
          token: token
        };

        console.log("User object:", user);
        sessionStorage.setItem('user', JSON.stringify(user));
        this.router.navigateByUrl('/home');
      }
      else {
        console.log("Session storage is not supported");
        this.router.navigateByUrl('/login');
      }
    } else {
      console.log("Failed to retrieve access token and user data");
      this.router.navigateByUrl('/login');
    }
  }

}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import {TokenService} from "../../services/token.service";

/**
 * Sidebar component responsible for managing the sidebar menu, generating URLs with tokens,
 * logging out, and navigating to various pages.
 */
@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  /**
   * Controls the visibility of the sidebar.
   * @type {boolean}
   */
  sidebarVisible: boolean = false;

  /**
   * Controls the visibility of the dialog box for the generated URL.
   * @type {boolean}
   */
  dialogVisible: boolean = false;

  /**
   * The base URL used to generate the final URL for the student with the token.
   * @type {string}
   */
  generatedUrl: string = 'http://localhost:4200/student?token=';

  /**
   * An array of menu items to be displayed in the sidebar.
   * @type {MenuItem[]}
   */
  items: MenuItem[] = [];

  /**
   * Creates an instance of SidebarComponent.
   *
   * @param router - The `Router` service used for navigation.
   * @param tokenService - The `TokenService` used for generating tokens.
   */
  constructor(private router: Router, private tokenService: TokenService) { }

  /**
   * Initializes the component by setting up the sidebar menu items.
   *
   * @returns {void}
   */
  ngOnInit(): void {
    this.initializeMenuItems();
  }

  /**
   * Initializes the sidebar menu items with labels, icons, and commands for various actions.
   * These include navigating to the home page, managing paperwork, generating URLs, and logging out.
   *
   * @returns {void}
   */
  initializeMenuItems(): void {
    this.items = [
      {
        label: 'Home',
        icon: 'pi pi-fw pi-home',
        command: () => this.toggleHomePage()
      },
      {
        label: 'Paperwork',
        icon: 'pi pi-file',
        items: [
          {
            label: 'Create paperwork',
            icon: 'pi pi-file-edit',
            routerLink: '/create-paperwork',
          },
          {
            label: 'Upload paperwork',
            icon: 'pi pi-file-import',
            routerLink: '/upload-paperwork'
          },
        ]
      },
      {
        label: 'Generate URL',
        icon: 'pi pi-link',
        command: () => this.generateUrl()
      },
      {
        label: 'Logout',
        icon: 'pi pi-sign-out',
        command: () => this.toggleLogOut()
      },
    ];

    console.log("Menu items:", this.items);
  }

  /**
   * Navigates to the home page.
   *
   * @returns {void}
   *
   * @example
   * this.toggleHomePage(); // Navigates to the home page
   */
  toggleHomePage(): void {
    this.router.navigateByUrl('/home')
  }

  /**
   * Clears session and local storage and redirects to the login page.
   *
   * @returns {void}
   *
   * @example
   * this.toggleLogOut(); // Logs the user out and redirects to login page
   */
  toggleLogOut(): void {
    sessionStorage.clear();
    localStorage.clear();
    this.router.navigateByUrl('/login')
  }

  /**
   * Generates a token for the user and constructs the URL to be copied to the clipboard.
   * Displays a dialog with the generated URL.
   *
   * @returns {void}
   *
   * @example
   * this.generateUrl(); // Generates a token and URL for the student
   */
  generateUrl(): void {
    this.dialogVisible = true;
    const user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data;
    this.tokenService.generateToken({id: user.id, email: user.email}).subscribe({
      next: (data) => {
        console.log("Data:", data);
        this.generatedUrl = 'http://localhost:4200/student?token=' + data['token'];
        console.log("URL:", this.generatedUrl);
      },
      error: (error) => {
        console.error();
      }
    });
  }

  /**
   * Copies the provided text to the user's clipboard.
   *
   * @param text - The text to be copied to the clipboard.
   * @returns {void}
   *
   * @example
   * this.copyToClipboard('http://localhost:4200/student?token=xyz'); // Copies the URL to clipboard
   */
  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(
      () => {
        console.log('Text copied to clipboard');
      },
      (err) => {
        console.error();
      }
    );
  }
}

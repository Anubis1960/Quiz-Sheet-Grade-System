import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';
import {TokenService} from "../../services/token.service";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  sidebarVisible: boolean = false;
  items: MenuItem[] = [];

  constructor(private tokenService: TokenService) { }

  ngOnInit() {
    this.initializeMenuItems();
  }

  initializeMenuItems() {
    if (!this.items || this.items.length === 0) {  // Ensure this is only initialized once
      this.items = [
        {
          label: 'Home',
          icon: 'pi pi-fw pi-home',
          routerLink: '/home'
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
          label: 'Logout',
          icon: 'pi pi-sign-out',
          routerLink: '/login',
          command: () => {
            this.toggleLogOut();
          }
        }
      ];
    }

    console.log("Menu items:", this.items);
  }

  toggleLogOut(){
    console.log("Logging out.")
    sessionStorage.clear();
    localStorage.clear();
  }

  generateUrl(){
    let token = '';
    const user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data
    this.tokenService.generateToken({id: user.id, email: user.email}).subscribe({
      next: (data) => {
        token = data.token

      },
      error: (error) => {
        console.error('Error generating token:', error);
      }
    });
    const url = `http://localhost:5000/login?token=${token}`;
  }
}

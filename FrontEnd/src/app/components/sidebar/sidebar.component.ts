import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  sidebarVisible: boolean = false;
  items: MenuItem[] = [];

  ngOnInit(){
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
}

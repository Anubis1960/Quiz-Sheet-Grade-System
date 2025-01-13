import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  sidebarVisible: boolean = false;
  items: MenuItem[] = [];

  constructor(private router: Router) {}

  ngOnInit(){
    this.initializeMenuItems();
  }

  initializeMenuItems() {
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
        label: 'Logout',
        icon: 'pi pi-sign-out',
        command: () => this.toggleLogOut()
      }
    ];
    
    console.log("Menu items:", this.items);
  }

  toggleHomePage() {
    this.router.navigateByUrl('/home')
  }

  toggleLogOut(){
    sessionStorage.clear();
    localStorage.clear();
    this.router.navigateByUrl('/login')
  }
}

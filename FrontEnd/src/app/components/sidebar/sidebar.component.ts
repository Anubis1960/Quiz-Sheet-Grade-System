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

  initializeMenuItems(){
    this.items = [
      {
        label: 'Home',
        icon: 'pi pi-fw pi-home',
        routerLink: ''
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
          }
        ]
      },
    ]
  }
}

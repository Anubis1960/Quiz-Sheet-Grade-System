import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import {TokenService} from "../../services/token.service";
import {generate} from "rxjs";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  sidebarVisible: boolean = false;
  dialogVisible: boolean = false;
  generatedUrl: string = 'http://localhost:4200/student?token=';
  items: MenuItem[] = [];


  constructor(private router: Router, private tokenService: TokenService) { }

  ngOnInit() {
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
      },
      {
        label: 'Generate URL',
        icon: 'pi pi-link',
        command: () => this.generateUrl()
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

  generateUrl(){
    this.dialogVisible = true;
    let token = '';
    const user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data
    this.tokenService.generateToken({id: user.id, email: user.email}).subscribe({
      next: (data) => {
        console.log("Data:", data);
        token = data['token'];
        this.generatedUrl = 'http://localhost:4200/student?token=' + data['token'];
        console.log("URL:", this.generatedUrl);
      },
      error: (error) => {
        console.error('Error generating token:', error);
      }
    });

  }

  copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(
      () => {
        console.log('Text copied to clipboard');
      },
      (err) => {
        console.error('Error copying text: ', err);
      }
    );
  }
}

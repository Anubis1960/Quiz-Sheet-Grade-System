import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RouterOutlet } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { SplitterModule } from 'primeng/splitter';
import { FileUploadModule } from 'primeng/fileupload';
import { HttpClientModule, provideHttpClient, withFetch } from '@angular/common/http';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { SidebarModule } from 'primeng/sidebar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PanelMenuModule } from 'primeng/panelmenu';
import { CreatePaperworkComponent } from './components/create-paperwork/create-paperwork.component';
import { UploadPaperworkComponent } from './components/upload-paperwork/upload-paperwork.component';
import { BadgeModule } from 'primeng/badge';
import { CardModule } from 'primeng/card';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MessageService } from 'primeng/api';

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    SidebarComponent,
    CreatePaperworkComponent,
    UploadPaperworkComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterOutlet,
    SplitterModule,
    FileUploadModule,
    HttpClientModule,
    SidebarModule,
    BrowserAnimationsModule,
    PanelMenuModule,
    BadgeModule,
    CardModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    MessageService,
    provideClientHydration(),
    provideHttpClient(withFetch())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

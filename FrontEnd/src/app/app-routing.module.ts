import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { CreatePaperworkComponent } from './components/create-paperwork/create-paperwork.component';
import { UploadPaperworkComponent } from './components/upload-paperwork/upload-paperwork.component';
import { LoginComponent } from './components/login/login.component';
import { canActivate, canActivateToken, canActivateUrlToken } from "./quard/auth-guard";
import { RegisterComponent } from './components/register/register.component';
import { CallbackComponent } from './components/callback/callback.component';
import { StudentFormComponent } from "./components/student-form/student-form.component";

/**
 * @module AppRoutingModule
 *
 * The routing module for the application that defines all routes
 * and their corresponding components. It also protects certain routes
 * with route guards for authentication and token validation.
 *
 */
const routes: Routes = [
  { path: 'home', component: HomePageComponent, canActivate: [canActivate, canActivateToken] },
  { path: 'register', component: RegisterComponent },
  { path: 'create-paperwork', component: CreatePaperworkComponent, canActivate: [canActivate, canActivateToken] },
  { path: 'upload-paperwork', component: UploadPaperworkComponent, canActivate: [canActivate, canActivateToken] },
  { path: 'login', component: LoginComponent },
  { path: 'auth/callback', component: CallbackComponent },
  { path: 'student', component: StudentFormComponent, pathMatch: 'full', canActivate: [canActivateUrlToken] },
  { path: '', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

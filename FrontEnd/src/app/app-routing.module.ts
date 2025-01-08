import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { CreatePaperworkComponent } from './components/create-paperwork/create-paperwork.component';
import { UploadPaperworkComponent } from './components/upload-paperwork/upload-paperwork.component';

const routes: Routes = [
  {path: '', component : HomePageComponent},
  {path: 'create-paperwork', component : CreatePaperworkComponent},
  {path: 'upload-paperwork', component : UploadPaperworkComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

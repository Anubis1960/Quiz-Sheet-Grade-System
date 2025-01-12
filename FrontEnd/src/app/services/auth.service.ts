import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user-model';
import { Observable } from 'rxjs';

const BASE_URL = 'http://localhost:5000'

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http:HttpClient) { }

  login(email: string, password:string): Observable<User> {
    return this.http.post<User>(`${BASE_URL}/login`, {email, password})
  }
}

import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

const BASE_URL = 'http://localhost:5000/';

@Injectable({
    providedIn: 'root'
  })

export class StudentService {

  constructor(private http: HttpClient) {

  }

  add_student(unique_id: string, email: string):Observable<any>{
    const body = {
      unique_id: unique_id,
      email: email
    };
    return this.http.post(`${BASE_URL}/api/students/`,body);
  }
}

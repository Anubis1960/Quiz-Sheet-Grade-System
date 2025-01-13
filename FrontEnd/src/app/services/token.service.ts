import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

const BASE_URL = 'http://localhost:5000/';
@Injectable({
  providedIn: 'root'
})
export class TokenService {
  constructor(private http: HttpClient) {
  }

  validateToken(token: string): Observable<any> {
    const body = {
      token: token
    }
    return this.http.get(`${BASE_URL}/api/token/validate`, {params: body});
  }

  generateToken(params: any, exp_time = 3600): Observable<any> {
    const body = {
      params: params,
      exp_time: exp_time
    }
    return this.http.post('$BASE_URL/api/token/generate', {params: body});
  }

  getToken() {
    return localStorage.getItem('token');
  }

  getTokenFromUrl() {
    const url = window.location.href;
    return url.split('token=')[1];
  }
}

import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ActivatedRoute, ActivatedRouteSnapshot} from "@angular/router";

const BASE_URL = 'http://localhost:5000/';
@Injectable({
  providedIn: 'root'
})
export class TokenService {
  constructor(private http: HttpClient, private route: ActivatedRoute) {
  }

  validateUrlToken(token: string): Observable<any> {
    console.log(token);
    return this.http.get(`${BASE_URL}/api/token/validate_url/${token}`);
  }

  validateTeacherToken(token: string): Observable<any> {
    return this.http.get(`${BASE_URL}/api/token/validate/${token}`);
  }

  generateToken(params: any, exp_time = 3600): Observable<any> {
    const body = {
      params: params,
      exp_time: exp_time
    }
    return this.http.post(`${BASE_URL}/api/token/generate`, {params: body});
  }

  getToken() {
    return JSON.parse(sessionStorage.getItem('user') || '{}').token;
  }

}

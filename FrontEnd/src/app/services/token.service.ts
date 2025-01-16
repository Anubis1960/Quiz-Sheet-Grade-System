
import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
const BASE_URL = 'http://localhost:5000/';

/**
 * Service for handling token-related operations.
 * Provides methods for generating, validating, and retrieving tokens.
 */
@Injectable({
  providedIn: 'root'
})
export class TokenService {

  /**
   * Creates an instance of TokenService.
   * @param http - The `HttpClient` used for making HTTP requests.
   */
  constructor(private http: HttpClient) {}

  /**
   * Validates a token received in a URL.
   *
   * @param token - The token to validate from the URL.
   * @returns {Observable<any>} An Observable that returns the response from the validation API.
   *
   * @example
   * tokenService.validateUrlToken('abc123').subscribe(response => {
   *   console.log(response); // Validation response
   * });
   */
  validateUrlToken(token: string): Observable<any> {
    console.log(token);
    console.log(`${BASE_URL}/api/token/validate_url/${token}`);
    return this.http.get(`${BASE_URL}/api/token/validate_url/${token}`);
  }

  /**
   * Validates a teacher token.
   *
   * @param token - The teacher token to validate.
   * @returns {Observable<any>} An Observable that returns the response from the teacher token validation API.
   *
   * @example
   * tokenService.validateTeacherToken('teacherToken123').subscribe(response => {
   *   console.log(response); // Validation response
   * });
   */
  validateTeacherToken(token: string): Observable<any> {
    return this.http.get(`${BASE_URL}/api/token/validate/${token}`);
  }

  /**
   * Generates a new token with optional expiration time.
   *
   * @param params - The parameters used to generate the token.
   * @param exp_time - The expiration time for the token in seconds (default is 3600 seconds).
   * @returns {Observable<any>} An Observable that returns the generated token.
   *
   * @example
   * tokenService.generateToken({ user_id: 'user123' }).subscribe(response => {
   *   console.log(response); // Generated token response
   * });
   */
  generateToken(params: any, exp_time = 3600): Observable<any> {
    const body = {
      params: params,
      exp_time: exp_time
    };
    return this.http.post(`${BASE_URL}/api/token/generate`, { params: body });
  }

  /**
   * Retrieves the token stored in sessionStorage.
   *
   * @returns {string} The token stored in sessionStorage, or an empty string if not available.
   *
   * @example
   * const token = tokenService.getToken();
   * console.log(token); // Retrieved token
   */
  getToken(): string {
    return JSON.parse(sessionStorage.getItem('user') || '{}').token;
  }
}

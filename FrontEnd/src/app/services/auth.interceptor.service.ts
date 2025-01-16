import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Intercepts outgoing HTTP requests to add the Authorization header with the Bearer token.
 * This service is responsible for attaching the authentication token to requests.
 */
@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService implements HttpInterceptor {

  /**
   * Intercepts an HTTP request and adds the Authorization header if a valid token exists.
   *
   * @param request - The HTTP request that is being sent.
   * @param next - The next handler in the HTTP request pipeline.
   * @returns {Observable<HttpEvent<any>>} An Observable that resolves to the HTTP event after the request has been processed.
   *
   * @example
   * const httpRequest = new HttpRequest('GET', '/api/data');
   * authInterceptor.intercept(httpRequest, next).subscribe(response => {
   *   console.log(response);
   * });
   */
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let token = '';
    if (typeof sessionStorage !== 'undefined') {
      token = sessionStorage.getItem('access_token') || '';
    } else {
      // Handle case when sessionStorage is not available
    }

    // If a token exists, add it to the Authorization header
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    // Pass the modified request to the next handler in the chain
    return next.handle(request);
  }
}

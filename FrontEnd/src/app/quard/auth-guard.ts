import { ActivatedRouteSnapshot, Router } from "@angular/router";
import { CanActivateFn } from "@angular/router";
import { RouterStateSnapshot } from "@angular/router";
import { TokenService } from "../services/token.service";
import { inject } from "@angular/core";
import { catchError, map, of } from "rxjs";

/**
 * Route guard that checks if a user is authenticated by checking the sessionStorage.
 * If the user is not authenticated, it redirects to the login page.
 *
 * @param route - The activated route snapshot.
 * @param state - The router state snapshot.
 * @returns {boolean | RouterUrlTree} Returns `true` if the user is authenticated, otherwise redirects to the login page.
 */
export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if (typeof sessionStorage !== 'undefined') {
    const user = JSON.parse(sessionStorage.getItem("user") || '{}');
    return user.user_data !== undefined ? true : inject(Router).createUrlTree(['/login']);
  }
  else {
    return inject(Router).createUrlTree(['/login']);
  }
}

/**
 * Route guard that checks if a teacher token is valid.
 * If the token is not valid or missing, it redirects to the login page.
 *
 * @param route - The activated route snapshot.
 * @param state - The router state snapshot.
 * @returns {Observable<boolean | RouterUrlTree>} Returns `true` if the teacher token is valid, otherwise redirects to the login page.
 */
export const canActivateToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const token = inject(TokenService).getToken();
  const tokenService = inject(TokenService);
  if (token !== undefined) {
    if (token === '') {
      return inject(Router).createUrlTree(['/login']);
    }
    return tokenService.validateTeacherToken(token).pipe(
      map((data) => {
        if (data['token'] === token) {
          return true;
        }
        else {
          return inject(Router).createUrlTree(['/login']);
        }
      }),
      catchError(() => {
        return of(inject(Router).createUrlTree(['/login']));
      })
    );
  }
  else {
    return inject(Router).createUrlTree(['/login']);
  }
}

/**
 * Route guard that checks if a token in the URL query parameters is valid.
 * If the token is not valid or missing, it redirects to the login page.
 *
 * @param route - The activated route snapshot, used to access query parameters.
 * @param state - The router state snapshot.
 * @returns {Observable<boolean | RouterUrlTree>} Returns `true` if the URL token is valid, otherwise redirects to the login page.
 */
export const canActivateUrlToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const router = inject(Router);
  const tokenService = inject(TokenService);
  const token = route.queryParams['token'];
  if (token === undefined) {
    return router.createUrlTree(['/login']);
  }
  if (token === '') {
    return router.createUrlTree(['/login']);
  }
  return tokenService.validateUrlToken(token).pipe(
    map((data) => {
      if (data['token'] === token) {
        return true;
      }
      else {
        return router.createUrlTree(['/login']);
      }
    }),
    catchError(() => {
      return of(router.createUrlTree(['/login']));
    })
  );
}

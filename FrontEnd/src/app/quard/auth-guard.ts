import {ActivatedRouteSnapshot, Router} from "@angular/router";
import {CanActivateFn} from "@angular/router";
import {RouterStateSnapshot} from "@angular/router";
import {TokenService} from "../services/token.service";
import {inject} from "@angular/core";
import {catchError, map, of} from "rxjs";

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if (typeof sessionStorage !== 'undefined')
  {
    const user = JSON.parse(sessionStorage.getItem("user") || '{}');
    return user.user_data !== undefined ? true : inject(Router).createUrlTree(['/login']);
  }
  else {
    return inject(Router).createUrlTree(['/login']);
  }
}

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

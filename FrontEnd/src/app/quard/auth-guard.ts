import {ActivatedRouteSnapshot, Router} from "@angular/router";
import {CanActivateFn} from "@angular/router";
import {RouterStateSnapshot} from "@angular/router";
import {TokenService} from "../services/token.service";
import {inject} from "@angular/core";
import {catchError, map, of} from "rxjs";

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if (sessionStorage !== undefined)
  {
    return sessionStorage.getItem("user") !== null ? true : inject(Router).createUrlTree(['/login']);
  }
  return inject(Router).createUrlTree(['/login']);
}

export const canActivateToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const token = inject(TokenService).getToken();
  console.log('Token:', token);
  const tokenService = inject(TokenService);
  if (token) {
    return tokenService.validateTeacherToken(token).pipe(
      map((data) => {
        console.log('Token validated:', data);
        return true;
      }),
      catchError(() => {
        return of(inject(Router).createUrlTree(['/login']));
      })
    );
  }
  return inject(Router).createUrlTree(['/login']);
}

export const canActivateUrlToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const router = inject(Router);
  const tokenService = inject(TokenService);
  return tokenService.validateUrlToken(route).pipe(
    map(() => {
      return true;
    }),
    catchError(() => {
      return of(router.createUrlTree(['/login']));
    })
  );
}

import {ActivatedRouteSnapshot, Router} from "@angular/router";
import {CanActivateFn} from "@angular/router";
import {RouterStateSnapshot} from "@angular/router";
import {TokenService} from "../services/token.service";
import {inject} from "@angular/core";

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if (sessionStorage !== undefined)
  {
    return sessionStorage.getItem("user") !== null ? true : inject(Router).createUrlTree(['/login']);
  }
  return false;
}

export const canActivateToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const token = inject(TokenService).getToken();
  if (token) {
    inject(TokenService).validateTeacherToken(token).subscribe({
      next: () => {
        return true;
      },
      error: () => {
        return inject(Router).createUrlTree(['/login']);
      }
    });
  } else {
    return inject(Router).createUrlTree(['/login']);
  }
  return false;
}

export const canActivateUrlToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  inject(TokenService).validateUrlToken(route).subscribe({
    next: () => {
      return true;
    },
    error: () => {
        return inject(Router).createUrlTree(['/login']);
    }
  });
  return inject(Router).createUrlTree(['/login']);
}

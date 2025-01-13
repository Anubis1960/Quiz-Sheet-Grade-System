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

export const canActivateUrlToken: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  return inject(TokenService).getToken() !== null ? true: inject(Router).createUrlTree(['/login']);
}

import {ActivatedRouteSnapshot} from "@angular/router";
import {CanActivateFn} from "@angular/router";
import {RouterStateSnapshot} from "@angular/router";

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if (sessionStorage !== undefined)
  {
    return sessionStorage.getItem("user") !== null;
  }

  return false;
}

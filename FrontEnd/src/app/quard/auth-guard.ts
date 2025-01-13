import {ActivatedRouteSnapshot} from "@angular/router";
import {CanActivateFn} from "@angular/router";
import {RouterStateSnapshot} from "@angular/router";

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  //TODO implement canActivate
  return true;
}

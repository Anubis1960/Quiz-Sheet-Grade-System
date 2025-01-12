export class User{
    id: number | undefined;
    name: string | undefined;
    email: string | undefined;
    password: string | undefined;

    constructor(id: number, name: string, email: string, password: string) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.password = password;
    }
}
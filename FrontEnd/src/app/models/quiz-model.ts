import { Question } from "./question-model";

export class Quiz{
    id: string | undefined;
    title: string | undefined;
    description: string | undefined;
    questions: Question[] | undefined;

    constructor(id:string,title:string,description:string,questions:Question[]){
        this.id = id;
        this.title = title;
        this.description = description;
        this.questions = questions;
    }

    static fromJSON(json: any): Quiz {
        return new Quiz(json.id, json.title, json.description, json.questions);
    }
}

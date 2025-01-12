export class Question{
    text:string | undefined;
    options: string[] | undefined;
    correct_answers: number[] | undefined;

    constructor(text:string,options:string[], correct_answers:number[]){
        this.text = text;
        this.options = options;
        this.correct_answers = correct_answers;
    }

    static fromJSON(json: any): Question {
        return new Question(json.text, json.options, json.correct_answers);
    }
}

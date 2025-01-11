export class Question{
    text:string | undefined;
    answers: string[] | undefined;
    correct_answers: number[] | undefined;

    constructor(text:string,answers:string[], correct_answers:number[]){
        this.text = text;
        this.answers = answers;
        this.correct_answers = correct_answers;
    }
}
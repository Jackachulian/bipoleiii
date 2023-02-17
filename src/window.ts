import { ChoiceGroup } from "./choice"
import { clear, line, output } from "./display"
import { handleInput } from "./main"

/**
 * Displays stuff to the output element on the page, and handles inputs submitted to it, mainly choices.
 */
export class Window {
    // Used by the History API to go back to the previous page when back is pressed
    path: string

    constructor(path: string = "") {
        this.path = path;
    }

    /**
     * Display this to the screen.
     */
    display() {
        
    }

    /**
     * 
     * @param {string | number} text the string or number passed as an input. Choices are usually numbers, stuff like names/letters is strings 
     */
    handleInput(text: string): void {

    }
}

export class ChoiceMenu extends Window {
    choiceGroup: ChoiceGroup
    prompt: string | null

    constructor(path: string, choiceGroup: ChoiceGroup, prompt: string | null = null){
        super(path)
        this.choiceGroup = choiceGroup;
        this.prompt = prompt;
    }

    display() {
        if (this.prompt) line(this.prompt);
        this.choiceGroup.display()
    }

    handleInput(text: string): void {
        // TODO: when passed a number/character, select the corresponding choice
    }
}

export class TextInputMenu extends Window {
    prompt: string;

    constructor(path: string, prompt: string){
        super(path)
        this.prompt = prompt;
    }

    display() {
        line(this.prompt)

        let inputElement = document.createElement("input")
        inputElement.type = "text"
        output.append(inputElement)

        inputElement.onkeydown = function(event){
            if(event.key === 'Enter') {
                handleInput(inputElement.value)        
            }
        }
    }

    handleInput(text: string): void {
        alert(text);
    }
}
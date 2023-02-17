import { Choice } from "./choice.js"
import { clear, line, output } from "./display.js"
import { setWindow } from "./main.js"

/**
 * Displays stuff to the output element on the page, and handles inputs submitted to it, mainly choices.
 */
export class Window {
    constructor() {

    }

    /**
     * Display this to the screen.
     */
    display() {

    }

    /**
     * 
     * @param {string | number} input the string or number passed as an input. Choices are usually numbers, stuff like names/letters is strings 
     */
    handleInput(input) {

    }
}

export class ChoiceMenu extends Window {
    constructor(choices){
        super()
        this.choice = new Choice(choices)
    }

    display() {
        this.choice.display()
    }

    handleInput(input) {
        
    }
}

export class TextInputMenu extends Window {
    constructor(prompt){
        super()
        this.prompt = prompt;
    }

    display() {
        line(this.prompt)

        this.input = document.createElement("input")
        this.input.type = "text"
        output.append(this.input)
    }
}
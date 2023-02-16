import { Choice } from "./choice.js"
import { line } from "./display.js"
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

export class MainMenu extends ChoiceMenu {
    constructor() {
        super({
            "1": {label: "New Game", effect: () => setWindow(new NewGame())},
            "2": {label: "Load Game", effect: () => {clear(); line("Loading not implemented"); this.display()}},
        })
    }
}

export class NewGame extends Window {
    display() {
        line("Choose a name...")
    }
}
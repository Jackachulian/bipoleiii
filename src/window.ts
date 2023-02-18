import { ChoiceGroup } from "./choice"
import { clear, line, output } from "./display"
import { back, handleInput, handleTextSubmit } from "./index"

/**
 * Displays stuff to the output element on the page, and handles inputs submitted to it, mainly choices.
 */
export class Window {
    // Used by the History API to go back to the previous page when back is pressed
    id: string
    // "Notification" that can be drawn at the top of the window without redrawing everything
    toast: string | null

    constructor(id: string = "", toast: string | null = null) {
        this.id = id;
        this.toast = toast;
    }

    /**
     * Display this to the screen.
     */
    display() {
        clear()

        if (this.toast) line(this.toast)
    }

    /**
     * 
     * @param {string | number} text the string or number passed as an input. Choices are usually numbers, stuff like names/letters is strings 
     * Base behaviour: left arrow will move back in history, right arrow moves forward if possible
     * Should be called in super for all windows that can be traversed back from.
     */
    handleInput(event: KeyboardEvent): void {
        // move back in history
        if (event.key === "ArrowLeft") {
            back()
        } 
    }

    /**
     * Handle a text input field being submitted to this window.
     * @param text the text that was submitted
     */
    handleTextSubmit(text: string): void {
        alert("submitted "+text);
    }
    
    showToast(toast: string) {
        this.toast = toast;
        this.display();
    }
}

export class ChoiceMenu extends Window {
    choiceGroup: ChoiceGroup
    prompt: string | null
    selectedIndex: number

    constructor(path: string, choiceGroup: ChoiceGroup, prompt: string | null = null){
        super(path)
        this.choiceGroup = choiceGroup;
        this.prompt = prompt;
        this.selectedIndex = 0;
    }

    display() {
        super.display()
        if (this.prompt) line(this.prompt);
        this.choiceGroup.display(this.selectedIndex)
    }

    handleInput(event: KeyboardEvent): void {
        // left - go back a window (from super)
        super.handleInput(event)

        // right - select current selected cursor choice
        if (event.key === "ArrowRight" || event.key === "Enter") {
            this.choiceGroup.choices[this.selectedIndex].effect()
        }

        // up/down - move choice cursor
        if (event.key == "ArrowUp") {
            this.selectedIndex++;
            if (this.selectedIndex >= this.choiceGroup.choices.length) this.selectedIndex = 0;
            clear();
            this.display();
        }
        if (event.key == "ArrowDown") {
            this.selectedIndex--;
            if (this.selectedIndex < 0) this.selectedIndex = this.choiceGroup.choices.length-1;
            clear();
            this.display();
        }
    }
}

export class TextInputMenu extends Window {
    prompt: string;

    constructor(id: string, prompt: string){
        super(id)
        this.prompt = prompt;
    }

    display() {
        super.display()

        line(this.prompt)

        let inputElement = document.createElement("input")
        inputElement.type = "text"
        output.append(inputElement)

        inputElement.onkeydown = function(event){
            if(event.key === 'Enter') {
                handleTextSubmit(inputElement.value)      
            }
        }
    }

    handleInput(event: KeyboardEvent): void {
        super.handleInput(event)
    }

    handleTextSubmit(text: string): void {
        alert(text);
    }
}
import { button, clear, line, output, space, writeElement } from "./display"
import { back, gotoWindow, handleInput, handleTextSubmit, showCursor } from "./index"

/**
 * Displays stuff to the output element on the page, and handles inputs submitted to it, mainly choices.
 */
export class Window {
    /** Used by the History API to go back to the previous page when back is pressed */
    id: string
    /** "Notification" that can be drawn at the top of the window without redrawing everything */
    toast: HTMLElement

    constructor(id: string = "") {
        this.id = id;
        this.toast = document.createElement("div");
        this.toast.classList.add("bipole-toast")
    }

    /**
     * Display this to the screen.
     */
    display() {
        clear()
        this.displayAboveToast();
        output.append(this.toast)
        // further behaviour implemented in inheriting classes
    }

    displayAboveToast() {
        // to be overridden in subclasses
    }

    /**
     * 
     * @param {string | number} text the string or number passed as an input. Choices are usually numbers, stuff like names/letters is strings 
     * Base behaviour: left arrow will move back in history, right arrow moves forward if possible
     * Should be called in super for all windows that can be traversed back from.
     */
    handleInput(event: KeyboardEvent): void {
        // to be implemented in subclasses
    }

    /**
     * Handle a text input field being submitted to this window.
     * @param text the text that was submitted
     */
    handleTextSubmit(text: string): void {
        alert("submitted "+text);
    }
    
    showToast(toast: string) {
        this.toast.innerHTML = toast+"<br>"
    }

    /**
     * Go to another window FROM this window.
     * Has some extra functionality such as clearing current toast.
     * @param window the window to navigate to
     */
    goto(window: Window) {
        this.toast.innerHTML = ""
        gotoWindow(window)
    }
}


export class IndexedElementWindow extends Window {
    selectableElements: HTMLElement[]
    selectedIndex: number
    direction: "top-bottom" | "left-right" = "left-right"

    constructor(path: string) {
        super(path)
        this.selectedIndex = 0;
        this.selectableElements = []
    }

    display(): void {
        super.display()
        // clears any existing selectable elements (this is being redrawn)
        this.selectableElements = []
    }

    handleInput(event: KeyboardEvent): void {
        // left - go back a window (from super)
        super.handleInput(event)

        this.handleArrowKeys(event);

        // enter - select current selected cursor choice
        if (event.code === "Enter") {
            this.handleElementPressed(this.selectableElements[this.selectedIndex], this.selectedIndex)
        }
    }

    /**
     * Moves the cursor.
     * @param event keyboard event
     * @returns true if an arrow key input was handled
     */
    handleArrowKeys(event: KeyboardEvent): boolean {
        // right/left - move choice cursor
        if (event.code === (this.direction === "top-bottom" ? 'ArrowUp' : 'ArrowLeft') && this.selectedIndex > 0) {
            this.moveSelection(-1);
            return true;
        }

        if (event.code === (this.direction === "top-bottom" ? 'ArrowDown' : 'ArrowRight') && this.selectedIndex+1 < this.selectableElements.length) {
            this.moveSelection(1)
            return true;
        }

        return false;
    }

    setSelection(index: number) {
        if (this.selectableElements.length > 0) {
            this.handleElementDeselected(this.selectableElements[this.selectedIndex], this.selectedIndex)
            this.selectedIndex = index;
            this.handleElementSelected(this.selectableElements[this.selectedIndex], this.selectedIndex)
        }
    }

    moveSelection(delta: number) {
        this.setSelection(this.selectedIndex + delta)
    }

    handleElementDeselected(element: HTMLElement, index: number): void {
        document.body.focus();
        element.classList.remove("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementSelected(element: HTMLElement, index: number): void {
        element.classList.add("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementPressed(element: HTMLElement, index: number) {
        if (element.onclick) element.onclick(null);
        // further behaviour to be implemented in subclasses
    }
}

export type Choice = {
    /**
     * All inputs that will select this choice
     */
    input: string[];
    /**
     * Label displayed for this choice
     */
    label: string;
    /**
     * Effect when this choice is chosen.
     */
    effect: () => void;
}

export const universalBack: (name?: string) => Choice = (name: string = "Back") => {
    return {input: ["X", "KeyX", "KeyN"], label: name, effect: () => back()}
}

export class ChoiceMenu extends IndexedElementWindow {
    choices: Choice[]
    prompt: string | null
    

    constructor(path: string, choices: Choice[] = [], prompt: string | null = null){
        super(path)
        this.choices = choices
        this.prompt = prompt;
    }

    display() {
        super.display();
        this.displayAboveChoices();
        this.displayChoices()
        this.setSelection(0)
    }

    displayAboveChoices() {
        if (this.prompt) line(this.prompt);
    }

    displayChoices() {
        let listElement = document.createElement("div")
        listElement.classList.add("ascii")

        for (let i = 0; i < this.choices.length; i++) {
            const choice = this.choices[i];
            let buttonElem = button(`[${choice.input[0]}] ${choice.label}`, () => choice.effect())
            output.append(buttonElem)
            this.selectableElements.push(buttonElem)
        }

        output.append(listElement)
    }

    addChoice(choice: Choice) {
        this.choices.push(choice)
    }

    handleInput(event: KeyboardEvent): void {
        super.handleInput(event);
        for (let choice of this.choices) {
            for (let inputCode of choice.input) {
                if (event.code === inputCode || event.key === inputCode) {
                    choice.effect();
                    return;
                }
            }
        }
    }
}

export class TextInputMenu extends ChoiceMenu {
    prompt: string;
    inputElem: HTMLInputElement
    maxlength: number = 24;

    constructor(id: string, prompt: string){
        super(id)
        this.prompt = prompt;
    }

    displayAboveChoices() {
        super.displayAboveChoices();
        this.displayTextInput();
    }

    displayTextInput() {
        let promptElem = document.createElement("div");
        output.append(promptElem)
        this.selectableElements.push(promptElem)
        promptElem.classList.add("bipole-prompt");

        let pointerElem = document.createElement("span");
        promptElem.append(pointerElem);
        pointerElem.classList.add("bipole-pointer");
        pointerElem.innerHTML = "> "

        this.inputElem = document.createElement("input");
        promptElem.append(this.inputElem);
        this.inputElem.type = "text"
        this.inputElem.placeholder = "Lead"
        this.inputElem.classList.add("bipole-prompt-input");

        let thisWindow = this;

        let ie = this.inputElem;

        // select this input whenever clicked/focused
        this.inputElem.onclick = () => thisWindow.setSelection(0);
        this.inputElem.onfocus = () => thisWindow.setSelection(0);

        // handles key inputs differently
        this.inputElem.onkeydown = (ev) => {
            // if arrow keys, send info to indexedelementmenu side, blur if navigated off via arrows
            if (thisWindow.handleArrowKeys(ev)) ie.blur();

            // submit input value as text on enter
            if (ev.code === 'Enter') {
                handleTextSubmit(ie.value)    
            }

            // set error color when text is too long (for some reason only works when run afer timeout)
            setTimeout(() => {
                if (ie.value.length > this.maxlength) {
                    ie.classList.add("bipole-error")
                } else {
                    ie.classList.remove("bipole-error")
                }
            }, 0)
        }
    }

    handleInput(event: KeyboardEvent): void {
        super.handleInput(event)
    }

    handleElementSelected(element: HTMLElement, index: number): void {
        super.handleElementSelected(element, index)
        // If the text box was selected, place cursor in it
        if (index === 0){
            // because browser is being quirky, adding, a timeout here to wait for other events
            setTimeout(() => this.inputElem.focus(), 0)
        }
    }
}
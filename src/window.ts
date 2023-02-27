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
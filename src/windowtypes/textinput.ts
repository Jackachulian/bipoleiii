import { ChoiceMenu } from "./choice";

export class TextInputMenu extends ChoiceMenu {
    prompt: string;
    inputElem: HTMLInputElement
    maxlength: number = 24;

    constructor(prompt: string){
        super()
        this.prompt = prompt;
    }

    displayAboveChoices(out: HTMLElement) {
        super.displayAboveChoices(out);
        this.displayTextInput(out);
    }

    displayTextInput(out: HTMLElement) {
        let promptElem = document.createElement("div");
        out.append(promptElem)
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
                this.handleTextSubmit(ie.value)    
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
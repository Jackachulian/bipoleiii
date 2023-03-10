import { ChoiceMenu } from "./choice";
import { Menu } from "./menu";
import { SelectEvent, TraversableMenu } from "./traversablemenu";

export class TextInputMenu extends Menu {
    inputElem: HTMLInputElement

    maxlength: number = 24;

    constructor(){
        super()

        let promptElem = document.createElement("div");
        promptElem.classList.add("bipole-prompt");
        this.element.append(promptElem)

        let pointerElem = document.createElement("span");
        promptElem.append(pointerElem);
        pointerElem.classList.add("bipole-pointer");
        pointerElem.innerHTML = "> "

        this.inputElem = document.createElement("input");
        promptElem.append(this.inputElem);
        this.inputElem.type = "text"
        this.inputElem.placeholder = "Lead"
        this.inputElem.classList.add("bipole-prompt-input");

        this.inputElem.onkeydown = (ev) => {
            // submit input value as text on enter
            if (ev.code === 'Enter') {
                this.handleTextSubmit(this.inputElem.value) 
            }

            // set error color when text is too long (for some reason only works when run afer timeout)
            setTimeout(() => {
                if (this.inputElem.value.length > this.maxlength) {
                    this.inputElem.classList.add("bipole-error")
                } else {
                    this.inputElem.classList.remove("bipole-error")
                }
            }, 0)
        }
    }

    onDeselected(): void {
        this.inputElem.blur()
    }

    handleTextSubmit(text: string) {
        console.log(text)
    }
}
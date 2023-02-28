import { button, line } from "../display";
import { back } from "../index";
import { IndexedElementWindow } from "./indexedelement";

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
    

    constructor(choices: Choice[] = [], prompt: string | null = null){
        super()
        this.choices = choices
        this.prompt = prompt;
    }

    display(out: HTMLElement) {
        super.display(out);
        this.displayAboveChoices(out);
        this.displayChoices(out)
        this.setSelection(0)
    }

    displayAboveChoices(out: HTMLElement) {
        if (this.prompt) line(this.prompt, out);
    }

    displayChoices(out: HTMLElement) {
        let listElement = document.createElement("div")
        listElement.classList.add("ascii")

        for (let i = 0; i < this.choices.length; i++) {
            const choice = this.choices[i];
            let buttonElem = button(`[${choice.input[0]}] ${choice.label}`, () => choice.effect())
            out.append(buttonElem)
            this.selectableElements.push(buttonElem)
        }

        out.append(listElement)
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
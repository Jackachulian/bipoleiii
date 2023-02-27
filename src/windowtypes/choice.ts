import { button, line, output } from "../display";
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
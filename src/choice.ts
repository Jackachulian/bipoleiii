import { output } from "./display";
import { showCursor } from "./index";

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

/**
 * Stores some choices that can be given to the player
 */
export class ChoiceGroup {
    choices: Choice[]

    /**
     * 
     * @param {Choice[]} choices should be an object of key-value pairs.
     * Key is input. Value is an object; label is what is displayed, effect is what is run when selected
     */
    constructor(choices: Choice[]) {
        this.choices = choices;
    }

    /**
     * Writes this as a list element to output.
     */
    display(selectedIndex: number) {
        let dl = document.createElement("dl")
        for (let i = 0; i < this.choices.length; i++) {
            const choice = this.choices[i];
            let dt = document.createElement("dt")
            dt.onclick = () => choice.effect()

            if (showCursor && i === selectedIndex)
            {
                dt.innerHTML = `<b>> [${i+1}] ${choice.label}</b>`
            } else {
                dt.innerHTML = `&nbsp;&nbsp;[${i+1}] ${choice.label}`
            }

            dl.append(dt)
        }
        output.append(dl)
    }
}
import { output } from "./display.js";

/**
 * Stores some choices that can be given to the player
 */
export class Choice {
    /**
     * 
     * @param {*} choices should be an object of key-value pairs.
     * Key is input. Value is an object; label is what is displayed, effect is what is run when selected
     */
    constructor(choices) {
        this.choices = choices;
    }

    /**
     * Writes this as a list element to output.
     */
    display() {
        let dl = document.createElement("dl")
        for (const prop in this.choices) {
            let dt = document.createElement("dt")
            dt.onclick = () => this.choices[prop].effect()
            dt.innerHTML = `[${prop}] ${this.choices[prop].label}`
            dl.append(dt)
        }
        output.append(dl)
    }
}
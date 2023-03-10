import { TraversableMenu, Menu } from "./menu";
import { createButton } from "./elements";

export type Choice = {
    /** Input displayed for this choice that will select it */
    input: string

    /** List of alias that also select this choice */
    aliases: string[];
    
    /** Label dislayed for this choice */
    label: string;
    
    /** Effect when this choice is chosen. */
    effect: () => void;
}


export class ChoiceMenu extends TraversableMenu {
    selectable: boolean = true;

    /** All choices this window displays as buttons. */
    choices: Choice[]

    constructor(choices: Choice[], boxInput: boolean = true) {
        super()
        this.choices = choices
        for (let choice of this.choices) {
            let choiceMenuItem = new ChoiceMenuItem(choice, boxInput);
            this.children.push(choiceMenuItem)
        }
    }
}

export class ChoiceMenuItem extends Menu {
    selectable: boolean = true;

    constructor(choice: Choice, boxInput: boolean) {
        let buttonElement;
        if (boxInput){
            buttonElement = createButton(`[${choice.input}] ${choice.label}`, choice.effect);
        } else {
            buttonElement = createButton(`<u>${choice.label.charAt(0)}</u>${choice.label.substring(1)}`, choice.effect);
        }
        super(buttonElement)
    }
}
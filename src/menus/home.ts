import { ChoiceMenu } from "../windowtypes/choice";

export class HomeMenu extends ChoiceMenu {
    constructor() {
        super("", [
            {input: ["1", "A", "M"], label: "Map", effect: () => {}},
            {input: ["2", "S", "I"], label: "Inventory", effect: () => {}},
            {input: ["3", "D"], label: "Deck", effect: () => {}},
        ], 'Home')
    }
}
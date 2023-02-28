import { gotoWindow } from "../index";
import { ChoiceMenu } from "../windowtypes/choice";
import { CardWindow } from "../windowtypes/cardwindow";
import { DeckMenu } from "./deck";

export class HomeMenu extends ChoiceMenu {
    constructor() {
        super([
            {input: ["1", "A", "M"], label: "Map", effect: () => {}},
            {input: ["2", "S", "I"], label: "Inventory", effect: () => {}},
            {input: ["3", "D"], label: "Deck", effect: () => gotoWindow(new DeckMenu())},
        ], 'Home')
    }
}
import { ChoiceMenu } from "./window";

export class HomeMenu extends ChoiceMenu {
    constructor() {
        super("", [
            {input: ["1"], label: "Map", effect: () => {}},
            {input: ["2"], label: "Items", effect: () => {}}
        ], 'Home')
    }
}
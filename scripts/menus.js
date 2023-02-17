import { setWindow } from "./main.js"
import { clear, line } from "./display.js"
import { ChoiceMenu, TextInputMenu } from "./window.js";

// Main Menu. the landing page for the game
export class MainMenu extends ChoiceMenu {
    constructor() {
        super({
            "1": {label: "New Game", effect: () => setWindow(new NewGame())},
            "2": {label: "Load Game", effect: () => {clear(); line("Loading not implemented"); this.display()}},
        })
    }
}

export class NewGame extends TextInputMenu {
    constructor() {
        super("Choose a name...")
    }
}
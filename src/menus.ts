import { back, gotoWindow } from "./index"
import { clear, line } from "./display"
import { ChoiceMenu, TextInputMenu } from "./window";
import { ChoiceGroup } from "./choice";

// Main Menu. the landing page for the game
export class MainMenu extends ChoiceMenu {
    constructor() {
        super("", new ChoiceGroup([
            {input: ["1"], label: "New Game", effect: () => gotoWindow(new NewGame())},
            {input: ["2"], label: "Load Game", effect: () => this.showToast("Loading not implemented")}
        ]), "Conspiracy of the Mechanical Entity")
    }
}

export class NewGame extends TextInputMenu {
    constructor() {
        super("newgame", "Choose a name..")
    }

    handleTextSubmit(text: string): void {
        gotoWindow(new NameConfirm(text));
    }
}

export class NameConfirm extends ChoiceMenu {
    selectedName: string

    constructor(selectedName: string) {

        super("newgame/confirm", new ChoiceGroup([
            {input: ["yes", "y", "1"], label: "Yes", effect: () => this.showToast("Game no happen... ;/")},
            {input: ["no", "n", "2"], label: "No", effect: () => back()}
        ]), `Are you sure you want to be named ${selectedName}?`)

        this.selectedName = selectedName;
    }
}
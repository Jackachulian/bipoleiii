import { setWindow } from "./main"
import { clear, line } from "./display"
import { ChoiceMenu, TextInputMenu } from "./window";
import { ChoiceGroup } from "./choice";

// Main Menu. the landing page for the game
export class MainMenu extends ChoiceMenu {
    constructor() {
        super("", new ChoiceGroup([
            {input: ["1"], label: "New Game", effect: () => setWindow(new NewGame())},
            {input: ["2"], label: "Load Game", effect: () => {clear(); line("Loading not implemented"); this.display()}}
        ]), "Conspiracy of the Mechanical Entity")
    }
}

export class NewGame extends TextInputMenu {
    constructor() {
        super("newgame", "Choose a name..")
    }

    handleInput(text: string): void {
        setWindow(new NameConfirm(text));
    }
}

export class NameConfirm extends ChoiceMenu {
    selectedName: string

    constructor(selectedName: string) {
        super("newgame/confirm", new ChoiceGroup([
            {input: ["yes", "y", "1"], label: "Yes", effect: () => {clear(); line("Not implemented... :/"); this.display()}},
            {input: ["no", "n", "2"], label: "No", effect: () => setWindow(new NewGame())}
        ]), `Are you sure you want to be named ${selectedName}?`)
        this.selectedName = selectedName;
    }
}
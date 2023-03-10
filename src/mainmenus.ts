import { createElement } from "./elements"
import { ChoiceMenu } from "./choice"
import { TextInputMenu } from "./textinput"
import { showMenu } from "./index"
import { TraversableMenu } from "./traversablemenu"

export class MainMenu extends ChoiceMenu {
    constructor() {
        super([
            {input: "1", aliases: [], label: "New Game", effect: () => {showMenu(new NameEntryMenu())}},
            {input: "2", aliases: [], label: "Load Game", effect: () => {this.showToast("load game")}},
        ])

        this.element.prepend(createElement("h1", "BIPOLE III"))

        this.toast = document.createElement("p")
        this.element.append(this.toast)
    }
}

export class NameEntryMenu extends TraversableMenu {
    direction: "row" | "column" = "column";

    constructor() {
        super()

        this
        this.element.append(createElement("p", "Enter a name"))

        let nameEntryMenu = new TextInputMenu()
        this.children.push(nameEntryMenu)

        let confirmWindow = new ChoiceMenu([
            {input: "1", aliases: [], label: "Confirm", effect: () => {this.showToast("submitted name!")}},
            {input: "2", aliases: [], label: "Back", effect: () => {this.showToast("goin back")}}
        ])
        confirmWindow.direction = "column"
        this.children.push(confirmWindow)
    }
}
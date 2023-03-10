import { Menu } from "./menu";
import { createElement } from "./elements"
import { ChoiceMenu } from "./choice"

export class MainMenu extends ChoiceMenu {
    constructor() {
        super([
            {input: "1", aliases: [], label: "New Game", effect: () => {this.showToast("new game")}},
            {input: "2", aliases: [], label: "Load Game", effect: () => {this.showToast("load game")}},
        ])

        this.element.prepend(createElement("h1", "BIPOLE III"))

        this.toast = document.createElement("p")
        this.element.append(this.toast)
    }
}
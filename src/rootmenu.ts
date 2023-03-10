import { Menu } from "./menu"
import { ChoiceMenu } from "./choice"
import { OverflowRule, TraversableMenu } from "./traversablemenu"

export class NavMenu extends ChoiceMenu {
    linkEnd = false

    constructor() {
        super([
            {input: "M", aliases: [], label: "Map", effect: () => {this.showToast("map")}},
            {input: "I", aliases: [], label: "Inventory", effect: () => {this.showToast("inventory")}},
            {input: "D", aliases: [], label: "Deck", effect: () => {this.showToast("deck")}},
            {input: "B", aliases: [], label: "Battle", effect: () => {this.showToast("battle")}},
        ], false)
        this.element.classList.add("terminal-menu", "bipole-nav-menu")

        this.toast = document.getElementById("navtoast")
    }
}

export class OutputMenu extends TraversableMenu {
    linkStart = false

    startOverflow: "row" | "column" | "none" = "column"

    constructor() {
        super()
        this.children = [null] // this one empty child will be replaced by currently shown menu when the game starts
    }

    setMenu(menu: Menu) {
        this.children[0] = menu;
    }

    displayedMenu(): Menu {
        return this.children[0]
    }
}

export class RootMenu extends TraversableMenu {
    /** Nav menu which is always present and isn't modified */
    nav: NavMenu

    /** Output window which changes when entering a new window */
    out: OutputMenu

    /** Output element where out menu should display to */
    outElement: HTMLElement

    direction: "row" | "column" = "column";

    constructor() {
        super(document.body)

        this.outElement = document.getElementById("output")
        
        this.nav = new NavMenu()
        this.children.push(this.nav)
        
        this.out = new OutputMenu()
        this.children.push(this.out);
        
        this.nav.display(document.getElementById("nav"))

        let rule: OverflowRule = {direction: "column", first: this.nav, last: this.out}
        this.nav.addOverflow(rule)
        this.out.addOverflow(rule)
    }

    showMenu(menu: Menu) {
        this.clear();

        this.out.setMenu(menu)

        menu.display(this.outElement);

        if (menu instanceof TraversableMenu) {
            this.setSelection(1);
            menu.setSelection(0)
        }

        menu.postDisplay(this.outElement)
    }

    clear() {
        this.outElement.innerHTML = ""
    }
}
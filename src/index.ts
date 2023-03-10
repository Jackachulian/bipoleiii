import { MainMenu } from "./mainmenus"
import { Menu } from "./menu";
import { SelectEvent, TraversableMenu } from "./traversablemenu"
import { NavMenu, RootMenu } from "./rootmenu" 

// listens for keypresses on the document body
document.body.onkeydown = function (event) {
    console.log(event)
    // If the user is focused on another input, ignore key presses
    if (event.target != document.body) {
        return
    }

    // ==== DEBUG
    // Prints window path
    if (event.code === "Slash") {
        let menu: Menu = rootMenu;
        let logString = ""
        while (menu) {
            logString += (" > "+menu.constructor.name)
            if (menu instanceof TraversableMenu) {
                logString += "["+menu.index+"]"
                menu = menu.selectedElement().menu
            } else {
                menu = null
            }
        }
        console.log(logString)
    }

    else if (event.code === "Period") {
        console.log(selectIndexes)
    }

    rootMenu.handleInput(event)
    rootMenu.handleCursorMovement(event)
};

// Always updated to be the currently selected element (parent of innermost & event of selection)
export let currentSelectionParent: TraversableMenu = null
export let currentSelection: SelectEvent = null
export let selectIndexes: number[] = []
export function setCurrentSelection(parent: TraversableMenu, ev: SelectEvent) {
    currentSelectionParent = parent
    currentSelection = ev;
    selectIndexes = []
    let menu: Menu = rootMenu;
    while (menu instanceof TraversableMenu) {
        selectIndexes.push(menu.index)
        menu = menu.selectedElement().menu
    }
}

// Root menu that is always present that holds the navigation bar and the current window
let rootMenu = new RootMenu();

export function showMenu(menu: Menu) {
    rootMenu.showMenu(menu)
}

// Starting window given to the player
let mainMenu = new MainMenu();

// display the starting menu to the user
rootMenu.showMenu(mainMenu)
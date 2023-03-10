import { MainMenu } from "./mainmenus"
import { Menu, TraversableMenu } from "./menu";
import { NavMenu, RootMenu } from "./rootmenu" 

console.log("Hello World!");

let rootMenu = new RootMenu();

let mainMenu = new MainMenu();


rootMenu.showMenu(mainMenu)

// listens for keypresses on the document body
document.body.onkeydown = function (event) {
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
            if (menu instanceof TraversableMenu) {
                logString += (" > "+menu.constructor.name)
                menu = menu.selectedElement().menu
            } else {
                menu = null
            }
        }
        console.log(logString)
    }

    rootMenu.handleInput(event)
};
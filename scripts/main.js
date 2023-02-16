import { Choice } from "./choice.js";
import { clear, line, output } from "./display.js";
import { MainMenu, Window } from "./window.js";

/** Stores the current window. */
var currentWindow = null

/**
 * 
 * @param {Window} window the window to set & display
 */
export function setWindow(window) {
    currentWindow = window;
    clear();
    currentWindow.display();
}

export function handleInput(input) {
    currentWindow.handleInput(input)
}

const mainMenu = new MainMenu()
setWindow(mainMenu)
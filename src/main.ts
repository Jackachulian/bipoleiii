import { clear, line, output } from "./display";
import { MainMenu } from "./menus";
import { Window } from "./window";

/** Stores the current window. */
var currentWindow: Window = new MainMenu()
setWindow(currentWindow)

/**
 * 
 * @param {Window} window the window to set & display
 */
export function setWindow(window) {
    currentWindow = window;
    clear();
    history.pushState(null, '', window.path)
    currentWindow.display();
}

export function handleInput(input) {
    currentWindow.handleInput(input)
}


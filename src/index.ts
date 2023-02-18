import { clear, line, output } from "./display";
import { MainMenu } from "./menus";
import { Window } from "./window";

/** Stores the current window path. */
const windows: Window[] = [new MainMenu()]

export let showCursor: boolean = true;

export function currentWindow(): Window {
    return windows[windows.length - 1];
}

/**
 * Clears window history back to a certain index
 * @param index the index to stop at (exclusive)
 */
export function clearHistoryTo(index: number)
{
    while (windows.length > index+1) windows.pop();
}

/**
 * 
 * @param {Window} window the window to set & display
 */
export function gotoWindow(window: Window) {
    // store current window and add to window stack
    windows.push(window)
    window.display();
    console.log(windows)
}

/**
 * Move back one step in the window history.
 */
export function back() {
    windows.pop()
    currentWindow().display()
    console.log(windows)
}

export function handleInput(event: KeyboardEvent) {
    currentWindow().handleInput(event)
}

export function handleTextSubmit(text: string) {
    currentWindow().handleTextSubmit(text)
}

// listens for keypresses on the document body
document.body.onkeydown = function (event) {
    // If the user is focused on another input, ignore key presses
    if (event.target != document.body) {
        return
    }

    currentWindow().handleInput(event)
};

windows[0].display();
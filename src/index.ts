import { CutsceneWindow } from "./cutscene";
import { clear, line, output } from "./display";
import { HomeMenu } from "./homemenus";
import { MainMenu } from "./mainmenus";
import { Window } from "./window";

/** Stores the current window path. */
let rootWindow: Window = new MainMenu();
// let rootWindow: Window = new CutsceneWindow("test", new HomeMenu());

const windows: Window[] = [rootWindow]

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
}

/**
 * Move back one step in the window history.
 */
export function back() {
    if (windows.length<=1) return; // do not exit outermost window
    windows.pop()
    currentWindow().display()
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
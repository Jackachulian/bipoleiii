import { clear, root } from "./display";
import { HomeMenu } from "./menus/home";
import { TitleScreen } from "./menus/title";
import { newSave } from "./save";
import { loadSave } from "./user";
import { Window } from "./window";

loadSave(newSave("Lead"))

/** Stores the current window path. */
// let rootWindow: Window = new TitleScreen();
// let rootWindow: Window = new CutsceneWindow("test", new HomeMenu());
let rootWindow: Window = new HomeMenu();

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
    clear(root)
    // store current window and add to window stack
    windows.push(window)
    window.display(root);
}

export function refresh() {
    clear(root)
    currentWindow().display(root);
}

/**
 * Move back one step in the window history.
 */
export function back() {
    if (windows.length<=1) return; // do not exit outermost window
    windows.pop()
    currentWindow().display(root)
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

windows[0].display(root);
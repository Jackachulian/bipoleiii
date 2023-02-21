/** The main element where output is written to. */
export const output: HTMLElement = document.getElementById("output") || document.body;

export function clear()
{
    output.textContent = ''
}

/**
 * Append an element to output.
 * @param {string} text text to put in the element
 * @param {string} element element tag
 */
export function writeElement(text: string, element: string) {
    let p = document.createElement(element);
    p.innerHTML = text;
    output.append(p);
}

export function addElement(elem: string | Node) {
    output.append(elem)
}

/** 
 * Add a paragraph to the output witht he given text.
 * @param {string} text 
 */
export function line(text: string): HTMLElement {
    let span = document.createElement("span")
    span.classList.add("bipole-line", "ascii")
    span.innerHTML = text
    output.append(span)
    return span;
}

/** Add a line break. */
export function space() {
    output.append(document.createElement("br"))
}

/**
 * 
 * @param {string} text 
 */
export function header(text: string) {
    writeElement(text, "h1")
}

/**
 * Append a button with the given effect to the screen.
 * @param onclick the effect that happens when the button is used 
 */
export function button(text: string, onclick: () => void): HTMLElement {
    let button = document.createElement("button");
    button.innerHTML = text;
    button.classList.add("btn", "btn-ghost")
    button.onclick = onclick
    output.append(button)
    return button
}
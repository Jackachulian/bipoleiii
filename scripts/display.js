/** The main element where output is written to. */
export const output = document.getElementById("output");

export function clear()
{
    output.textContent = ''
}

/**
 * Append an element to output.
 * @param {string} text text to put in the element
 * @param {string} element element tag
 */
function write(text, element) {
    let p = document.createElement(element);
    p.innerHTML = text;
    output.append(p);
}

/** 
 * Add a paragraph to the output witht he given text.
 * @param {string} text 
 */
export function line(text) {
    write(text, "p")
}

/**
 * 
 * @param {string} text 
 */
export function header(text) {
    write(text, "h1")
}
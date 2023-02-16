/** The main element where output is written to. */
const output = document.getElementById("output");

/**
 * Append an element to output.
 * @param {string} text text to put in the element
 * @param {string} element element tag
 */
function addElement(text, element)
{
    let p = document.createElement(element);
    p.innerHTML = text;
    output.append(p);
}

/** 
 * Add a paragraph to the output witht he given text.
 * @param {string} text 
 */
export function line(text) {
    addElement(text, "p")
}

/**
 * 
 * @param {*} text 
 */
export function header(text) {
    addElement(text, "h1")
}
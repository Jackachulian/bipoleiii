export function createButton(text: string, effect: () => void): HTMLButtonElement {
    let element = document.createElement("button")
    element.innerHTML = text;
    element.onclick = effect
    return element;
}

export function createElement(tag: string = "div", innerHTML: string = "") {
    let element = document.createElement(tag)
    element.innerHTML = innerHTML;
    return element;
}
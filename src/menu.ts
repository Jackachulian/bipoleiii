

/** Menu - can be interacted with by the user and traversed between with other windows. */
export class Menu {
    /** The root element for this window. Should be created in constructor */
    element: HTMLElement

    /** If the cursor can be moved to this element. */
    selectable: boolean = false

    /** If this menu is selected. */
    selected: boolean = false;

    /** Current toast on this element if it exists (notification that appears at the start) */
    toast: HTMLElement | null = null;

    constructor(element: HTMLElement | null = null) {
        if (!element) element = document.createElement("div");
        this.element = element;
    }

    /** Appends this menu's element to the passed element. */
    display(out: HTMLElement) {
        out.appendChild(this.element)
    }

    /** Code to be run after all displays are done */
    postDisplay(out: HTMLElement) {
        // behaviour to be overridden in subclasses
    }

    /** Behaviour when a key is pressed while this is selected. */
    handleInput(event: KeyboardEvent) {
        
    }

    /** Display a message to the toast element on this menu (and create it if it doesn't exist) */
    showToast(text: string) {
        if (!this.toast) {
            this.toast = document.createElement("p")
            this.element.prepend(this.toast)
        }
        this.toast.innerHTML = text;
    }

    /** Effect when THIS menu is deselected. */
    onDeselected() {
        // to be defined in subclasses
    }
}
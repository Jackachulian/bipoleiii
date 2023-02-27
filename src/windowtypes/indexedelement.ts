import { Window } from "../window";

export class IndexedElementWindow extends Window {
    selectableElements: HTMLElement[]
    selectedIndex: number
    direction: "top-bottom" | "left-right" = "left-right"

    constructor(path: string) {
        super(path)
        this.selectedIndex = 0;
        this.selectableElements = []
    }

    display(): void {
        super.display()
        // clears any existing selectable elements (this is being redrawn)
        this.selectableElements = []
    }

    handleInput(event: KeyboardEvent): void {
        // left - go back a window (from super)
        super.handleInput(event)

        this.handleArrowKeys(event);

        // enter - select current selected cursor choice
        if (event.code === "Enter") {
            this.handleElementPressed(this.selectableElements[this.selectedIndex], this.selectedIndex)
        }
    }

    /**
     * Moves the cursor.
     * @param event keyboard event
     * @returns true if an arrow key input was handled
     */
    handleArrowKeys(event: KeyboardEvent): boolean {
        // right/left - move choice cursor
        if (event.code === (this.direction === "top-bottom" ? 'ArrowUp' : 'ArrowLeft') && this.selectedIndex > 0) {
            this.moveSelection(-1);
            return true;
        }

        if (event.code === (this.direction === "top-bottom" ? 'ArrowDown' : 'ArrowRight') && this.selectedIndex+1 < this.selectableElements.length) {
            this.moveSelection(1)
            return true;
        }

        return false;
    }

    setSelection(index: number) {
        if (this.selectableElements.length > 0) {
            this.handleElementDeselected(this.selectableElements[this.selectedIndex], this.selectedIndex)
            this.selectedIndex = index;
            this.handleElementSelected(this.selectableElements[this.selectedIndex], this.selectedIndex)
        }
    }

    moveSelection(delta: number) {
        this.setSelection(this.selectedIndex + delta)
    }

    handleElementDeselected(element: HTMLElement, index: number): void {
        document.body.focus();
        element.classList.remove("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementSelected(element: HTMLElement, index: number): void {
        element.classList.add("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementPressed(element: HTMLElement, index: number) {
        if (element.onclick) element.onclick(null);
        // further behaviour to be implemented in subclasses
    }
}
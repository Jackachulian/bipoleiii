import { Window } from "../window";

export class GridElementWindow extends Window {
    selectableElements: HTMLElement[][]
    selectedRow: number
    selectedCol: number

    constructor() {
        super()
        this.selectedRow = 0;
        this.selectedCol = 0;
        this.selectableElements = []
    }

    display(out: HTMLElement): void {
        super.display(out)
        // clears any existing selectable elements (this is being redrawn)
        this.selectableElements = []
    }

    handleInput(event: KeyboardEvent): void {
        // left - go back a window (from super)
        super.handleInput(event)

        this.handleArrowKeys(event);

        // enter - select current selected cursor choice
        if (event.code === "Enter") {
            this.handleElementPressed(this.selectableElements[this.selectedRow][this.selectedCol], this.selectedRow, this.selectedCol)
        }
    }

    /**
     * Moves the cursor.
     * @param event keyboard event
     * @returns true if an arrow key input was handled
     */
    handleArrowKeys(event: KeyboardEvent): boolean {
        if (event.code === 'ArrowUp') {
            if (this.selectedRow <= 0) return this.handleCursorOverflow(-1, 0)
            else this.moveSelection(-1, 0);
        }

        else if (event.code === 'ArrowDown') {
            if (this.selectedRow+1 >= this.selectableElements.length) return this.handleCursorOverflow(1, 0)
            else this.moveSelection(1, 0);
        }

        else if (event.code === 'ArrowLeft') {
            if (this.selectedCol <= 0) return this.handleCursorOverflow(0, -1);
            else this.moveSelection(0, -1);
        }

        else if (event.code === 'ArrowRight') {
            if (this.selectedCol+1 >= this.selectableElements[this.selectedRow].length) return this.handleCursorOverflow(0, 1)
            else this.moveSelection(0, 1);
        }

        else {
            return false;
        }

        return true;
    }

    /** Handles what happens when cursor exits bounds. Default behaviour: nothing, cursor doesn't move
     * @returns true if overflow was handled with something other than not moving the cursor
     */
    handleCursorOverflow(rowDelta: number, colDelta: number): boolean {
        return false;
    }

    /** returns true if the index exists. */
    setSelection(row: number, col: number): boolean {
        if (this.selectableElements.length <= 0 && this.selectableElements[0].length <= 0) return false;

        if (row >= this.selectableElements.length) {
            row = this.selectableElements.length - 1;
            col = this.selectableElements[row].length - 1;
        }

        if (this.selectableElements.length > 0 && this.selectableElements[this.selectedRow].length > 0) {
            this.handleElementDeselected(this.selectedElement(), this.selectedRow, this.selectedCol)
            this.selectedRow = row;
            this.selectedCol = col;

            // bump cursor back if outside of row
            if (this.selectedCol >= this.selectableElements[this.selectedRow].length) {
                this.selectedCol = this.selectableElements[this.selectedRow].length - 1;
            }
            this.handleElementSelected(this.selectedElement(), this.selectedRow, this.selectedCol)
            return true;
        }
        return false;
    }

    removeSelection() {
        this.handleElementDeselected(this.selectedElement(), this.selectedRow, this.selectedCol)
    }

    selectedElement(): HTMLElement {
        return this.selectableElements[this.selectedRow][this.selectedCol]
    }

    moveSelection(rowDelta: number, colDelta: number) {
        this.setSelection(this.selectedRow + rowDelta, this.selectedCol + colDelta)
    }

    handleElementDeselected(element: HTMLElement, row: number, col: number): void {
        document.body.focus();
        element.classList.remove("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementSelected(element: HTMLElement, row: number, col: number): void {
        element.focus();
        element.classList.add("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementPressed(element: HTMLElement, row: number, col: number) {
        if (element.onclick) element.onclick(null);
        // further behaviour to be implemented in subclasses
    }
}
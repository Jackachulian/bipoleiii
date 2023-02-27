import { Window } from "../window";

export class IndexedElementWindow extends Window {
    selectableElements: HTMLElement[][]
    selectedRow: number
    selectedCol: number

    constructor(path: string) {
        super(path)
        this.selectedRow = 0;
        this.selectedCol = 0;
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
            this.handleElementPressed(this.selectableElements[this.selectedRow][this.selectedCol], this.selectedRow, this.selectedCol)
        }
    }

    /**
     * Moves the cursor.
     * @param event keyboard event
     * @returns true if an arrow key input was handled
     */
    handleArrowKeys(event: KeyboardEvent): boolean {
        if (event.code === 'ArrowUp' && this.selectedRow > 0) {
            this.moveSelection(-1, 0);
        }

        else if (event.code === 'ArrowDown' && this.selectedRow+1 < this.selectableElements.length) {
            this.moveSelection(1, 0);
        }

        else if (event.code === 'ArrowLeft' && this.selectedCol > 0) {
            this.moveSelection(0, -1);
        }

        else if (event.code === 'ArrowRight' && this.selectedCol+1 < this.selectableElements[this.selectedRow].length) {
            this.moveSelection(0, 1);
        }

        else {
            return false;
        }

        return true;
    }

    setSelection(row: number, col: number) {
        if (this.selectableElements.length > 0) {
            this.handleElementDeselected(this.selectedElement(), this.selectedRow, this.selectedCol)
            this.selectedRow = row;
            this.selectedCol = col;
            if (this.selectedCol >= this.selectableElements[this.selectedRow].length) {
                this.selectedCol = this.selectableElements[this.selectedRow].length - 1;
            }
            this.handleElementSelected(this.selectedElement(), this.selectedRow, this.selectedCol)
        }
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
        element.classList.add("bipole-cursor")
        // further behaviour to be implemented in subclasses
    }

    handleElementPressed(element: HTMLElement, row: number, col: number) {
        if (element.onclick) element.onclick(null);
        // further behaviour to be implemented in subclasses
    }
}
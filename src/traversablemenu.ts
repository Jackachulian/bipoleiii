import { currentSelectionParent, setCurrentSelection } from "./index"
import { Menu } from "./menu"

/** A menu that stores selectable sub-menus within it. */
export class TraversableMenu extends Menu {
    /** Child menus/selectable items of this in a grid. Drawn child menu elements within this menu's element. */
    children: Menu[]

    /** The index of the selected child menu, if there are any children. */
    index: number = -1

    /** Direction that the cursor moves in this element. */
    direction: "row" | "column" = "row"

    /** Direction the cursor needs to move to overflow to the previous element */
    startOverflow: "row" | "column" | "none" = "row"

    /** Direction the cursor needs to move to overflow to the next element */
    endOverflow: "row" | "column" | "none" = "row"

    /** Defines the edges of elements and where they should overflow to. */
    overflowRules: OverflowRule[]

    constructor(element: HTMLElement | null = null) {
        super(element)
        this.children = []
        this.overflowRules = []
    }

    /** When displayed, display all child menus to this menu's element */
    display(out: HTMLElement): void {
        super.display(out)
        
        for (let child of this.children) {
            child.display(this.element)
        }
    }

    /** stuff that should be run after the display function of all elements */
    postDisplay(out: HTMLElement): void {
        super.postDisplay(out)

        for (let child of this.children) {
            child.postDisplay(this.element)
        }
    }

    /** Define an overflow rule for this menu  */
    addOverflow(rule: OverflowRule) {
        this.overflowRules.push(rule)
    }

    /** Removes selection from this window. */
    removeSelection() {
        this.onDeselect(this.selectedElement())
        this.index = -1;
    }

    /** Set selected to true and select a certain index. */
    setSelection(index: number, selectChildren: boolean = true) {
        if (currentSelectionParent) currentSelectionParent.removeSelection()
        this.index = index;

        let ev = this.selectedElement()
        /** If selectChildren flag is true, move cursor to first child instead of this */
        if (selectChildren && ev.menu instanceof TraversableMenu) {
            ev.menu.setSelection(0, selectChildren)
        } else {
            setCurrentSelection(this, ev)
            this.onSelect(ev)
        }
    }

    /** Move selection by a set increment.
     * @returns [row overflow, column overflow]. 0 is no overflow, -1 is before start, 1 is past end
     */
    moveSelection(delta: number): number {
        if (this.index+delta < 0) return -1;
        if (this.index+delta >= this.children.length) return 1;
        this.setSelection(this.index + delta);
        return 0;
    }

    /** Retrieve the current selected element */
    selectedElement(): SelectEvent {
        return {index: this.index, menu: this.children[this.index]}
    }

    /** Behaviour when a child menu is selected. */
    onSelect(ev: SelectEvent) {
        if (!ev.menu) return;
        ev.menu.element.classList.add("bipole-cursor")
    }

    /** Behaviour when THIS element is deselected. */
    onDeselect(ev: SelectEvent) {
        if (!ev.menu) return;
        ev.menu.element.classList.remove("bipole-cursor")
    }

    /** Handles arrow keys, moving the cursor on the selected element if possible.
     * @returns amount of overflow; 0 for none, -1 for before start, 1 for past end
     */
    handleInput(event: KeyboardEvent): void {
        // Handles clicking selected element if enter/space pressed
        if (event.code === "Enter" || event.code === "Space") {
            let menuOnclick = this.selectedElement().menu.element.onclick;
            if (menuOnclick) menuOnclick.apply(null)
        }

        let ev = this.selectedElement();
        if (ev.menu instanceof TraversableMenu) {
            ev.menu.handleInput(event)
        }
    }

    /** Handles keypresses for cursor movement. 
     * Tries to move in elements higher in stack first. 
     * Also checks for overflow.
     * @return true if level below in stack should move cursor */
    handleCursorMovement(event: KeyboardEvent): boolean {
        let ev = this.selectedElement();

        let moveCursor: boolean;
        /** if selected element is traversable, handle cursor movement in it, and only move cursor if submenu requires */
        if (ev.menu instanceof TraversableMenu) {
            moveCursor = ev.menu.handleCursorMovement(event)
        } 
        /** if selected is not traversable, always move cursor here */
        else {
            moveCursor = true;
        }

        if (moveCursor) {
            let overflow = 0;
            if (this.direction === "row") {
                if (event.code === "ArrowLeft") overflow = this.moveSelection(-1)
                else if (event.code === "ArrowRight") overflow = this.moveSelection(1)
                else if (event.code === "ArrowUp") overflow = -1;
                else if (event.code === "ArrowDown") overflow = 1;
            } else {
                if (event.code === "ArrowUp") overflow = this.moveSelection(-1)
                else if (event.code === "ArrowDown") overflow = this.moveSelection(1)
                else if (event.code === "ArrowLeft") overflow = -1;
                else if (event.code === "ArrowRight") overflow = 1;
            }

            // let cursorDirection: "row" | "column" = (event.code === "ArrowLeft" || event.code === "ArrowRight") ? "row" : "column"

            // If cursor didn't move due due to not being an arrow or overflow failed, reselect the window in case it was deselected
            // if (overflow == 0 && ev.menu instanceof TraversableMenu && ev.menu.index == -1) {
            //     this.setSelection(ev.index)
            // }

            // console.log(this.constructor.name+": "+this.startOverflow+", "+this.endOverflow)

            /** If at the edge and startOverflow or endOverflow matched, let parent element handle overflow */
            if ((overflow === -1 && this.startOverflow === this.direction) || (overflow === 1 && this.endOverflow === this.direction)) {
                return true;
            }

            /** cursor should be moved in parent menus if overflowed here */
            return (overflow != 0)
        }

        return false;
    }
}

export type SelectEvent = {
    index: number,
    menu: Menu
}

/** Defines an edge between two elements in a menu */
export type OverflowRule = {
    /** Direction between elements */
    direction: ("row" | "column")

    /** Element to left or on top, depending on direction */
    first: Menu

    /** Element to right or on bottom, depending on direction */
    last: Menu
}
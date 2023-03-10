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

/** A menu that stores selectable sub-menus within it. */
export class TraversableMenu extends Menu {
    /** Child menus/selectable items of this in a grid. Drawn child menu elements within this menu's element. */
    children: Menu[]

    /** The index of the selected child menu, if there are any children. */
    index: number = -1

    /** Direction that the cursor moves in this element. */
    direction: ("row" | "column") = "row"

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
    }

    /** Set selected to true and select a certain index. */
    setSelection(index: number, selectChildren: boolean = true) {
        this.removeSelection();
        this.index = index;

        let ev = this.selectedElement()
        /** If selectChildren flag is true, move cursor to first child instead of this */
        if (selectChildren && ev.menu instanceof TraversableMenu) {
            ev.menu.setSelection(0, selectChildren)
        } else {
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

    /** Behaviour when a child menu is deselected. */
    onDeselect(ev: SelectEvent) {
        if (!ev.menu) return;
        ev.menu.element.classList.remove("bipole-cursor")
    }

    /** Handles arrow keys, moving the cursor on the selected element if possible.
     * @returns amount of overflow; 0 for none, -1 for before start, 1 for past end
     */
    handleInput(event: KeyboardEvent): void {
        // Handles cursor movement if arrow key pressed
        this.handleCursorMovement(event);

        // Handles clicking selected element if enter/space pressed
        if (event.code === "Enter" || event.code === "Space") {
            this.selectedElement().menu.element.onclick(null)
        }
    }

    /** Handles keypresses for cursor movement. 
     * @returns true if there was overflow / cursor could not be moved in this child menu  */
    handleCursorMovement(event: KeyboardEvent): boolean {
        
        /** Will be true if the cursor should be moved within this element */
        let shouldMoveCursor: boolean
        
        /** If sub element is traversable, traverse within it, and overflow is true if oveflowed outside of that element */
        let ev = this.selectedElement()
        if (ev.menu instanceof TraversableMenu) {
            ev.menu.handleCursorMovement(event)
        } 
        /** if not traversable, traversal has gone to deepest element, return true to stack below & try to move cursor */
        else {
            shouldMoveCursor = true;
        }

        /** Try to move cursor if no overflow if this is deepest element */
        let flowDirection: "row" | "column" = (event.code === "ArrowLeft" || event.code === "ArrowRight") ? "row" : "column"
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

        if (shouldMoveCursor) {
            /** If there is overflow, find out if this innermost element can be escaped from by overflow rules */
            if (overflow) {
                shouldMoveCursor = false;
                

            /** If cursor did not move, will did move cursor in this element, send true down stack */
            } else {
                shouldMoveCursor = true;
            }
        }

        /** Check for overflow rules */
        console.log(this.constructor.name +": "+ flowDirection)
        for (let overflowRule of this.overflowRules) {
            console.log(overflowRule)

            /** If cursor move direction matches rule */
            if (overflowRule.direction === flowDirection) {
                /** Check if selected is the element before the one it overflows to, if so, move forward to it */
                if (overflow == 1 && overflowRule.first === this) {
                    this.setSelection(this.children.indexOf(overflowRule.last))
                }

                /** Check if selected menu is the one after the one it overflows to */
                else if (overflow == -1 && overflowRule.last === this) {
                    this.setSelection(this.children.indexOf(overflowRule.first))
                }
            }
        }

        // Returns: false if not traversable or handled overflow of this element successfully
        return shouldMoveCursor;
    }
}

export type SelectEvent = {
    index: number,
    menu: Menu
}
// Stores the element that was last focused, incase focus is lost
let lastFocusedElement: HTMLElement = null

// updates the last focused element, call when needed
function updateLastFocusedElement() {
    let activeElem = document.activeElement;
    if (activeElem !== document.body && activeElem !== lastFocusedElement && activeElem instanceof HTMLElement) lastFocusedElement = activeElem; 
}

// update focus on clicks
document.addEventListener("click", () => {
    updateLastFocusedElement();
})

// cursor movement between elements
document.addEventListener("keydown", function (evt) {
	updateLastFocusedElement();

    let activeElem = document.activeElement;
    if (!activeElem || activeElem === document.body) activeElem = lastFocusedElement;
    if (!(activeElem instanceof HTMLElement)) return;

    let axis = activeElem.getAttribute("axis")
    if (!axis) axis = "row"

    // Overflow. will be name of evt key if not handled, "none" if handled without overflow
    let overflow: string = evt.code;

    // Focus elements with arrow keys.
    let nextElem: Element = null
    if ((evt.code === "ArrowLeft" && axis === "row") || (evt.code === "ArrowUp" && axis === "column")) {
		nextElem = activeElem.previousElementSibling; 
	}
    else if ((evt.code === "ArrowRight" && axis === "row") || (evt.code === "ArrowDown" && axis === "column")) {
		nextElem = activeElem.nextElementSibling;
	}
    
    // If cursor was moved and next element was found, no overflow
    if (nextElem instanceof HTMLElement) {
        overflow = "none"
        tryFocus(nextElem);
    }

    // If cursor would cause overflow outside of element,
    if (overflow !== "none") {
        // check for overflow{evt.code}, if found, focus element with that id. ex. overflowArrowUp, overflowArrowLeft
        let overflowAttributeName = "overflow"+overflow;

        // check all parents of element for this tag
        let parent: HTMLElement | null = activeElem
        while (parent) {
            activeElem = parent;

            if (!(activeElem instanceof HTMLElement)) break;
            let overflowTo = activeElem.getAttribute(overflowAttributeName)

            // if attribute was found, select element with id of value
            if (overflowTo) {
                tryFocusAll( document.getElementById(overflowTo) )
                break;
            }

            parent = activeElem.parentElement;
        }
    }
});

// Focus an element. ADDITIONALLY, set last focusable element in case it is unfocused.
function tryFocus(elem: HTMLElement): boolean {
    elem.focus();
    if (document.activeElement === elem) {
        lastFocusedElement = elem;
        return true;
    } else {
        return false;
    }
}

// Try to focus all child elements in this node. Once one is focused, stop
function tryFocusAll(elem: HTMLElement): boolean {
    // Try to focus this element
    if (tryFocus(elem)) return true;

    // Try on all child elements
    for (var i = 0; i < elem.children.length; i++) {
        // If element was successfully focused, stop checking
        var child = elem.children[i];
        if (child instanceof HTMLElement && tryFocusAll(child)) {
            lastFocusedElement = child;
            return true;   
        }
    }

    return false;
}

// Definitions
function map() {
    console.log("map")
}

function deck() {
    console.log("deck")
}

function items() {
    console.log("items")
}

// DOCUMENT SETUP
// button onclicks
document.getElementById("choice_map").onclick = map
document.getElementById("choice_deck").onclick = deck
document.getElementById("choice_items").onclick = items

// select first selectable in output
tryFocusAll( document.getElementById("output") );
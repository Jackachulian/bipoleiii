/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/cutscene.ts":
/*!*************************!*\
  !*** ./src/cutscene.ts ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "loadCutscene": () => (/* binding */ loadCutscene)
/* harmony export */ });
function loadCutscene(name) {
    fetch(`./cutscenes/${name}.txt`)
        .then((data) => console.log(data.text()));
}


/***/ }),

/***/ "./src/display.ts":
/*!************************!*\
  !*** ./src/display.ts ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addElement": () => (/* binding */ addElement),
/* harmony export */   "button": () => (/* binding */ button),
/* harmony export */   "clear": () => (/* binding */ clear),
/* harmony export */   "header": () => (/* binding */ header),
/* harmony export */   "line": () => (/* binding */ line),
/* harmony export */   "output": () => (/* binding */ output),
/* harmony export */   "space": () => (/* binding */ space),
/* harmony export */   "writeElement": () => (/* binding */ writeElement)
/* harmony export */ });
/** The main element where output is written to. */
const output = document.getElementById("output") || document.body;
function clear() {
    output.textContent = '';
}
/**
 * Append an element to output.
 * @param {string} text text to put in the element
 * @param {string} element element tag
 */
function writeElement(text, element) {
    let p = document.createElement(element);
    p.innerHTML = text;
    output.append(p);
}
function addElement(elem) {
    output.append(elem);
}
/**
 * Add a paragraph to the output witht he given text.
 * @param {string} text
 */
function line(text) {
    let span = document.createElement("span");
    span.classList.add("bipole-line", "ascii");
    span.innerHTML = text;
    output.append(span);
    return span;
}
/** Add a line break. */
function space() {
    output.append(document.createElement("br"));
}
/**
 *
 * @param {string} text
 */
function header(text) {
    writeElement(text, "h1");
}
/**
 * Append a button with the given effect to the screen.
 * @param onclick the effect that happens when the button is used
 */
function button(text, onclick) {
    let button = document.createElement("button");
    button.innerHTML = text;
    button.classList.add("btn", "btn-ghost");
    button.onclick = onclick;
    output.append(button);
    return button;
}


/***/ }),

/***/ "./src/homemenus.ts":
/*!**************************!*\
  !*** ./src/homemenus.ts ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HomeMenu": () => (/* binding */ HomeMenu)
/* harmony export */ });
/* harmony import */ var _cutscene__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./cutscene */ "./src/cutscene.ts");
/* harmony import */ var _window__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./window */ "./src/window.ts");


class HomeMenu extends _window__WEBPACK_IMPORTED_MODULE_1__.ChoiceMenu {
    constructor() {
        super("", [
            { input: ["1"], label: "Map", effect: () => { } },
            { input: ["2"], label: "Items", effect: () => { } }
        ], 'Home');
        (0,_cutscene__WEBPACK_IMPORTED_MODULE_0__.loadCutscene)("intro");
    }
}


/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "back": () => (/* binding */ back),
/* harmony export */   "clearHistoryTo": () => (/* binding */ clearHistoryTo),
/* harmony export */   "currentWindow": () => (/* binding */ currentWindow),
/* harmony export */   "gotoWindow": () => (/* binding */ gotoWindow),
/* harmony export */   "handleInput": () => (/* binding */ handleInput),
/* harmony export */   "handleTextSubmit": () => (/* binding */ handleTextSubmit),
/* harmony export */   "showCursor": () => (/* binding */ showCursor)
/* harmony export */ });
/* harmony import */ var _mainmenus__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mainmenus */ "./src/mainmenus.ts");

/** Stores the current window path. */
const windows = [new _mainmenus__WEBPACK_IMPORTED_MODULE_0__.MainMenu()];
let showCursor = true;
function currentWindow() {
    return windows[windows.length - 1];
}
/**
 * Clears window history back to a certain index
 * @param index the index to stop at (exclusive)
 */
function clearHistoryTo(index) {
    while (windows.length > index + 1)
        windows.pop();
}
/**
 *
 * @param {Window} window the window to set & display
 */
function gotoWindow(window) {
    // store current window and add to window stack
    windows.push(window);
    window.display();
}
/**
 * Move back one step in the window history.
 */
function back() {
    if (windows.length <= 1)
        return; // do not exit outermost window
    windows.pop();
    currentWindow().display();
}
function handleInput(event) {
    currentWindow().handleInput(event);
}
function handleTextSubmit(text) {
    currentWindow().handleTextSubmit(text);
}
// listens for keypresses on the document body
document.body.onkeydown = function (event) {
    // If the user is focused on another input, ignore key presses
    if (event.target != document.body) {
        return;
    }
    currentWindow().handleInput(event);
};
windows[0].display();


/***/ }),

/***/ "./src/mainmenus.ts":
/*!**************************!*\
  !*** ./src/mainmenus.ts ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ChooseName": () => (/* binding */ ChooseName),
/* harmony export */   "MainMenu": () => (/* binding */ MainMenu),
/* harmony export */   "NameConfirm": () => (/* binding */ NameConfirm)
/* harmony export */ });
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index */ "./src/index.ts");
/* harmony import */ var _display__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./display */ "./src/display.ts");
/* harmony import */ var _window__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./window */ "./src/window.ts");
/* harmony import */ var _homemenus__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./homemenus */ "./src/homemenus.ts");




// Main Menu. the landing page for the game
class MainMenu extends _window__WEBPACK_IMPORTED_MODULE_2__.ChoiceMenu {
    constructor() {
        super("", [
            { input: ["1"], label: "New Game", effect: () => this.goto(new ChooseName()) },
            { input: ["2"], label: "Load Game", effect: () => this.showToast("Loading not implemented") }
        ]);
    }
    displayAboveToast() {
        (0,_display__WEBPACK_IMPORTED_MODULE_1__.line)(`
______ ___________ _____ _      _____   _____ _____ _____ 
| ___ \\_   _| ___ \\  _  | |    |  ___| |_   _|_   _|_   _|
| |_/ / | | | |_/ / | | | |    | |__     | |   | |   | |  
| ___ \\ | | |  __/| | | | |    |  __|    | |   | |   | |  
| |_/ /_| |_| |   \\ \\_/ / |____| |___   _| |_ _| |_ _| |_ 
\\____/ \\___/\\_|    \\___/\\_____/\\____/   \\___/ \\___/ \\___/
        
        `);
    }
}
class ChooseName extends _window__WEBPACK_IMPORTED_MODULE_2__.TextInputMenu {
    constructor() {
        super("newgame", "Choose a name...");
        this.direction = "top-bottom";
        this.addChoice((0,_window__WEBPACK_IMPORTED_MODULE_2__.universalBack)());
        this.maxlength = 24;
    }
    handleTextSubmit(text) {
        if (text.length === 0) {
            text = "Lead";
        }
        if (text.length > this.maxlength) {
            this.showToast("Name is too long");
            return;
        }
        (0,_index__WEBPACK_IMPORTED_MODULE_0__.gotoWindow)(new NameConfirm(text));
    }
}
class NameConfirm extends _window__WEBPACK_IMPORTED_MODULE_2__.ChoiceMenu {
    constructor(selectedName) {
        super("newgame/confirm", [
            { input: ["Z", "KeyZ", "KeyY"], label: "Yes", effect: () => this.goto(new _homemenus__WEBPACK_IMPORTED_MODULE_3__.HomeMenu()) },
            (0,_window__WEBPACK_IMPORTED_MODULE_2__.universalBack)("No")
        ], `Are you sure you want to be named <span class="hljs-built_in">${selectedName}</span>?`);
        this.selectedName = selectedName;
    }
}


/***/ }),

/***/ "./src/window.ts":
/*!***********************!*\
  !*** ./src/window.ts ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ChoiceMenu": () => (/* binding */ ChoiceMenu),
/* harmony export */   "IndexedElementWindow": () => (/* binding */ IndexedElementWindow),
/* harmony export */   "TextInputMenu": () => (/* binding */ TextInputMenu),
/* harmony export */   "Window": () => (/* binding */ Window),
/* harmony export */   "universalBack": () => (/* binding */ universalBack)
/* harmony export */ });
/* harmony import */ var _display__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./display */ "./src/display.ts");
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./index */ "./src/index.ts");


/**
 * Displays stuff to the output element on the page, and handles inputs submitted to it, mainly choices.
 */
class Window {
    constructor(id = "") {
        this.id = id;
        this.toast = document.createElement("div");
        this.toast.classList.add("bipole-toast");
    }
    /**
     * Display this to the screen.
     */
    display() {
        (0,_display__WEBPACK_IMPORTED_MODULE_0__.clear)();
        this.displayAboveToast();
        _display__WEBPACK_IMPORTED_MODULE_0__.output.append(this.toast);
        // further behaviour implemented in inheriting classes
    }
    displayAboveToast() {
        // to be overridden in subclasses
    }
    /**
     *
     * @param {string | number} text the string or number passed as an input. Choices are usually numbers, stuff like names/letters is strings
     * Base behaviour: left arrow will move back in history, right arrow moves forward if possible
     * Should be called in super for all windows that can be traversed back from.
     */
    handleInput(event) {
        // to be implemented in subclasses
    }
    /**
     * Handle a text input field being submitted to this window.
     * @param text the text that was submitted
     */
    handleTextSubmit(text) {
        alert("submitted " + text);
    }
    showToast(toast) {
        this.toast.innerHTML = toast + "<br>";
    }
    /**
     * Go to another window FROM this window.
     * Has some extra functionality such as clearing current toast.
     * @param window the window to navigate to
     */
    goto(window) {
        this.toast.innerHTML = "";
        (0,_index__WEBPACK_IMPORTED_MODULE_1__.gotoWindow)(window);
    }
}
class IndexedElementWindow extends Window {
    constructor(path) {
        super(path);
        this.direction = "left-right";
        this.selectedIndex = 0;
        this.selectableElements = [];
    }
    display() {
        super.display();
        // clears any existing selectable elements (this is being redrawn)
        this.selectableElements = [];
    }
    handleInput(event) {
        // left - go back a window (from super)
        super.handleInput(event);
        this.handleArrowKeys(event);
        // enter - select current selected cursor choice
        if (event.code === "Enter") {
            this.handleElementPressed(this.selectableElements[this.selectedIndex], this.selectedIndex);
        }
    }
    /**
     * Moves the cursor.
     * @param event keyboard event
     * @returns true if an arrow key input was handled
     */
    handleArrowKeys(event) {
        // right/left - move choice cursor
        if (event.code === (this.direction === "top-bottom" ? 'ArrowUp' : 'ArrowLeft') && this.selectedIndex > 0) {
            this.moveSelection(-1);
            return true;
        }
        if (event.code === (this.direction === "top-bottom" ? 'ArrowDown' : 'ArrowRight') && this.selectedIndex + 1 < this.selectableElements.length) {
            this.moveSelection(1);
            return true;
        }
        return false;
    }
    setSelection(index) {
        this.handleElementDeselected(this.selectableElements[this.selectedIndex], this.selectedIndex);
        this.selectedIndex = index;
        this.handleElementSelected(this.selectableElements[this.selectedIndex], this.selectedIndex);
    }
    moveSelection(delta) {
        this.setSelection(this.selectedIndex + delta);
    }
    handleElementDeselected(element, index) {
        document.body.focus();
        element.classList.remove("bipole-cursor");
        // further behaviour to be implemented in subclasses
    }
    handleElementSelected(element, index) {
        element.classList.add("bipole-cursor");
        // further behaviour to be implemented in subclasses
    }
    handleElementPressed(element, index) {
        if (element.onclick)
            element.onclick(null);
        // further behaviour to be implemented in subclasses
    }
}
const universalBack = (name = "Back") => {
    return { input: ["X", "KeyX", "KeyN"], label: name, effect: () => (0,_index__WEBPACK_IMPORTED_MODULE_1__.back)() };
};
class ChoiceMenu extends IndexedElementWindow {
    constructor(path, choices = [], prompt = null) {
        super(path);
        this.choices = choices;
        this.prompt = prompt;
    }
    display() {
        super.display();
        this.displayAboveChoices();
        this.displayChoices();
        this.setSelection(0);
    }
    displayAboveChoices() {
        if (this.prompt)
            (0,_display__WEBPACK_IMPORTED_MODULE_0__.line)(this.prompt);
    }
    displayChoices() {
        let listElement = document.createElement("div");
        listElement.classList.add("ascii");
        for (let i = 0; i < this.choices.length; i++) {
            const choice = this.choices[i];
            let buttonElem = (0,_display__WEBPACK_IMPORTED_MODULE_0__.button)(`[${choice.input[0]}] ${choice.label}`, () => choice.effect());
            _display__WEBPACK_IMPORTED_MODULE_0__.output.append(buttonElem);
            this.selectableElements.push(buttonElem);
        }
        _display__WEBPACK_IMPORTED_MODULE_0__.output.append(listElement);
    }
    addChoice(choice) {
        this.choices.push(choice);
    }
    handleInput(event) {
        super.handleInput(event);
        for (let choice of this.choices) {
            for (let inputCode of choice.input) {
                if (event.code === inputCode || event.key === inputCode) {
                    choice.effect();
                    return;
                }
            }
        }
    }
}
class TextInputMenu extends ChoiceMenu {
    constructor(id, prompt) {
        super(id);
        this.maxlength = 0;
        this.prompt = prompt;
    }
    displayAboveChoices() {
        super.displayAboveChoices();
        this.displayTextInput();
    }
    displayTextInput() {
        let promptElem = document.createElement("div");
        _display__WEBPACK_IMPORTED_MODULE_0__.output.append(promptElem);
        this.selectableElements.push(promptElem);
        promptElem.classList.add("bipole-prompt");
        let pointerElem = document.createElement("span");
        promptElem.append(pointerElem);
        pointerElem.classList.add("bipole-pointer");
        pointerElem.innerHTML = "> ";
        this.inputElem = document.createElement("input");
        promptElem.append(this.inputElem);
        this.inputElem.type = "text";
        this.inputElem.placeholder = "Lead";
        this.inputElem.classList.add("bipole-prompt-input");
        let thisWindow = this;
        let ie = this.inputElem;
        this.inputElem.onkeydown = function (event) {
            if (thisWindow.handleArrowKeys(event))
                ie.blur();
            if (event.code === 'Enter') {
                (0,_index__WEBPACK_IMPORTED_MODULE_1__.handleTextSubmit)(ie.value);
            }
            setTimeout(() => {
                if (ie.value.length > 24) {
                    ie.classList.add("bipole-error");
                }
                else {
                    ie.classList.remove("bipole-error");
                }
            }, 0);
        };
    }
    handleInput(event) {
        super.handleInput(event);
    }
    handleElementSelected(element, index) {
        super.handleElementSelected(element, index);
        // If the text box was selected, place cursor in it
        if (index === 0) {
            // because browser is being quirky, adding, a timeout here to wait for other events
            setTimeout(() => this.inputElem.focus(), 0);
        }
    }
}


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./src/index.ts");
/******/ 	
/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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Q1BBOzs7OztXQ0FBO1dBQ0E7V0FDQTtXQUNBLHVEQUF1RCxpQkFBaUI7V0FDeEU7V0FDQSxnREFBZ0QsYUFBYTtXQUM3RDs7Ozs7VUVOQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL2JpcG9sZWlpaS8uL3NyYy9jdXRzY2VuZS50cyIsIndlYnBhY2s6Ly9iaXBvbGVpaWkvLi9zcmMvZGlzcGxheS50cyIsIndlYnBhY2s6Ly9iaXBvbGVpaWkvLi9zcmMvaG9tZW1lbnVzLnRzIiwid2VicGFjazovL2JpcG9sZWlpaS8uL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9iaXBvbGVpaWkvLi9zcmMvbWFpbm1lbnVzLnRzIiwid2VicGFjazovL2JpcG9sZWlpaS8uL3NyYy93aW5kb3cudHMiLCJ3ZWJwYWNrOi8vYmlwb2xlaWlpL3dlYnBhY2svYm9vdHN0cmFwIiwid2VicGFjazovL2JpcG9sZWlpaS93ZWJwYWNrL3J1bnRpbWUvZGVmaW5lIHByb3BlcnR5IGdldHRlcnMiLCJ3ZWJwYWNrOi8vYmlwb2xlaWlpL3dlYnBhY2svcnVudGltZS9oYXNPd25Qcm9wZXJ0eSBzaG9ydGhhbmQiLCJ3ZWJwYWNrOi8vYmlwb2xlaWlpL3dlYnBhY2svcnVudGltZS9tYWtlIG5hbWVzcGFjZSBvYmplY3QiLCJ3ZWJwYWNrOi8vYmlwb2xlaWlpL3dlYnBhY2svYmVmb3JlLXN0YXJ0dXAiLCJ3ZWJwYWNrOi8vYmlwb2xlaWlpL3dlYnBhY2svc3RhcnR1cCIsIndlYnBhY2s6Ly9iaXBvbGVpaWkvd2VicGFjay9hZnRlci1zdGFydHVwIl0sInNvdXJjZXNDb250ZW50IjpbImV4cG9ydCBmdW5jdGlvbiBsb2FkQ3V0c2NlbmUobmFtZSkge1xuICAgIGZldGNoKGAuL2N1dHNjZW5lcy8ke25hbWV9LnR4dGApXG4gICAgICAgIC50aGVuKChkYXRhKSA9PiBjb25zb2xlLmxvZyhkYXRhLnRleHQoKSkpO1xufVxuIiwiLyoqIFRoZSBtYWluIGVsZW1lbnQgd2hlcmUgb3V0cHV0IGlzIHdyaXR0ZW4gdG8uICovXG5leHBvcnQgY29uc3Qgb3V0cHV0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJvdXRwdXRcIikgfHwgZG9jdW1lbnQuYm9keTtcbmV4cG9ydCBmdW5jdGlvbiBjbGVhcigpIHtcbiAgICBvdXRwdXQudGV4dENvbnRlbnQgPSAnJztcbn1cbi8qKlxuICogQXBwZW5kIGFuIGVsZW1lbnQgdG8gb3V0cHV0LlxuICogQHBhcmFtIHtzdHJpbmd9IHRleHQgdGV4dCB0byBwdXQgaW4gdGhlIGVsZW1lbnRcbiAqIEBwYXJhbSB7c3RyaW5nfSBlbGVtZW50IGVsZW1lbnQgdGFnXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiB3cml0ZUVsZW1lbnQodGV4dCwgZWxlbWVudCkge1xuICAgIGxldCBwID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChlbGVtZW50KTtcbiAgICBwLmlubmVySFRNTCA9IHRleHQ7XG4gICAgb3V0cHV0LmFwcGVuZChwKTtcbn1cbmV4cG9ydCBmdW5jdGlvbiBhZGRFbGVtZW50KGVsZW0pIHtcbiAgICBvdXRwdXQuYXBwZW5kKGVsZW0pO1xufVxuLyoqXG4gKiBBZGQgYSBwYXJhZ3JhcGggdG8gdGhlIG91dHB1dCB3aXRodCBoZSBnaXZlbiB0ZXh0LlxuICogQHBhcmFtIHtzdHJpbmd9IHRleHRcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGxpbmUodGV4dCkge1xuICAgIGxldCBzcGFuID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInNwYW5cIik7XG4gICAgc3Bhbi5jbGFzc0xpc3QuYWRkKFwiYmlwb2xlLWxpbmVcIiwgXCJhc2NpaVwiKTtcbiAgICBzcGFuLmlubmVySFRNTCA9IHRleHQ7XG4gICAgb3V0cHV0LmFwcGVuZChzcGFuKTtcbiAgICByZXR1cm4gc3Bhbjtcbn1cbi8qKiBBZGQgYSBsaW5lIGJyZWFrLiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHNwYWNlKCkge1xuICAgIG91dHB1dC5hcHBlbmQoZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJyXCIpKTtcbn1cbi8qKlxuICpcbiAqIEBwYXJhbSB7c3RyaW5nfSB0ZXh0XG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBoZWFkZXIodGV4dCkge1xuICAgIHdyaXRlRWxlbWVudCh0ZXh0LCBcImgxXCIpO1xufVxuLyoqXG4gKiBBcHBlbmQgYSBidXR0b24gd2l0aCB0aGUgZ2l2ZW4gZWZmZWN0IHRvIHRoZSBzY3JlZW4uXG4gKiBAcGFyYW0gb25jbGljayB0aGUgZWZmZWN0IHRoYXQgaGFwcGVucyB3aGVuIHRoZSBidXR0b24gaXMgdXNlZFxuICovXG5leHBvcnQgZnVuY3Rpb24gYnV0dG9uKHRleHQsIG9uY2xpY2spIHtcbiAgICBsZXQgYnV0dG9uID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJ1dHRvblwiKTtcbiAgICBidXR0b24uaW5uZXJIVE1MID0gdGV4dDtcbiAgICBidXR0b24uY2xhc3NMaXN0LmFkZChcImJ0blwiLCBcImJ0bi1naG9zdFwiKTtcbiAgICBidXR0b24ub25jbGljayA9IG9uY2xpY2s7XG4gICAgb3V0cHV0LmFwcGVuZChidXR0b24pO1xuICAgIHJldHVybiBidXR0b247XG59XG4iLCJpbXBvcnQgeyBsb2FkQ3V0c2NlbmUgfSBmcm9tIFwiLi9jdXRzY2VuZVwiO1xuaW1wb3J0IHsgQ2hvaWNlTWVudSB9IGZyb20gXCIuL3dpbmRvd1wiO1xuZXhwb3J0IGNsYXNzIEhvbWVNZW51IGV4dGVuZHMgQ2hvaWNlTWVudSB7XG4gICAgY29uc3RydWN0b3IoKSB7XG4gICAgICAgIHN1cGVyKFwiXCIsIFtcbiAgICAgICAgICAgIHsgaW5wdXQ6IFtcIjFcIl0sIGxhYmVsOiBcIk1hcFwiLCBlZmZlY3Q6ICgpID0+IHsgfSB9LFxuICAgICAgICAgICAgeyBpbnB1dDogW1wiMlwiXSwgbGFiZWw6IFwiSXRlbXNcIiwgZWZmZWN0OiAoKSA9PiB7IH0gfVxuICAgICAgICBdLCAnSG9tZScpO1xuICAgICAgICBsb2FkQ3V0c2NlbmUoXCJpbnRyb1wiKTtcbiAgICB9XG59XG4iLCJpbXBvcnQgeyBNYWluTWVudSB9IGZyb20gXCIuL21haW5tZW51c1wiO1xuLyoqIFN0b3JlcyB0aGUgY3VycmVudCB3aW5kb3cgcGF0aC4gKi9cbmNvbnN0IHdpbmRvd3MgPSBbbmV3IE1haW5NZW51KCldO1xuZXhwb3J0IGxldCBzaG93Q3Vyc29yID0gdHJ1ZTtcbmV4cG9ydCBmdW5jdGlvbiBjdXJyZW50V2luZG93KCkge1xuICAgIHJldHVybiB3aW5kb3dzW3dpbmRvd3MubGVuZ3RoIC0gMV07XG59XG4vKipcbiAqIENsZWFycyB3aW5kb3cgaGlzdG9yeSBiYWNrIHRvIGEgY2VydGFpbiBpbmRleFxuICogQHBhcmFtIGluZGV4IHRoZSBpbmRleCB0byBzdG9wIGF0IChleGNsdXNpdmUpXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBjbGVhckhpc3RvcnlUbyhpbmRleCkge1xuICAgIHdoaWxlICh3aW5kb3dzLmxlbmd0aCA+IGluZGV4ICsgMSlcbiAgICAgICAgd2luZG93cy5wb3AoKTtcbn1cbi8qKlxuICpcbiAqIEBwYXJhbSB7V2luZG93fSB3aW5kb3cgdGhlIHdpbmRvdyB0byBzZXQgJiBkaXNwbGF5XG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBnb3RvV2luZG93KHdpbmRvdykge1xuICAgIC8vIHN0b3JlIGN1cnJlbnQgd2luZG93IGFuZCBhZGQgdG8gd2luZG93IHN0YWNrXG4gICAgd2luZG93cy5wdXNoKHdpbmRvdyk7XG4gICAgd2luZG93LmRpc3BsYXkoKTtcbn1cbi8qKlxuICogTW92ZSBiYWNrIG9uZSBzdGVwIGluIHRoZSB3aW5kb3cgaGlzdG9yeS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGJhY2soKSB7XG4gICAgaWYgKHdpbmRvd3MubGVuZ3RoIDw9IDEpXG4gICAgICAgIHJldHVybjsgLy8gZG8gbm90IGV4aXQgb3V0ZXJtb3N0IHdpbmRvd1xuICAgIHdpbmRvd3MucG9wKCk7XG4gICAgY3VycmVudFdpbmRvdygpLmRpc3BsYXkoKTtcbn1cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVJbnB1dChldmVudCkge1xuICAgIGN1cnJlbnRXaW5kb3coKS5oYW5kbGVJbnB1dChldmVudCk7XG59XG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlVGV4dFN1Ym1pdCh0ZXh0KSB7XG4gICAgY3VycmVudFdpbmRvdygpLmhhbmRsZVRleHRTdWJtaXQodGV4dCk7XG59XG4vLyBsaXN0ZW5zIGZvciBrZXlwcmVzc2VzIG9uIHRoZSBkb2N1bWVudCBib2R5XG5kb2N1bWVudC5ib2R5Lm9ua2V5ZG93biA9IGZ1bmN0aW9uIChldmVudCkge1xuICAgIC8vIElmIHRoZSB1c2VyIGlzIGZvY3VzZWQgb24gYW5vdGhlciBpbnB1dCwgaWdub3JlIGtleSBwcmVzc2VzXG4gICAgaWYgKGV2ZW50LnRhcmdldCAhPSBkb2N1bWVudC5ib2R5KSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY3VycmVudFdpbmRvdygpLmhhbmRsZUlucHV0KGV2ZW50KTtcbn07XG53aW5kb3dzWzBdLmRpc3BsYXkoKTtcbiIsImltcG9ydCB7IGdvdG9XaW5kb3cgfSBmcm9tIFwiLi9pbmRleFwiO1xuaW1wb3J0IHsgbGluZSB9IGZyb20gXCIuL2Rpc3BsYXlcIjtcbmltcG9ydCB7IENob2ljZU1lbnUsIFRleHRJbnB1dE1lbnUsIHVuaXZlcnNhbEJhY2sgfSBmcm9tIFwiLi93aW5kb3dcIjtcbmltcG9ydCB7IEhvbWVNZW51IH0gZnJvbSBcIi4vaG9tZW1lbnVzXCI7XG4vLyBNYWluIE1lbnUuIHRoZSBsYW5kaW5nIHBhZ2UgZm9yIHRoZSBnYW1lXG5leHBvcnQgY2xhc3MgTWFpbk1lbnUgZXh0ZW5kcyBDaG9pY2VNZW51IHtcbiAgICBjb25zdHJ1Y3RvcigpIHtcbiAgICAgICAgc3VwZXIoXCJcIiwgW1xuICAgICAgICAgICAgeyBpbnB1dDogW1wiMVwiXSwgbGFiZWw6IFwiTmV3IEdhbWVcIiwgZWZmZWN0OiAoKSA9PiB0aGlzLmdvdG8obmV3IENob29zZU5hbWUoKSkgfSxcbiAgICAgICAgICAgIHsgaW5wdXQ6IFtcIjJcIl0sIGxhYmVsOiBcIkxvYWQgR2FtZVwiLCBlZmZlY3Q6ICgpID0+IHRoaXMuc2hvd1RvYXN0KFwiTG9hZGluZyBub3QgaW1wbGVtZW50ZWRcIikgfVxuICAgICAgICBdKTtcbiAgICB9XG4gICAgZGlzcGxheUFib3ZlVG9hc3QoKSB7XG4gICAgICAgIGxpbmUoYFxuX19fX19fIF9fX19fX19fX19fIF9fX19fIF8gICAgICBfX19fXyAgIF9fX19fIF9fX19fIF9fX19fIFxufCBfX18gXFxcXF8gICBffCBfX18gXFxcXCAgXyAgfCB8ICAgIHwgIF9fX3wgfF8gICBffF8gICBffF8gICBffFxufCB8Xy8gLyB8IHwgfCB8Xy8gLyB8IHwgfCB8ICAgIHwgfF9fICAgICB8IHwgICB8IHwgICB8IHwgIFxufCBfX18gXFxcXCB8IHwgfCAgX18vfCB8IHwgfCB8ICAgIHwgIF9ffCAgICB8IHwgICB8IHwgICB8IHwgIFxufCB8Xy8gL198IHxffCB8ICAgXFxcXCBcXFxcXy8gLyB8X19fX3wgfF9fXyAgIF98IHxfIF98IHxfIF98IHxfIFxuXFxcXF9fX18vIFxcXFxfX18vXFxcXF98ICAgIFxcXFxfX18vXFxcXF9fX19fL1xcXFxfX19fLyAgIFxcXFxfX18vIFxcXFxfX18vIFxcXFxfX18vXG4gICAgICAgIFxuICAgICAgICBgKTtcbiAgICB9XG59XG5leHBvcnQgY2xhc3MgQ2hvb3NlTmFtZSBleHRlbmRzIFRleHRJbnB1dE1lbnUge1xuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBzdXBlcihcIm5ld2dhbWVcIiwgXCJDaG9vc2UgYSBuYW1lLi4uXCIpO1xuICAgICAgICB0aGlzLmRpcmVjdGlvbiA9IFwidG9wLWJvdHRvbVwiO1xuICAgICAgICB0aGlzLmFkZENob2ljZSh1bml2ZXJzYWxCYWNrKCkpO1xuICAgICAgICB0aGlzLm1heGxlbmd0aCA9IDI0O1xuICAgIH1cbiAgICBoYW5kbGVUZXh0U3VibWl0KHRleHQpIHtcbiAgICAgICAgaWYgKHRleHQubGVuZ3RoID09PSAwKSB7XG4gICAgICAgICAgICB0ZXh0ID0gXCJMZWFkXCI7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHRleHQubGVuZ3RoID4gdGhpcy5tYXhsZW5ndGgpIHtcbiAgICAgICAgICAgIHRoaXMuc2hvd1RvYXN0KFwiTmFtZSBpcyB0b28gbG9uZ1wiKTtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBnb3RvV2luZG93KG5ldyBOYW1lQ29uZmlybSh0ZXh0KSk7XG4gICAgfVxufVxuZXhwb3J0IGNsYXNzIE5hbWVDb25maXJtIGV4dGVuZHMgQ2hvaWNlTWVudSB7XG4gICAgY29uc3RydWN0b3Ioc2VsZWN0ZWROYW1lKSB7XG4gICAgICAgIHN1cGVyKFwibmV3Z2FtZS9jb25maXJtXCIsIFtcbiAgICAgICAgICAgIHsgaW5wdXQ6IFtcIlpcIiwgXCJLZXlaXCIsIFwiS2V5WVwiXSwgbGFiZWw6IFwiWWVzXCIsIGVmZmVjdDogKCkgPT4gdGhpcy5nb3RvKG5ldyBIb21lTWVudSgpKSB9LFxuICAgICAgICAgICAgdW5pdmVyc2FsQmFjayhcIk5vXCIpXG4gICAgICAgIF0sIGBBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gYmUgbmFtZWQgPHNwYW4gY2xhc3M9XCJobGpzLWJ1aWx0X2luXCI+JHtzZWxlY3RlZE5hbWV9PC9zcGFuPj9gKTtcbiAgICAgICAgdGhpcy5zZWxlY3RlZE5hbWUgPSBzZWxlY3RlZE5hbWU7XG4gICAgfVxufVxuIiwiaW1wb3J0IHsgYnV0dG9uLCBjbGVhciwgbGluZSwgb3V0cHV0IH0gZnJvbSBcIi4vZGlzcGxheVwiO1xuaW1wb3J0IHsgYmFjaywgZ290b1dpbmRvdywgaGFuZGxlVGV4dFN1Ym1pdCB9IGZyb20gXCIuL2luZGV4XCI7XG4vKipcbiAqIERpc3BsYXlzIHN0dWZmIHRvIHRoZSBvdXRwdXQgZWxlbWVudCBvbiB0aGUgcGFnZSwgYW5kIGhhbmRsZXMgaW5wdXRzIHN1Ym1pdHRlZCB0byBpdCwgbWFpbmx5IGNob2ljZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBXaW5kb3cge1xuICAgIGNvbnN0cnVjdG9yKGlkID0gXCJcIikge1xuICAgICAgICB0aGlzLmlkID0gaWQ7XG4gICAgICAgIHRoaXMudG9hc3QgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB0aGlzLnRvYXN0LmNsYXNzTGlzdC5hZGQoXCJiaXBvbGUtdG9hc3RcIik7XG4gICAgfVxuICAgIC8qKlxuICAgICAqIERpc3BsYXkgdGhpcyB0byB0aGUgc2NyZWVuLlxuICAgICAqL1xuICAgIGRpc3BsYXkoKSB7XG4gICAgICAgIGNsZWFyKCk7XG4gICAgICAgIHRoaXMuZGlzcGxheUFib3ZlVG9hc3QoKTtcbiAgICAgICAgb3V0cHV0LmFwcGVuZCh0aGlzLnRvYXN0KTtcbiAgICAgICAgLy8gZnVydGhlciBiZWhhdmlvdXIgaW1wbGVtZW50ZWQgaW4gaW5oZXJpdGluZyBjbGFzc2VzXG4gICAgfVxuICAgIGRpc3BsYXlBYm92ZVRvYXN0KCkge1xuICAgICAgICAvLyB0byBiZSBvdmVycmlkZGVuIGluIHN1YmNsYXNzZXNcbiAgICB9XG4gICAgLyoqXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZyB8IG51bWJlcn0gdGV4dCB0aGUgc3RyaW5nIG9yIG51bWJlciBwYXNzZWQgYXMgYW4gaW5wdXQuIENob2ljZXMgYXJlIHVzdWFsbHkgbnVtYmVycywgc3R1ZmYgbGlrZSBuYW1lcy9sZXR0ZXJzIGlzIHN0cmluZ3NcbiAgICAgKiBCYXNlIGJlaGF2aW91cjogbGVmdCBhcnJvdyB3aWxsIG1vdmUgYmFjayBpbiBoaXN0b3J5LCByaWdodCBhcnJvdyBtb3ZlcyBmb3J3YXJkIGlmIHBvc3NpYmxlXG4gICAgICogU2hvdWxkIGJlIGNhbGxlZCBpbiBzdXBlciBmb3IgYWxsIHdpbmRvd3MgdGhhdCBjYW4gYmUgdHJhdmVyc2VkIGJhY2sgZnJvbS5cbiAgICAgKi9cbiAgICBoYW5kbGVJbnB1dChldmVudCkge1xuICAgICAgICAvLyB0byBiZSBpbXBsZW1lbnRlZCBpbiBzdWJjbGFzc2VzXG4gICAgfVxuICAgIC8qKlxuICAgICAqIEhhbmRsZSBhIHRleHQgaW5wdXQgZmllbGQgYmVpbmcgc3VibWl0dGVkIHRvIHRoaXMgd2luZG93LlxuICAgICAqIEBwYXJhbSB0ZXh0IHRoZSB0ZXh0IHRoYXQgd2FzIHN1Ym1pdHRlZFxuICAgICAqL1xuICAgIGhhbmRsZVRleHRTdWJtaXQodGV4dCkge1xuICAgICAgICBhbGVydChcInN1Ym1pdHRlZCBcIiArIHRleHQpO1xuICAgIH1cbiAgICBzaG93VG9hc3QodG9hc3QpIHtcbiAgICAgICAgdGhpcy50b2FzdC5pbm5lckhUTUwgPSB0b2FzdCArIFwiPGJyPlwiO1xuICAgIH1cbiAgICAvKipcbiAgICAgKiBHbyB0byBhbm90aGVyIHdpbmRvdyBGUk9NIHRoaXMgd2luZG93LlxuICAgICAqIEhhcyBzb21lIGV4dHJhIGZ1bmN0aW9uYWxpdHkgc3VjaCBhcyBjbGVhcmluZyBjdXJyZW50IHRvYXN0LlxuICAgICAqIEBwYXJhbSB3aW5kb3cgdGhlIHdpbmRvdyB0byBuYXZpZ2F0ZSB0b1xuICAgICAqL1xuICAgIGdvdG8od2luZG93KSB7XG4gICAgICAgIHRoaXMudG9hc3QuaW5uZXJIVE1MID0gXCJcIjtcbiAgICAgICAgZ290b1dpbmRvdyh3aW5kb3cpO1xuICAgIH1cbn1cbmV4cG9ydCBjbGFzcyBJbmRleGVkRWxlbWVudFdpbmRvdyBleHRlbmRzIFdpbmRvdyB7XG4gICAgY29uc3RydWN0b3IocGF0aCkge1xuICAgICAgICBzdXBlcihwYXRoKTtcbiAgICAgICAgdGhpcy5kaXJlY3Rpb24gPSBcImxlZnQtcmlnaHRcIjtcbiAgICAgICAgdGhpcy5zZWxlY3RlZEluZGV4ID0gMDtcbiAgICAgICAgdGhpcy5zZWxlY3RhYmxlRWxlbWVudHMgPSBbXTtcbiAgICB9XG4gICAgZGlzcGxheSgpIHtcbiAgICAgICAgc3VwZXIuZGlzcGxheSgpO1xuICAgICAgICAvLyBjbGVhcnMgYW55IGV4aXN0aW5nIHNlbGVjdGFibGUgZWxlbWVudHMgKHRoaXMgaXMgYmVpbmcgcmVkcmF3bilcbiAgICAgICAgdGhpcy5zZWxlY3RhYmxlRWxlbWVudHMgPSBbXTtcbiAgICB9XG4gICAgaGFuZGxlSW5wdXQoZXZlbnQpIHtcbiAgICAgICAgLy8gbGVmdCAtIGdvIGJhY2sgYSB3aW5kb3cgKGZyb20gc3VwZXIpXG4gICAgICAgIHN1cGVyLmhhbmRsZUlucHV0KGV2ZW50KTtcbiAgICAgICAgdGhpcy5oYW5kbGVBcnJvd0tleXMoZXZlbnQpO1xuICAgICAgICAvLyBlbnRlciAtIHNlbGVjdCBjdXJyZW50IHNlbGVjdGVkIGN1cnNvciBjaG9pY2VcbiAgICAgICAgaWYgKGV2ZW50LmNvZGUgPT09IFwiRW50ZXJcIikge1xuICAgICAgICAgICAgdGhpcy5oYW5kbGVFbGVtZW50UHJlc3NlZCh0aGlzLnNlbGVjdGFibGVFbGVtZW50c1t0aGlzLnNlbGVjdGVkSW5kZXhdLCB0aGlzLnNlbGVjdGVkSW5kZXgpO1xuICAgICAgICB9XG4gICAgfVxuICAgIC8qKlxuICAgICAqIE1vdmVzIHRoZSBjdXJzb3IuXG4gICAgICogQHBhcmFtIGV2ZW50IGtleWJvYXJkIGV2ZW50XG4gICAgICogQHJldHVybnMgdHJ1ZSBpZiBhbiBhcnJvdyBrZXkgaW5wdXQgd2FzIGhhbmRsZWRcbiAgICAgKi9cbiAgICBoYW5kbGVBcnJvd0tleXMoZXZlbnQpIHtcbiAgICAgICAgLy8gcmlnaHQvbGVmdCAtIG1vdmUgY2hvaWNlIGN1cnNvclxuICAgICAgICBpZiAoZXZlbnQuY29kZSA9PT0gKHRoaXMuZGlyZWN0aW9uID09PSBcInRvcC1ib3R0b21cIiA/ICdBcnJvd1VwJyA6ICdBcnJvd0xlZnQnKSAmJiB0aGlzLnNlbGVjdGVkSW5kZXggPiAwKSB7XG4gICAgICAgICAgICB0aGlzLm1vdmVTZWxlY3Rpb24oLTEpO1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGV2ZW50LmNvZGUgPT09ICh0aGlzLmRpcmVjdGlvbiA9PT0gXCJ0b3AtYm90dG9tXCIgPyAnQXJyb3dEb3duJyA6ICdBcnJvd1JpZ2h0JykgJiYgdGhpcy5zZWxlY3RlZEluZGV4ICsgMSA8IHRoaXMuc2VsZWN0YWJsZUVsZW1lbnRzLmxlbmd0aCkge1xuICAgICAgICAgICAgdGhpcy5tb3ZlU2VsZWN0aW9uKDEpO1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICBzZXRTZWxlY3Rpb24oaW5kZXgpIHtcbiAgICAgICAgdGhpcy5oYW5kbGVFbGVtZW50RGVzZWxlY3RlZCh0aGlzLnNlbGVjdGFibGVFbGVtZW50c1t0aGlzLnNlbGVjdGVkSW5kZXhdLCB0aGlzLnNlbGVjdGVkSW5kZXgpO1xuICAgICAgICB0aGlzLnNlbGVjdGVkSW5kZXggPSBpbmRleDtcbiAgICAgICAgdGhpcy5oYW5kbGVFbGVtZW50U2VsZWN0ZWQodGhpcy5zZWxlY3RhYmxlRWxlbWVudHNbdGhpcy5zZWxlY3RlZEluZGV4XSwgdGhpcy5zZWxlY3RlZEluZGV4KTtcbiAgICB9XG4gICAgbW92ZVNlbGVjdGlvbihkZWx0YSkge1xuICAgICAgICB0aGlzLnNldFNlbGVjdGlvbih0aGlzLnNlbGVjdGVkSW5kZXggKyBkZWx0YSk7XG4gICAgfVxuICAgIGhhbmRsZUVsZW1lbnREZXNlbGVjdGVkKGVsZW1lbnQsIGluZGV4KSB7XG4gICAgICAgIGRvY3VtZW50LmJvZHkuZm9jdXMoKTtcbiAgICAgICAgZWxlbWVudC5jbGFzc0xpc3QucmVtb3ZlKFwiYmlwb2xlLWN1cnNvclwiKTtcbiAgICAgICAgLy8gZnVydGhlciBiZWhhdmlvdXIgdG8gYmUgaW1wbGVtZW50ZWQgaW4gc3ViY2xhc3Nlc1xuICAgIH1cbiAgICBoYW5kbGVFbGVtZW50U2VsZWN0ZWQoZWxlbWVudCwgaW5kZXgpIHtcbiAgICAgICAgZWxlbWVudC5jbGFzc0xpc3QuYWRkKFwiYmlwb2xlLWN1cnNvclwiKTtcbiAgICAgICAgLy8gZnVydGhlciBiZWhhdmlvdXIgdG8gYmUgaW1wbGVtZW50ZWQgaW4gc3ViY2xhc3Nlc1xuICAgIH1cbiAgICBoYW5kbGVFbGVtZW50UHJlc3NlZChlbGVtZW50LCBpbmRleCkge1xuICAgICAgICBpZiAoZWxlbWVudC5vbmNsaWNrKVxuICAgICAgICAgICAgZWxlbWVudC5vbmNsaWNrKG51bGwpO1xuICAgICAgICAvLyBmdXJ0aGVyIGJlaGF2aW91ciB0byBiZSBpbXBsZW1lbnRlZCBpbiBzdWJjbGFzc2VzXG4gICAgfVxufVxuZXhwb3J0IGNvbnN0IHVuaXZlcnNhbEJhY2sgPSAobmFtZSA9IFwiQmFja1wiKSA9PiB7XG4gICAgcmV0dXJuIHsgaW5wdXQ6IFtcIlhcIiwgXCJLZXlYXCIsIFwiS2V5TlwiXSwgbGFiZWw6IG5hbWUsIGVmZmVjdDogKCkgPT4gYmFjaygpIH07XG59O1xuZXhwb3J0IGNsYXNzIENob2ljZU1lbnUgZXh0ZW5kcyBJbmRleGVkRWxlbWVudFdpbmRvdyB7XG4gICAgY29uc3RydWN0b3IocGF0aCwgY2hvaWNlcyA9IFtdLCBwcm9tcHQgPSBudWxsKSB7XG4gICAgICAgIHN1cGVyKHBhdGgpO1xuICAgICAgICB0aGlzLmNob2ljZXMgPSBjaG9pY2VzO1xuICAgICAgICB0aGlzLnByb21wdCA9IHByb21wdDtcbiAgICB9XG4gICAgZGlzcGxheSgpIHtcbiAgICAgICAgc3VwZXIuZGlzcGxheSgpO1xuICAgICAgICB0aGlzLmRpc3BsYXlBYm92ZUNob2ljZXMoKTtcbiAgICAgICAgdGhpcy5kaXNwbGF5Q2hvaWNlcygpO1xuICAgICAgICB0aGlzLnNldFNlbGVjdGlvbigwKTtcbiAgICB9XG4gICAgZGlzcGxheUFib3ZlQ2hvaWNlcygpIHtcbiAgICAgICAgaWYgKHRoaXMucHJvbXB0KVxuICAgICAgICAgICAgbGluZSh0aGlzLnByb21wdCk7XG4gICAgfVxuICAgIGRpc3BsYXlDaG9pY2VzKCkge1xuICAgICAgICBsZXQgbGlzdEVsZW1lbnQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICBsaXN0RWxlbWVudC5jbGFzc0xpc3QuYWRkKFwiYXNjaWlcIik7XG4gICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy5jaG9pY2VzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBjb25zdCBjaG9pY2UgPSB0aGlzLmNob2ljZXNbaV07XG4gICAgICAgICAgICBsZXQgYnV0dG9uRWxlbSA9IGJ1dHRvbihgWyR7Y2hvaWNlLmlucHV0WzBdfV0gJHtjaG9pY2UubGFiZWx9YCwgKCkgPT4gY2hvaWNlLmVmZmVjdCgpKTtcbiAgICAgICAgICAgIG91dHB1dC5hcHBlbmQoYnV0dG9uRWxlbSk7XG4gICAgICAgICAgICB0aGlzLnNlbGVjdGFibGVFbGVtZW50cy5wdXNoKGJ1dHRvbkVsZW0pO1xuICAgICAgICB9XG4gICAgICAgIG91dHB1dC5hcHBlbmQobGlzdEVsZW1lbnQpO1xuICAgIH1cbiAgICBhZGRDaG9pY2UoY2hvaWNlKSB7XG4gICAgICAgIHRoaXMuY2hvaWNlcy5wdXNoKGNob2ljZSk7XG4gICAgfVxuICAgIGhhbmRsZUlucHV0KGV2ZW50KSB7XG4gICAgICAgIHN1cGVyLmhhbmRsZUlucHV0KGV2ZW50KTtcbiAgICAgICAgZm9yIChsZXQgY2hvaWNlIG9mIHRoaXMuY2hvaWNlcykge1xuICAgICAgICAgICAgZm9yIChsZXQgaW5wdXRDb2RlIG9mIGNob2ljZS5pbnB1dCkge1xuICAgICAgICAgICAgICAgIGlmIChldmVudC5jb2RlID09PSBpbnB1dENvZGUgfHwgZXZlbnQua2V5ID09PSBpbnB1dENvZGUpIHtcbiAgICAgICAgICAgICAgICAgICAgY2hvaWNlLmVmZmVjdCgpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxufVxuZXhwb3J0IGNsYXNzIFRleHRJbnB1dE1lbnUgZXh0ZW5kcyBDaG9pY2VNZW51IHtcbiAgICBjb25zdHJ1Y3RvcihpZCwgcHJvbXB0KSB7XG4gICAgICAgIHN1cGVyKGlkKTtcbiAgICAgICAgdGhpcy5tYXhsZW5ndGggPSAwO1xuICAgICAgICB0aGlzLnByb21wdCA9IHByb21wdDtcbiAgICB9XG4gICAgZGlzcGxheUFib3ZlQ2hvaWNlcygpIHtcbiAgICAgICAgc3VwZXIuZGlzcGxheUFib3ZlQ2hvaWNlcygpO1xuICAgICAgICB0aGlzLmRpc3BsYXlUZXh0SW5wdXQoKTtcbiAgICB9XG4gICAgZGlzcGxheVRleHRJbnB1dCgpIHtcbiAgICAgICAgbGV0IHByb21wdEVsZW0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICBvdXRwdXQuYXBwZW5kKHByb21wdEVsZW0pO1xuICAgICAgICB0aGlzLnNlbGVjdGFibGVFbGVtZW50cy5wdXNoKHByb21wdEVsZW0pO1xuICAgICAgICBwcm9tcHRFbGVtLmNsYXNzTGlzdC5hZGQoXCJiaXBvbGUtcHJvbXB0XCIpO1xuICAgICAgICBsZXQgcG9pbnRlckVsZW0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwic3BhblwiKTtcbiAgICAgICAgcHJvbXB0RWxlbS5hcHBlbmQocG9pbnRlckVsZW0pO1xuICAgICAgICBwb2ludGVyRWxlbS5jbGFzc0xpc3QuYWRkKFwiYmlwb2xlLXBvaW50ZXJcIik7XG4gICAgICAgIHBvaW50ZXJFbGVtLmlubmVySFRNTCA9IFwiPiBcIjtcbiAgICAgICAgdGhpcy5pbnB1dEVsZW0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW5wdXRcIik7XG4gICAgICAgIHByb21wdEVsZW0uYXBwZW5kKHRoaXMuaW5wdXRFbGVtKTtcbiAgICAgICAgdGhpcy5pbnB1dEVsZW0udHlwZSA9IFwidGV4dFwiO1xuICAgICAgICB0aGlzLmlucHV0RWxlbS5wbGFjZWhvbGRlciA9IFwiTGVhZFwiO1xuICAgICAgICB0aGlzLmlucHV0RWxlbS5jbGFzc0xpc3QuYWRkKFwiYmlwb2xlLXByb21wdC1pbnB1dFwiKTtcbiAgICAgICAgbGV0IHRoaXNXaW5kb3cgPSB0aGlzO1xuICAgICAgICBsZXQgaWUgPSB0aGlzLmlucHV0RWxlbTtcbiAgICAgICAgdGhpcy5pbnB1dEVsZW0ub25rZXlkb3duID0gZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgICAgICAgICBpZiAodGhpc1dpbmRvdy5oYW5kbGVBcnJvd0tleXMoZXZlbnQpKVxuICAgICAgICAgICAgICAgIGllLmJsdXIoKTtcbiAgICAgICAgICAgIGlmIChldmVudC5jb2RlID09PSAnRW50ZXInKSB7XG4gICAgICAgICAgICAgICAgaGFuZGxlVGV4dFN1Ym1pdChpZS52YWx1ZSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICAgICAgICBpZiAoaWUudmFsdWUubGVuZ3RoID4gMjQpIHtcbiAgICAgICAgICAgICAgICAgICAgaWUuY2xhc3NMaXN0LmFkZChcImJpcG9sZS1lcnJvclwiKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIGllLmNsYXNzTGlzdC5yZW1vdmUoXCJiaXBvbGUtZXJyb3JcIik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSwgMCk7XG4gICAgICAgIH07XG4gICAgfVxuICAgIGhhbmRsZUlucHV0KGV2ZW50KSB7XG4gICAgICAgIHN1cGVyLmhhbmRsZUlucHV0KGV2ZW50KTtcbiAgICB9XG4gICAgaGFuZGxlRWxlbWVudFNlbGVjdGVkKGVsZW1lbnQsIGluZGV4KSB7XG4gICAgICAgIHN1cGVyLmhhbmRsZUVsZW1lbnRTZWxlY3RlZChlbGVtZW50LCBpbmRleCk7XG4gICAgICAgIC8vIElmIHRoZSB0ZXh0IGJveCB3YXMgc2VsZWN0ZWQsIHBsYWNlIGN1cnNvciBpbiBpdFxuICAgICAgICBpZiAoaW5kZXggPT09IDApIHtcbiAgICAgICAgICAgIC8vIGJlY2F1c2UgYnJvd3NlciBpcyBiZWluZyBxdWlya3ksIGFkZGluZywgYSB0aW1lb3V0IGhlcmUgdG8gd2FpdCBmb3Igb3RoZXIgZXZlbnRzXG4gICAgICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHRoaXMuaW5wdXRFbGVtLmZvY3VzKCksIDApO1xuICAgICAgICB9XG4gICAgfVxufVxuIiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXShtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIi8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb25zIGZvciBoYXJtb255IGV4cG9ydHNcbl9fd2VicGFja19yZXF1aXJlX18uZCA9IChleHBvcnRzLCBkZWZpbml0aW9uKSA9PiB7XG5cdGZvcih2YXIga2V5IGluIGRlZmluaXRpb24pIHtcblx0XHRpZihfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZGVmaW5pdGlvbiwga2V5KSAmJiAhX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIGtleSkpIHtcblx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBrZXksIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBkZWZpbml0aW9uW2tleV0gfSk7XG5cdFx0fVxuXHR9XG59OyIsIl9fd2VicGFja19yZXF1aXJlX18ubyA9IChvYmosIHByb3ApID0+IChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqLCBwcm9wKSkiLCIvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG5fX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSAoZXhwb3J0cykgPT4ge1xuXHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcblx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcblx0fVxuXHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xufTsiLCIiLCIvLyBzdGFydHVwXG4vLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbi8vIFRoaXMgZW50cnkgbW9kdWxlIGlzIHJlZmVyZW5jZWQgYnkgb3RoZXIgbW9kdWxlcyBzbyBpdCBjYW4ndCBiZSBpbmxpbmVkXG52YXIgX193ZWJwYWNrX2V4cG9ydHNfXyA9IF9fd2VicGFja19yZXF1aXJlX18oXCIuL3NyYy9pbmRleC50c1wiKTtcbiIsIiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==
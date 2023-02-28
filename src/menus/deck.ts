import { clear, line, space } from "../display";
import { save } from "../user";
import { Window } from "../window";
import { CardWindow } from "../windowtypes/cardwindow";

export class DeckMenu extends Window {
    deckWindow: CardWindow
    collectionWindow: CardWindow
    cursorInDeck = true

    constructor() {
        super()
    }

    display(out: HTMLElement): void {
        super.display(out)

        this.displayCards(out);

        this.deckWindow.setSelection(0, 0)
    }

    displayCards(out: HTMLElement) {
        line("Deck", out)
        this.deckWindow = new CardWindow(() => save.deck, (card) => {
            if (card.sendToCollection()) {
                this.refresh(out)
            } else {
                this.showToast(`Deck cannot have less than ${save.minDeckSize} cards`)
            }
        })
        this.deckWindow.display(out)
        this.deckWindow.handleCursorOverflow = (rowDelta, colDelta) => {
            if (rowDelta === 1 && this.collectionWindow.selectableElements[0].length > 0) {
                this.cursorInDeck = false;
                this.deckWindow.removeSelection()
                this.collectionWindow.setSelection(0, this.deckWindow.selectedCol)
                return true;
            } else return false;
        }

        space(out)
        line("Collection", out)
        this.collectionWindow = new CardWindow(() => save.collection, (card) => {
            if (card.sendToDeck()) {
                this.refresh(out)
            } else {
                this.showToast(`Deck cannot have more than ${save.maxDeckSize} cards`)
            }
        }
            )
        this.collectionWindow.display(out)
        this.collectionWindow.handleCursorOverflow = (rowDelta, colDelta) => {
            if (rowDelta === -1 && this.deckWindow.selectableElements[0].length > 0) {
                this.cursorInDeck = true;
                this.collectionWindow.removeSelection()
                this.deckWindow.setSelection(this.deckWindow.selectableElements.length-1, this.collectionWindow.selectedCol)
                return true;
            } else return false;
        }
    }

    handleInput(event: KeyboardEvent): void {
        if (this.cursorInDeck) {
            this.deckWindow.handleInput(event)
        } else {
            this.collectionWindow.handleInput(event)
        }
    }
    
    refresh(out: HTMLElement): void {
        if (this.cursorInDeck) {
            let row = this.deckWindow.selectedRow;
            let col = this.deckWindow.selectedCol;
            clear(out)
            this.displayCards(out);
            if (!this.deckWindow.setSelection(row, col)) {
                this.cursorInDeck = false;
                this.collectionWindow.setSelection(0, 0)
            }
        } else {
            let row = this.collectionWindow.selectedRow;
            let col = this.collectionWindow.selectedCol;
            clear(out)
            this.displayCards(out);
            if (!this.collectionWindow.setSelection(row, col)) {
                this.cursorInDeck = true;
                this.deckWindow.setSelection(0, 0)
            }
        }
    }
}
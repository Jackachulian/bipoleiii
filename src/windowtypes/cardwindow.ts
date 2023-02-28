import { Card } from "../card";
import { save } from "../user";
import { GridElementWindow } from "./grid";

/**
 * Displays a collection of cards, such as a deck, hand, discard pile, etc.
 */
export class CardWindow extends GridElementWindow {
    /** The list of cards this window is displaying. */
    cardsToDisplay: () => Card[]
    /** Function when cards are clicked/selected. */
    cardSelect: (card: Card) => void
    /** Current list that is displayed */
    cards: Card[]

    colCount = 4

    constructor(cardsToDisplay: () => Card[], cardSelect: (card: Card) => void) {
        super();
        this.cardsToDisplay = cardsToDisplay;
        this.cardSelect = cardSelect;
    }

    display(out: HTMLElement): void {
        super.display(out);

        this.cards = this.cardsToDisplay();

        let row = 0;
        let rowElem = document.createElement("div");
        this.selectableElements = [[]]

        console.log(this.cards)
        for (let card of this.cards) {
            if (this.selectableElements[row].length >= this.colCount) {
                row++;
                out.appendChild(rowElem);
                rowElem = document.createElement("div");
                this.selectableElements.push([])
            }

            let cardElem = card.createElement()
            cardElem.onclick = () => this.cardSelect(card);
            this.selectableElements[row].push(cardElem)
            out.appendChild(cardElem);
        }

        out.appendChild(rowElem);
    }
}
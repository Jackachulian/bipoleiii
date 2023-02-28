import { Battler } from "./battle"
import { save } from "./user"

/** Information that a card uses. */
export type CardData = {
    /** Display name of the card */
    name: string
    /** Description of the card's effect */
    description: string
    /** Cost to use this card in LE. */
    cost: number
    /** Cost to use this card in MP. */
    mpCost: number
    /** Miscellaneous properties on this object used in effects. */
    props: Object
    /** Effect when using the card. */
    effect: (user: Battler, target: Battler) => void
}

export class Card {
    data: CardData

    constructor(data: CardData) {
        this.data = data
    }

    sendToDeck(): boolean {
        if (save.deck.length >= save.maxDeckSize) return false;
        save.collection.splice(save.collection.findIndex((c) => c === this), 1)
        save.deck.push(this)
        return true;
    }

    sendToCollection(): boolean {
        if (save.deck.length <= save.minDeckSize) return false;
        save.deck.splice(save.deck.findIndex((c) => c === this), 1)
        save.collection.push(this)
        return true;
    }

    createElement(): HTMLElement {
        let lines: string[] = []
        let currentLine = ""
        for (let word of this.data.description.split(" ")) {
            if (word.length + currentLine.length > 13) {
                lines.push(currentLine)
                currentLine = ""
            }
            while (word.length + currentLine.length > 13) {
                lines.push(word.substring(0, 12)+"-")
                word = word.substring(12)
            }
            currentLine = currentLine + " "+word;
        }

        // Add remaining line and fill with empty lines
        lines.push(currentLine)
        while (lines.length < 5) {
            lines.push(" ")
        }

        let text = `<span class="bipole-card-cursor">0-</span>              <span class="bipole-card-cursor">-0</span>
<span class="bipole-card-cursor">|</span>/--------------\\<span class="bipole-card-cursor">|</span>
 | ${this.data.name.padEnd(10, " ")} ${this.data.cost} | 
 |              | 
`

        for (let line of lines) {
            text += ` |${line.padEnd(13, " ")} | 
`
        }
        text += `<span class="bipole-card-cursor">|</span>\\--------------/<span class="bipole-card-cursor">|</span>
<span class="bipole-card-cursor">0-</span>              <span class="bipole-card-cursor">-0</span>`

        let elem = document.createElement("div")
        elem.classList.add("bipole-card")
        elem.innerHTML = text;
        return elem;
    }
}

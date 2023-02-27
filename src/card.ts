import { Battler } from "./battle"

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

    createElement(): HTMLElement {
        let lines: string[] = []
        let currentLine = ""
        for (let word in this.data.description.split(" ")) {
            if (word.length + currentLine.length > 13) {
                lines.push(currentLine)
                currentLine = ""
            }
            while (word.length + currentLine.length > 13) {
                lines.push(word.substring(0, 12)+"-")
                word = word.substring(12)
            }
            currentLine = currentLine + word;
        }

        let text = `+---------------+
| ${this.data.name.padEnd(13, " ")} |
|               |
`

        for (let line in lines) {
            text += `| ${line.padEnd(13, " ")} |
`
        }
        text += "+---------------+"

        let elem = document.createElement("div")
        elem.classList.add("bipole-card")
        elem.innerHTML = text;
        return elem;
    }
}

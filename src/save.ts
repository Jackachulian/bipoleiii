import { Card, CardData } from "./card";
import { fireball, punch } from "./data/cards";

/**
 * Stores all save data information for a single save.
 */
export default class Save {
    name: string
    hp: number
    maxHp: number
    deck: Card[]

    /**
     * Create a new save file
     * @param name The player's name
     */
    constructor(name: string) {
        this.name = name;
        this.deck = []
    }

    addToDeck(data: CardData) {
        this.deck.push(new Card(data))
    }
}

export function newSave(name: string): Save {
    let save = new Save(name);
    save.maxHp = 100;
    save.hp = 100;
    save.addToDeck(punch)
    save.addToDeck(punch)
    save.addToDeck(punch)
    save.addToDeck(fireball)
    return save;
}  
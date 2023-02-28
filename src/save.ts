import { Card, CardData } from "./card";
import { fireball, punch } from "./data/cards";

/**
 * Stores all save data information for a single save.
 */
export default class Save {
    name: string
    hp: number
    maxHp: number

    deck: Card[] = []
    minDeckSize: number = 3;
    maxDeckSize: number = 5
    collection: Card[] = []

    /**
     * Create a new save file
     * @param name The player's name
     */
    constructor(name: string) {
        this.name = name;
    }

    addToDeck(data: CardData): boolean {
        if (this.deck.length >= this.maxDeckSize) return false;
        this.deck.push(new Card(data))
        return true;
    }

    addToCollection(data: CardData): boolean {
        if (this.deck.length <= this.minDeckSize) return false;
        this.collection.push(new Card(data))
        return true;
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
    save.addToCollection(punch)
    save.addToCollection(punch)
    save.addToCollection(fireball)
    save.addToCollection(punch)
    save.addToCollection(punch)
    save.addToCollection(fireball)
    return save;
}  
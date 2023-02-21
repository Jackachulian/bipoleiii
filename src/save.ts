/**
 * Stores all save data information for a single save.
 */
export default class Save {
    name: string
    hp: number
    maxHp: number

    /**
     * Create a new save file
     * @param name The player's name
     */
    constructor(name: string) {
        this.name = name;

        this.hp = 100
        this.maxHp = 100
    }
}
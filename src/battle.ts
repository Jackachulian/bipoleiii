import { Card } from "./card";

export type BattlerData = {
    name: string;
    maxHp: number;
}

/** Any fighter in a battle; both the user and the enemies. */
export class Battler {
    data: BattlerData
    hp: number
    maxHp: number
    deck: Card[]
    hand: Card[]
    discard: Card[]

    constructor(data: BattlerData) {
        this.data = data;
    }

    /** Initiialize this battler. Should be run before battle logic begins */
    initialize() {
        this.maxHp = this.data.maxHp;
        this.hp = this.data.maxHp;

        this.deck = []
        this.hand = []
        this.discard = []
    }

    /** Deal damage to another battler. */
    dealDamage(target: Battler, damage: number) {
        target.takeDamage(this, damage)
    }

    /** Take damage from another battler. */
    private takeDamage(attacker: Battler, damage: number) {
        this.hp -= damage;
        // TODO: on death
    }
}
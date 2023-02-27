import { CardData } from "../card";

export const punch: CardData = {
    name: "Punch",
    description: "Deal {dmg} damage.",
    cost: 1, mpCost: 0,
    props: {damage: 1},
    effect: (user, target) => user.dealDamage(target, 1)
}

export const fireball: CardData = {
    name: "Fireball",
    description: "Deal {dmg} damage. May burn the target.",
    cost: 0, mpCost: 2,
    props: {damage: 2},
    effect: (user, target) => user.dealDamage(target, 1)
}
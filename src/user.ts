import Save, { newSave } from "./save"

export type UserSettings = {
    textSpeed: "slow" | "normal" | "fast" | "instant"
    textAuto: boolean
}

export const settings: UserSettings = {
    textSpeed: "normal",
    textAuto: false
}

export let save: Save | null = null

export function loadSave(loadedSave: Save) {
    save = loadedSave;
}
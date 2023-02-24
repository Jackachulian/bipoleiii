export type UserSettings = {
    textSpeed: "slow" | "normal" | "fast" | "instant"
    textAuto: boolean
}

export const settings: UserSettings = {
    textSpeed: "normal",
    textAuto: false
}
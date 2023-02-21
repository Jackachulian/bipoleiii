export function loadCutscene(name: string) {
    fetch(`./cutscenes/${name}.txt`)
    .then((data) => console.log(data.text()));
}
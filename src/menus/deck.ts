import { save } from "../user";
import { IndexedElementWindow } from "../windowtypes/indexedelement";

export class DeckMenu extends IndexedElementWindow {
    constructor(path: string) {
        super(path);
        this.direction = "top-bottom"
    }

    display(): void {
        super.display();

        
    }
}
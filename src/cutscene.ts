import { gotoWindow } from "./index";
import { settings } from "./user";
import { Window } from "./window";
import { ChoiceMenu } from "./windowtypes/choice";

export class CutsceneWindow extends ChoiceMenu {
    name: string
    cut: HTMLElement
    node: ChildNode
    currentNodeText: string
    outputNode: HTMLElement;
    nodeIndex: number
    nodeCharIndex: number
    writing: boolean
    charDelay: number
    charDelayMult: number
    out: HTMLElement

    /** Set to true when {noinput} is read. Doesn't wait for user input on the next <br>. */
    noInput: boolean

    /** List of the indexes of all labels, saved at the start of the cutscene, used in gotos */
    labels: Map<string, number>

    /** If the user is currently making a choice. Prevents enter move to next while during. */
    makingChoice: boolean

    /** Window to show after this cutscene is done. */
    displayAfter: Window

    static parser: DOMParser = new DOMParser();

    constructor(name: string, displayAfter: Window) {
        super()
        this.name = name;
        this.displayAfter = displayAfter;
        this.nodeIndex = 0;
        this.nodeCharIndex = 0;

        this.writing = false;
        this.charDelayMult = 1
        this.makingChoice = false;
    }

    display(out: HTMLElement) {
        this.out = out;
        super.display(out);
        this.playCutscene();
    }

    async playCutscene() {
        const response = await fetch(`./cutscenes/${this.name}.html`);
        const data = await response.text();

        this.cut = CutsceneWindow.parser.parseFromString(data, 'text/html').body;
        // this.cut.classList.add("bipole-cutscene");

        console.log(this.cut)
        console.log(this.cut.childNodes)

        this.labels = new Map();
        for (let i=0; i<this.cut.childNodes.length; i++) {
            let node = this.cut.childNodes[i];
            if (node.nodeName.toLowerCase() === "label") {
                this.labels.set(node.textContent, i);
            }
        }

        this.updateCharDelay()

        this.parseNode()
    }

    parseNode() {
        // if last node reached, display next window
        if (this.nodeIndex >= this.cut.childNodes.length) {
            this.writing = false;
            gotoWindow(this.displayAfter)
            return;
        }

        this.writing = true;
        this.node = this.cut.childNodes[this.nodeIndex]
        this.currentNodeText = this.node.textContent;
        this.currentNodeText = this.currentNodeText.replace("{name}", "Lead") // TODO: dynamic variables

        if (this.node.nodeName === "#text") {
            this.outputNode = document.createElement("span");
        } else {
            this.outputNode = document.createElement(this.node.nodeName);

            // If the node is not an HTMLelement, classes should be undefined
            let className = (this.node as HTMLElement).className;
            if (className) {
                this.outputNode.className = className;
            }

            // If new node is a label, ignore it
            if (this.node.nodeName.toLowerCase() === "label") {
                this.nodeIndex++;
                this.parseNode(); return;
            }

            // If this is a goto, go to the label (specifically the node after it)
            if (this.node.nodeName.toLowerCase() === "goto") {
                this.gotoLabel(this.node.textContent);
                return;
            }

            // If this is a choice, print the choice & wait for input
            if (this.node.nodeName.toLowerCase() === "choice") {
                this.choices = []

                let choiceStrings = this.node.textContent.split(" ")
                for (let choiceString of choiceStrings) {
                    let params = choiceString.split(",")
                    console.log(params)
                    this.choices.push({input: [params[0]], label: params[2], effect: () => this.makeChoice(params[1])})
                }

                this.makingChoice = true;
                this.writing = false;
                this.displayChoices(this.out);
                this.setSelection(0);
                return;
            }
        }
        this.outputNode.scrollIntoView();
        this.out.append(this.outputNode)

        this.parseNodeByChar()
    }

    makeChoice(label: string) {
        console.log("choice made: "+label)
        this.makingChoice = false;
        this.gotoLabel(label);
    }

    gotoLabel(label: string) {
        this.nodeIndex = this.labels.get(label)+1;
        this.parseNode()
    }

    parseNodeByChar() {
        // If not writing anymore user hit enter to inistant finish current line, so don't write anymore
        if (!this.writing) return;

        // If character is a {, parse the input
        if (this.currentNodeText.charAt(this.nodeCharIndex) === "{") {
            let bracketEnd = this.currentNodeText.indexOf("}", this.nodeCharIndex)
            let insideBrackets = this.currentNodeText.substring(this.nodeCharIndex+1, bracketEnd)
            
            let params = insideBrackets.split("=");
            if (params[0] === "noinput") {
                this.noInput = true;
            } else if (params[0] === "delay") {
                this.charDelayMult = parseFloat(params[1])
            }

            this.nodeCharIndex = bracketEnd+1;
        }

        // Add next char to the current element
        this.outputNode.innerHTML += this.currentNodeText.charAt(this.nodeCharIndex);
        this.nodeCharIndex++;

        if (this.nodeCharIndex >= this.currentNodeText.length) {
            // End of the node has been reached
            this.nodeCharIndex = 0
            this.nodeIndex++

            if (this.nodeIndex >= this.cut.childNodes.length) {
                this.writing = false;
                return;
            }

            // If this is a line break
            if (this.node.nodeName.toLowerCase() === "br") {
                // stop writing - waits for user input
                this.writing = false;
                
                // if auto, start next node after a delay, along with waiting for input
                if (settings.textAuto) {
                    setTimeout(() => this.parseNode(), 1500)
                }

                return
            }

            // if not stopped at linebreak or not end of file, start next node
            this.parseNode();
            return;
        } 
        
        else {
             // If not stopped at line break / file ended, write next after a delay
            setTimeout(() => this.parseNodeByChar(), this.charDelay*this.charDelayMult)
        }
    }

    updateCharDelay() {
        if (settings.textSpeed === "slow") {
            this.charDelay = 50;
        } else if (settings.textSpeed === "normal") {
            this.charDelay = 35;
        } else if (settings.textSpeed === "fast") {
            this.charDelay = 20;
        }
        // If speed is instant, parseNode will know from settings and write whole line at once
    }

    handleInput(event: KeyboardEvent): void {
        if (this.makingChoice) {
            super.handleInput(event);
        }

        else if (event.code === "Enter" || event.code === "Space") {
            // TODO: If writing, finish nodes until BR reached
            if (this.writing) {
                // finish current node (ignore commands)
                this.outputNode.innerHTML = this.currentNodeText // TODO: ignore commands
                this.nodeIndex++;
                this.nodeCharIndex = 0;

                // will break loop when the element added is a BR or end of file reached
                while (true) {
                    this.node = this.cut.childNodes[this.nodeIndex]
                    this.currentNodeText = this.node.textContent;
                    this.currentNodeText = this.currentNodeText.replace("{name}", "Lead") // TODO: dynamic variables
                    if (this.node.nodeName === "#text") {
                        this.outputNode = document.createElement("span");
                    } else {
                        this.outputNode = document.createElement(this.node.nodeName);

                        // If the node is not an HTMLelement, classes should be undefined
                        let className = (this.node as HTMLElement).className;
                        if (className) {
                            this.outputNode.className = className;
                        }
                    }
                    this.outputNode.innerHTML = this.currentNodeText;
                    this.out.append(this.outputNode)

                    this.nodeIndex++;
                    // stop looping when a BR is displayed or end is reached
                    if (this.node.nodeName === "BR" || this.nodeIndex >= this.cut.childNodes.length) break;
                }

                this.writing = false;
            } 
            
            // otherwise, start printing next node
            else {
                this.writing = true;
                this.parseNode();
            }
        }
    }
}
import time, re

import game as g

import client

from colors import TextCodes

choice = None
current_branch = None

def parse_line(l):
    global choice
    global current_branch

    params = l.split(" ")

    if params[0] == "if":
        current_branch = params[1]
        return
    elif params[0] == "end":
        current_branch = None
        return
    elif params[0] == "choiceend":
        choice = None
        return

    if current_branch: 
        if not current_branch == choice:
            return      #Do not continue if not on current choice branch.

    if params[0] == "choice":   #choice <format> <important> (choice)
        if params[1] == "yes_or_no":
            if params[2] == "0" and client.skip_cutscene:
                return

            text = " ".join(params[3:])
            choice = "yes" if client.entry(text) else "no"
        return

    if client.skip_cutscene:   #Skip headings, lines, waits and dialog if skip_cutscene is on
        return
    
    if params[0] == "heading":
        text = " ".join(params[1:])
        client.line(client.bold(text))

    elif params[0] == "line":
        time = float(params[1])
        text = " ".join(params[2:])
        client.line(text, time)

    elif params[0] == "wait":
        client.wait(float(params[1]))
        

    else:   #Dialog
        client.dialog(l)
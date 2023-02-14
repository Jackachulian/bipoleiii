# ---
# The root display file. Manages inputs and outputs to the console / whatever it's being displayed to.
# ALL inputs and outputs should pass through this file, so that this file's functions can be changed to match the platform it is ported to.
# ---

width = 50      #Width of dividers and such
ld = 1    #Line delay. The length (in seconds) of the standard status line

from time import sleep
import random, math, sys, re, os
import game as g

from colors import TextCodes as c

def set_line_delay(t):
    #Changes the delay between lines. Helpful for changing long strings of lines' delay.
    global ld
    ld = t

def set_width(w):
    width = w

def cb(s, n): #code between
    if type(n) == int:
        return f'\033[{n}m{s}\033[0m'
    elif type(n) == str:
        return str(getattr(c, n)) + str(s) + c.RESET

def bold(t):
    return c.BOLD + t + c.RESET

def italic(t):
    return c.ITALIC + t + c.RESET

def url(t):
    return c.URL + t + c.RESET

def line(x='', t=None, w=False, reset_end=True):
    #Output a single line, and then wait the specified amount (seconds).
    #Then, if w, wait for any input before proceeding
    if not x:   #Failsafe
        return

    if reset_end:  #by default, a nomral format is placed at the end of each line
        x += '{c.RESET}'
    print(cf(x))

    if g.game:
        time_mul = g.game.line_speed
    else:
        time_mul=1

    if t != None:
        wait(t*time_mul)
    else:
        wait(ld*time_mul)
    if w:      #If there should be a wait after
        entry('')

    
def wait(t):
    try:
        sleep(t)
    except KeyboardInterrupt:
        g.quick_save(keyinterrupt=True)
    
def cf(string):     #color format
    return string.format(c=c)

def entry(x, f="text", cancel=None, keyinterrupt=True):
    #Get an input from the player with the given prompt.
    while True:
        if f=="yes_or_no":
            x += " (Y/N)"

        inputted = False
        while not inputted:
            try:
                e = input(x+' ')
                inputted = True
            except KeyboardInterrupt:
                g.quick_save(keyinterrupt=keyinterrupt)
            except EOFError:
                sys.exit('Exiting Bipole III')

        if f=="yes_or_no":
            return True if e.lower()=="y" or e.lower()=="yes" or e.lower()=="1" else False
        else:
            return e


def divider(title=None, x=width, c="="):
    #Make a divider of x length. c to change the character, default is =.
    #Title to give it a title, will place it in the middle
    if title:
        title = ' '+title+' '
        x -= len(title) + 2
        x1 = round(x/2)
        x2 = x - x1
        line(str(c)*x1 + title + str(c)*x2, 0)
    else:
        line(str(c)*x, 0)

def numchoice(choices, ft="either", prompt='Choose one:', invalidprompt='Enter a number or name', cancellable=True, cancel_index=None, cancel_label=None, return_item=False, flist=None, return_list=None, rows=1):
    #Get a choice from the player. Responds to number indices and the name of the choice. Return the index of the choice they chose, unless return_item is true.
    
    if cancel_label:
        cadd = 0
        choice_list = [cancel_label]
        if return_list:
            return_list = [False] + return_list
    else:
        cadd = 1
        choice_list = []
    choice_list += choices

    if not choices:
        return False      #Return if there are no choices
        

    if len(choice_list) == 1:       #no need to choose if there is only one choice.
        if return_list:
            return return_list[0] if return_item else 0

    while True:
        row=0
        col=0
        current_row=[]
        for n, c in enumerate(choice_list):
            current_row.append( f'{n+cadd}. {c}' )
            row += 1
            if row >= rows or n == len(choice_list)-1:
                line('\t'.join(current_row), 0)
                row = 0
                col += 1
                current_row = []
                
            

        i = entry(prompt + " ", f="text")
        choice = None
        cindex = None

        if i in ['0', 'quit', 'cancel', 'exit']:
            if cancellable:
                return False
            else:
                continue
            

        if ft != 'number':   #String, Either
            if not flist:
                flist = [str(c).strip().lower() for c in choice_list]
            istr = i.lower().strip()
            if istr in flist:
                cindex = flist.index(istr)

        if ft != 'string' and cindex == None:  #Number, Either if not string
            if not i.isdigit():
                line(invalidprompt, 0)  
                continue
            cindex = int(i)-cadd
            if not cindex in range(len(choice_list)):
                line('Number not in range', 0)
                continue

        if return_item:
            if return_list:
                return return_list[cindex]
            else:
                return choice_list[cindex]
        else:
            return cindex

        line(invalidprompt, 0)


auto=False
instant=False
do_input = True
skip_cutscene = False

standard_speed = 25
delay = 25

def reset_curscene_settings():
    global skip_cutscene
    global auto
    skip_cutscene = False
    auto = False

def dialog(msg, talker=None, noinput=False):
    global auto
    global instant
    global do_input
    global skip_cutscene
    
    global standard_speed
    global delay
    delay = standard_speed

    do_input = True

    slowChars = ".,;:!?"

    parse = False
    parse_length = 0
    pesi = False    #Parse end space ignore
    commandEnter = False
    command=""
    value=""

    if not msg or msg[0] == "#":
        return

    msg = msg.strip().replace("{name}", g.game.player.name)

    current_msg = c.RESET

    if talker:
        current_msg += f'{talker}: '

    index = 0
    while index < len(msg):
        char = msg[index]
        index += 1
        if parse:
            parse_length += 1
            if commandEnter and char == "=":    #Seperate command from value
                commandEnter = False
                continue
            elif char == "}":
                parse = False
                if command == "delay":
                    pesi = True
                output = parse_command(command, value)
                # index -= parse_length

                if output:
                    current_msg += str(output)
                    # index += len(str(output))
                
                continue

            if commandEnter:    #if not seperating command/enter or ending parse, keep adding the char to the command/calue
                command += char
            else:
                value += char
            continue

        if char == "{":     #Check if a new command is being started, if so set it up so chars are added to command
            parse = True
            parse_length = 1
            commandEnter=True
            command=""
            value=""
            continue

        if pesi:
            if char == " ":
                continue
            else:
                pesi = False

        #Everything below: not inside a parse

        current_msg += char
        if not instant:
            sys.stdout.write("\r" + current_msg)

            wait(delay / (250 if char in slowChars else 1000))

            sys.stdout.flush()

    if instant:
        sys.stdout.write("\r" + current_msg)
        sys.stdout.flush()

    if do_input and not auto and not noinput:
        i = entry('').lower()
        if i == "auto":
            auto = not auto
            line("Auto: " + str(auto).capitalize(), 0)
        elif i == "skip":
            skip_cutscene = True
            line("Skipped", 0)

        elif i == "slow":
            instant = False
            standard_speed = 40
            line("Speed: Slow", 0)
        elif i == "medium":
            instant = False
            standard_speed = 25 
            line("Speed: Medium", 0)
        elif i == "fast":
            instant = False
            standard_speed = 15
            line("Speed: Fast", 0)
        elif i == "instant":
            instant = True
            line("Speed: Instant", 0)
    else:
        wait(0.5)
        print()
        

def parse_command(com, val):
    if com == "color" or com == "c":
        return getattr(c, val)
    elif com == "delay":
        global delay
        delay = float(val) * standard_speed
    elif com == "noinput":
        global do_input
        do_input = False


def encounter_anim():
    set_line_delay(0)
    while random.random() > 0.15:
        line("\n"*8)
        line("|----------------------|")
        line("|\\                    /|")
        line("| ==================== |")
        line("|   \\                / |")
        line("|    |------------|    |")
        line("|    |            |    |")
        line("|    |            |    |")
        line("|    |            |    |")
        line("|    |------------|    |")
        line("|   /               \\  |")
        line("| ==================== |")
        line("|/                    \\|")
        line("|----------------------|")
        line("Walking...")
        wait(.5)
        line("\n"*8)
        line("|======================|")
        line("|\\                    /|")
        line("| -------------------- |")
        line("|   \\                / |")
        line("|    |============|    |")
        line("|    |            |    |")
        line("|    |            |    |")
        line("|    |            |    |")
        line("|    |============|    |")
        line("|   /               \\  |")
        line("| -------------------- |")
        line("|/                    \\|")
        line("|======================|")
        line("Walking...")
        wait(.5)
    line("\n"*8)
    line("|----------------------|")
    line("|\\                    /|")
    line("| ==================== |")
    line("|   \\                / |")
    line("|    |------------|    |")
    line("|    |            |    |")
    line("|    |      .     |    |")
    line("|    |            |    |")
    line("|    |------------|    |")
    line("|   /               \\  |")
    line("| ==================== |")
    line("|/                    \\|")
    line("|----------------------|")
    line("You see something in the distance...")
    wait(1.5)
    line("\n"*8)
    line("|======================|")
    line("|\\                    /|")
    line("| -------------------- |")
    line("|   \\                / |")
    line("|    |============|    |")
    line("|    |            |    |")
    line("|    |      |     |    |")
    line("|    |      o     |    |")
    line("|    |============|    |")
    line("|   /               \\  |")
    line("| -------------------- |")
    line("|/                    \\|")
    line("|======================|")
    line("You see something in the distance...")
    wait(1.5)
    line("\n"*8)
    line("|----------------------|")
    line("| \\                  / |")
    line("|   \\==============/   |")
    line("|   |              |   |")
    line("|   |      ||      |   |") 
    line("|   |      ||      |   |")  
    line("|   |              |   |")
    line("|   |      ()      |   |")
    line("|   |              |   |")
    line("|   /==============\\   |")
    line("| /                  \\ |")
    line("|----------------------|")
    line("You see something in the distance...")
    wait(1)
    set_line_delay(1)
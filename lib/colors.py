class TextCodes:   #text codes
    #BASIC
    RESET = '\33[0m'
    NORMAL = '\33[37m'
    BOLD = '\33[1m'
    BOLD_OFF = '\33[21m'
    ITALIC = '\33[3m'
    ITALIC_OFF = '\33[23m'
    URL = '\33[4m'
    URL_OFF = '\33[24m'

    #OTHER
    BLINK = '\033[5m'
    RAPID_BLINK = '\33[6m'
    BLINK_OFF = '\33[25m'
    REVERSE = '\33[7m'
    REVERSE_OFF = '\33[27m'
    CONCEAL = '\33[8m'
    REVEAL = '\33[28m'
    CROSSED_OUT = '\33[9m'
    NOT_CROSSED_OUT = '\33[29m'
    FRAKTUR = '\33[20m'
    FRAMED = '\33[51m'
    ENCIRCLED = '\33[52m'
    OVERLINED = '\33[53m'
    NOT_FRAMED = '\33[54m' #and not encircled
    NOT_OVERLINED = '\33[55m'

    #COLORS
    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE  = '\33[36m'
    WHITE  = '\33[37m'

    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG  = '\33[46m'
    WHITEBG  = '\33[47m'

    GREY    = '\33[90m'
    RED2    = '\33[91m'
    GREEN2  = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2   = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2  = '\33[96m'
    WHITE2  = '\33[97m'

    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'
    GREENBG2  = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2   = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2  = '\33[106m'
    WHITEBG2  = '\33[107m'

def show_all_colors():      #use to look at all color codes
    for c in dir(TextCodes):
        if type(getattr(TextCodes, c)) == str:
            print(getattr(TextCodes, c),c,TextCodes.RESET)

# show_all_colors()

if __name__ == "__main__":
    show_all_colors()
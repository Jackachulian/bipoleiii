#Handles the main events of the game and most game-related modules are imported and interacted with here.

version = 'Alpha 5.17.2020'

import random, copy, os



from client import *
from colors import TextCodes as c

import player as p
import game as g
import enemies, moves, shop, cutscenes, areas, items, util

game = None
player = None       #references for convenience, overriden later
s = shop.norshu

def play_level(area=None, lvl=None):
    check_for_game()

    if not area:
        area = game.area
    else:
        area = getattr(areas, area)

    if not lvl:
        lvl = game.level

    event = list(area)[lvl]

    if type(event) == list:     #Battle
        return battle(event)

    elif type(event) == str:    #Everything else
        args = event.split(" ")
        cmd = args[0]
        if cmd == "cts":    #Cutscene
            skip_cutscene = False
            auto = False
            play_cutscene(args[1])
            if args[1] == 'intro':
                game.started = True
            return True

        elif cmd == "postbattle":
            return post_battle()

        elif cmd == "area":
            if args[1] == "choice":
                choice = numchoice(args[2:], prompt="Choose your path:")
                game.area = getattr(areas, args[choice+2])
            else:
                game.area = getattr(areas, args[1])
            game.level = 1
            return True


def play_cutscene(name):
    with open(f'cutscenes/{name}.txt') as f:
        cutscene = f.read().splitlines()

        auto = False    #client.auto
        skip_cutscene = False   #client.skip_cutscene
        for line in cutscene:
            cutscenes.parse_line(line)
            

def encounter(startanim):
    enemies = game.enemies

    if startanim:
        encounter_anim()

    if len(enemies) > 1:
        sep = ', '
        line(f'--- Encountered {sep.join([e.name for e in enemies[:-1]])} and {enemies[-1].name} ---')
    else:
        line(f'--- Encountered {enemies[0].name} ---')


def battle(e, startanim=True):
    check_for_game()

    game.in_battle=True
    game.enemies = [enemies.enemy_from_string(enemy) for enemy in e]

    encounter(startanim)

    game.init_enemies()
    game.turn = 0
    while True:
        game.turn += 1
        
        if game.turn == 1:
            player.draw(player.starting_cards)
            player.mulligan()
        else:
            player.draw(1)     
            [move.cooldown_tick(player) for move in player.skills]   #Count down cooldown of all moves turn 2 onward
            [[move.cooldown_tick(enemy) for move in enemy.skills] for enemy in game.enemies]

        line(f'\t--- TURN {game.turn} ---')
        game.player.display_stats()     # List stats

        game.player.make_decision()    # The player selects the move to use

        player.per_turn()
        [enemy.per_turn() for enemy in game.enemies]

        # Sorts enemies so that the ones with lower HP decide first
        game.enemies.sort(key=lambda enemy: enemy.hp)
        [enemy.make_decision() for enemy in game.enemies]   #All enemies make their decision on what move to use.
        #If the enemy chooses Defend or other priority moves they will activate here.

        if game.check(): #Check if the player is dead, if so ends. Checks if all enemies are dead and if so, breaks the loop.
            break

        game.player.act()    #The player uses their selected move

        if game.check():
            break

        # Sorts enemies so that the ones with lower HP move first
        game.enemies.sort(key=lambda enemy: enemy.hp)

        # All enemies use their move they decided on earlier
        [enemy.act() for enemy in game.enemies] 

        if game.check():
            break

        player.per_end_turn()
        [enemy.per_end_turn() for enemy in game.enemies] 

        if game.check(): #Check if the player is dead, if so ends. Checks if all enemies are dead and if so, breaks the loop.
            break

    if game.player_dead_check():
        line(f'{c.RED}- - - - GAME OVER - - - -', t=2)
        return False

    line(f'{game.player.name} won the battle!')
    game.in_battle=False
    player.reset()
    return True

def post_battle():
    check_for_game()

    #Update shop and add new items
    shop.update_shop()

    choices = {     #Coresponds to the items of post_battle_choices list in the game class at game.py
        'Stats  ': lambda: player.check(battle=False),
        'Inventory': inventory,
        'Norshu ': run_shop,
        'Xuirbo ': xuirbo,
        'Sacrifice': sacrifice,
        'Save   ': save,
        'Advance': 'advance'
    }

    lastcmd = None

    no_divider = ['stats']

    while True:
        if not lastcmd in no_divider:
            divider('Post-Battle')
        # A wacky and quirky line that gets the input and sets it to the choice in the same line
        choice = numchoice(game.post_battle_choices, 'either', rows=3, return_item=True)

        if not choice:
            continue

        run = choices[choice] #Should return a lambda if it works
        lastcmd = choice.strip().lower()

        if run == 'advance':
            # if entry('Are you sure you wish to advance?'):
            #     break
            return True
        else:
            run()

#===== Used in many choice things
def dict_choice(choices, divider_text=None, cancel_label=None, cancel_index=None, prompt="Choose one:", arg=None, arg2=None):
    while True:
        if divider_text:
            divider(divider_text)
        choice = numchoice(list(choices.keys()), 'either', prompt=prompt, return_item=True, cancel_index=cancel_index, cancel_label=cancel_label)
        if not choice or choice in ['Back', 'Cancel', 'Exit', 'Used']:
            return True
        if arg:     # i really hope there is a better way then this, but for now im doing it this way
            if arg2:
                c = choices[choice](arg, arg2)
                if not c or c == 'Used All': # (USE ITEM LAZINESS)
                    return True
            else:
                if not choices[choice](arg): #
                    return True
        else:
            if not choices[choice](): #If it returns false (aka Exit) then stop the function
                return True


# =========================== INVENTORY
def inventory():
    choices = {
        "Deck": inv_deck,
        "Collection": inv_cards,
        "Skills": inv_skills,
        "Items": inv_items,
        "Craft": inv_crafting
    }
    dict_choice(choices, 'Inventory', cancel_label='Back', cancel_index=3)    #Makes a choice and runs the function, and if it returns True then the player exited

    return True

# -------- DECK
def inv_deck():
    while True:
        divider('Deck')
        card = numchoice(player.deck, cancel_label='Back', rows=5, return_item=True)
        if not card:
            return True

        card.check()

        choices = {
            "Remove from Deck": remove_from_deck
        }

        if not dict_choice(choices, arg=card, cancel_label='Cancel'):
            return True

def remove_from_deck(card):
    if len(player.deck) > 5:
        player.inventory_cards.append(card)
        player.deck.remove(card)
        line( f'{card} sent to inventory.' )
        return False
    else:
        line( 'Your deck cannot be fewer than 5 cards.' )
    
    return True

# -------- COLLECTION
def inv_cards():
    if len(player.inventory_cards) > 0:
        while True:
            divider('Collection')
            card = numchoice(player.inventory_cards, cancel_label='Back', rows=5, return_item=True)
            if not card:
                return True

            card.check()

            divider()
            line( 'Deck: ' + ', '.join(list( map( lambda card: card.name, player.deck ) ) ), 0 )
            
            choices = {
                'Add to Deck': add_to_deck,
            }
            dict_choice(choices, arg=card, cancel_label='Cancel')
    else:
        line('You have no cards in your inventory.')
        return True
    
    return True


def add_to_deck(card):
    swap_card = None
    if len(player.deck) >= player.deck_slots:
        swap_card = numchoice(player.deck, cancel_label='Cancel', prompt='Choose a deck card to swap with', rows=5, return_item=True)

        if not swap_card:
            return True

        player.inventory_cards.append(swap_card)
        player.deck.remove(swap_card)

    player.deck.append(card)
    player.inventory_cards.remove(card)
    
    if swap_card:
        line( f'Swapped {swap_card} for {card}!' )
        return False
    else:
        line( f'Added {card} to deck!' )
        return False

    return True

# -------- SKILLS
def inv_skills():
    while True:
        skill = numchoice(player.skills, cancel_label='Back', rows=5, return_item=True)
        if not skill:
            return True
        skill.check()
    
# -------- ITEMS
def inv_items():
    if len(player.inventory_items) > 0:
        while True:
            divider('Items')
            item = numchoice(player.item_list(), cancel_label='Back', return_item=True, return_list=player.inventory_items, rows=5)
            if not item:
                return True

            item.check()
            
            choices = {}
            if item.is_usable():
                choices['Use'] = lambda item, user: item.use(user)
            dict_choice(choices, arg=item, arg2=player, cancel_label='Cancel')
    else:
        line('You have no items in your inventory.')
        return True
    
    return True
    
# -------- CRAFTING
def inv_crafting():
    if len(g.game.recipes) > 0:
        while True:
            divider('Crafting')
            i = numchoice(items.recipe_list(), cancel_label='Back', flist=items.recipe_list(productonly=True) )
            if not i:
                return True

            recipe = g.game.recipes[i-1]
            product_name = recipe[1] if type(recipe[1]) == str else recipe[1][0]
            item = items.item_from_product(product_name)

            item.check()

            choices = {
                'Craft': items.craft
            }
            dict_choice(choices, product_name, cancel_label='Cancel', arg=recipe)    #Makes a choice and runs the function, and if it returns True then the player exited
    else:
        line('You don\'t have any recipes unlocked.')
        return True


# =========================== SHOP ============================
def run_shop():     #   s - shop.norshu, or current shop later in coding if nore shops are added, will probably be renamed current_shop
    shop.greeting()

    choices = {
        "Buy": shop_buy,
        "Talk": shop.talk,
        "Leave": lambda: False
    }
    while True:
        divider('Norshu')
        choice = numchoice(list(choices.keys()), 'either', return_item=True, cancel_index=2)
        if not choice:
            break
        if not choices[choice](): #If it returns false (aka Exit) then stop the function
            break
        
    shop.parting()

def shop_buy():
    while True:
        line(f'{player}\'s Gold: {player.gold}', 0)
        line('0. Back', 0)
        shop.list_items()
        selection = shop.find_item()
        if not selection:   #If user selected 'cancel'
            return True
        else:
            selection.buy()

# ======================== SHACK ========================
def xuirbo():
    # shop.greeting()

    choices = {
        "Heal": xuirbo_heal,
        "Buy": xuirbo_buy,
        "Economy": economy,
        "Talk": lambda: True,
        "Leave": lambda: False
    }
    while True:
        divider('Xuirbo')
        choice = numchoice(list(choices.keys()), 'either', return_item=True, cancel_index=2)
        if not choice:
            break
        if not choices[choice](): #If it returns false (aka Exit) then stop the function
            break
        
    # shop.parting()

def xuirbo_heal():
    player = g.game.player
    hp_lost = player.max_hp - player.hp
    hp_percentage = player.hp / player.max_hp

    cost = math.ceil(hp_lost/2) + 2

    if hp_percentage >= 1:
        dialog('Xuirbo: You\'re not even hurt at all! Why would I use my coveted substances on you?')
        return True
    elif hp_percentage >= 0.75:
        d = f'You\'re barely even injured... but I can heal you for {cost}G. Deal?'
    elif hp_percentage >= 0.5:
        d = f'Look like you\'ve sustained some cuts. I can heal that for {cost}G. Deal?'
    elif hp_percentage >= 0.25:
        d = f'Wow, those enemies really got you good. I can heal you for {cost}G. Deal?'
    else:
        d = f'How are you still even alive? ...Anyways, I can heal you for {cost}G. Deal?'

    dialog(d, talker='Xuirbo')
    choice = numchoice(['Accept'], cancel_label='Decline')

    if choice:
        if not player.remove_gold(cost):
            return True #Will return if the user doesnt have enough gold and also not subtract the gold

        lines = ['Xuirleaf remedy, coming right up...', 'Alright, time to drug you...', 'Okay, don\'t move.', '', 'Time to do something very legal.']
        dialog( random.choice(lines), talker='Xuirbo' )

        player.heal(hp_lost)

        lines = ['Should be good as new.', 'Now go out and squash some slimes.', 'If you have any adverse side effects, you didn\'t get this from me.', 'Probably shouldv\'e checked the side effects of that one beforehand..', 'Congrats, you\'re now addicted and have a depencence of xuirleaf!']
        dialog( random.choice(lines), talker='Xuirbo' )
        return True
    else:
        if hp_percentage > 0.5:
            line('Fine, keep your gold.')
        else:
            line('Okay, guess you\'ll just die then.')
        return True


def xuirbo_buy():
    while True:
        line(f'{player}\'s Gold: {player.gold}', 0)
        line('0. Back', 0)
        shop.list_items( shop=shop.xuirbo )
        selection = shop.find_item( shop=shop.xuirbo )

        if not selection:   #If user selected 'cancel'
            return True
        else:
            selection.buy()

def economy():
    line('Economy is not implemented yet', 0)



def sacrifice():
    line('Sacrifice is not implemented yet', 0)

def save():
    g.save_file()


game_loop = False
choice_loop = True

def mainloop():
    global game_loop
    game_loop = True

    choices = {
        "New Game": lambda: start_new_game(),
        "Load File": lambda: load_game(),
        "Options": lambda: options(),
        "Stats": lambda: stats(),
        "Exit": lambda: quit_game()
    }
    
    while game_loop:
        title_screen()
        global choice_loop
        choice_loop = True

        while choice_loop:
            choice = numchoice(list(choices.keys()), return_item=True)

            if choice:
                choices[choice]()
            else:
                quit_game()
            
        #If the code gets here then the player died and was sent back to the menu
    #If the code reaches here the player has exited the mainloop
    line('See ya!', 0)
    

def gameloop():
    while play_level():    #This will keep going on, and if returns false, then escape
        if not game_loop:
            return      #Exit if game loop is off
        game.level += 1


def title_screen():
    set_line_delay(0)
    line()
    line()
    line(f'   {c.GREY}{" "*(36-len(version))}Ver. {version} ')
    line('    {c.GREY}=========================================')
    line('    ************** {c.RED}{c.BOLD}{c.URL}BIPOLE III{c.URL_OFF}{c.BOLD_OFF}{c.RESET} ***************')
    line('    ** {c.BLUE}{c.ITALIC}Conspiracy of the Mechanical Entity{c.ITALIC_OFF}{c.NORMAL} **')
    line('    {c.GREY}=========================================')
    line()
    set_line_delay(1)

def start_new_game(onlysetup=False):
    global choice_loop
    choice_loop = False

    g.new_game()
    global game
    game = g.game
    game.player = p.Player()
    global player
    player = game.player

    game.version = version

    game.area = areas.port
    game.level = 0

    if onlysetup:
        return

    if not g.game.player.changename():  #Exit if the game cancels the name creation
        return
    gameloop()

def check_for_game():   #Used for testing mainly. Start a new game if a game isn't loaded and a battle/event is trying to run.
    if not game:
        start_new_game(onlysetup=True)

def load_game():
    while True:
        file = g.load_file(check_empty=True)   #Returns false if a file is not loaded
        if file == False:
            break

        global choice_loop
        choice_loop = False
        
        global game
        game = g.game
        global player
        player = g.game.player

        gameloop()

        return True


def options():
    line('Not implemented yet')

def stats():
    line('Not implemented yet')

def quit_game():
    global game_loop
    game_loop = False
    global choice_loop
    choice_loop = False

# ====
# Runs the game
# ====
if __name__ == "__main__":
    mainloop()
# This file is where the game class is kept (to prevent circular imports from importing the main file). 
# Most files import this file to use the game variable that is shared among them.

#Load game from save if one exists.
#There is one save file only. Game can only be saved during post-battle.
# If the game is closed mid-game and when the player loses, the file is deleted and game stats are saved to a game history file.
# Games can only be saved and exited from the post-battle which will save the file and can be continued later.

import sys
if __name__ == "__main__":
    sys.exit("Make sure you are running the BipoleIII.py file!")

import os, random

try:
    import dill as pickle     #yes these are actual module names
except:
    import pickle

import datetime

import util, client
from colors import TextCodes as c

game = None

saves_updated = False
saves = []

class Game:
    def __init__(self):
        self.version = None

        self.file_id = random.random()
        self.file = None
        self.started = False    #Turns to true after the first level, no need to save midway through first cutscene

        self.player = None

        #Battle
        self.in_battle = False
        self.enemies = []
        self.turn = 0

        #SETTINGS
        self.line_speed = 1     #Changes the speed that lines are displayed

        #Gamemodes
        #normal - basic gamemode    hard - no heal in-between   randomized - everything is randomized
        self.gamemode = 'normal'

        #When enabled, to select moves, you first type "S" or "A" for skill/action insstead of hand, and then the index in the list (the numbers are listed when displayed)
        #NOT IMPLEMENTED YET, Will be used for possible calculator implementation
        self.move_numeric_select = False

        #Whether or not to show all shop items. For debugging and for Justin video showcase, will probably have this off in the final game
        self.shop_show_all = False

        #Area data
        self.area = None
        self.level = None

        self.post_battle_choices = [
            'Stats  ',
            'Inventory',
            'Norshu ',
            'Xuirbo ',
            'Sacrifice',
            'Save   ',
            'Advance'
        ]

        self.recipes = []

    def init_enemies(self):
        #Initializes enemies, mostly based on other enemies because everything else is defined in the class
        self.rename_enemies()
    

    def rename_enemies(self):
        # - Gives them a troop order which is used in list displaying to keep the order consistent
        # - Renames enemies so that there are not duplicate nmes, etc. Slime, Slime -> Slime A, Slime B
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        n =  0
        for enemy in self.enemies:
            enemy.troop_order = n
            n += 1
            same_name_list = list(filter(lambda e: e.name == enemy.name, self.enemies))
            if len(same_name_list) > 1:
                for i, e in enumerate(same_name_list):
                    e.name = e.name + " " + letters[i]



    def check(self):
        if not self.in_battle:
            return False

        if self.battle_cleared_check():
            return True

        if self.player_dead_check():
            return True

        return False

        
    def alive_enemies(self):
        #return all alive enemies
        return list( filter(lambda e: not e.dead, game.enemies) )

    def battle_cleared_check(self):
        #Checks that all enemies have been defeated, and if so returns true
        for enemy in self.enemies:
            if not enemy.dead:
                return False
        return True

    def player_dead_check(self):
        #Returns true if the player has died
        return self.player.dead

    
    def display_file(self, i=0):
        client.divider()
        client.line(f'{i+1}. {self.player.name}     {self.area}     Level {self.player.level}     HP: {self.player.hp}/{self.player.max_hp}',0)
        client.line(self.savetime.strftime("  %m/%d/%Y %H:%M:%S"),0)

    def savable(self):
        #Whether or not the game is savable in its current state
        return (not self.in_battle) and self.started



def new_game():
    global game
    game = Game()

def save_file(file=None, auto=False):
    global game

    if auto:
        file = game.file

    if not file:
        while True:
            ind = choose_file(return_index=True, load=False)

            if type(ind) == bool and ind == False:
                return False

            game_file = saves[ind]

            if game_file:
                if game_file.file_id != game.file_id:
                    if client.entry('This will overwrite this game, are you sure?', f='yes_or_no'):
                        file = game_file.file
                        break
                else:
                    file = game_file.file
                    break

            else:
                #If file slot is empty, find next available name
                file = game.player.name+'.bipole3'

                n = 2
                while file_exists(file):
                    file = game.player.name+str(n)+'.bipole3'
                    n += 1
                break

    game.savetime = datetime.datetime.now()
    game.file = file

    pickle.dump(game, open( 'saves/'+file, 'wb'))

    global saves_updated
    saves_updated = False

    client.line('{c.BEIGE}Game saved!',0)

def quick_save(keyinterrupt=True):
    #There was originally a save here but i removed it because it was janky, so its really just an exit check
    if game:
        try:
            if keyinterrupt: 
                if client.entry('Are you sure you want to quit?', 'yes_or_no', keyinterrupt=False):
                    sys.exit('Exiting Bipole III')
                else:
                    return
            else:
                sys.exit('Exiting Bipole III')
        except KeyboardInterrupt:
            sys.exit('Exiting Bipole III')
    else:
        sys.exit('Exiting Bipole III')


def load_game(save, vers=None):
    global game
    game = save
    return True

def read_file(file):
    # try:
    #     file_load = pickle.load( open( 'saves/'+file, 'rb'))
    # except:
    #     print(f'\33[31mWarning: {file} is corrupt\33[0m')
    #     return None

    file_load = pickle.load( open( 'saves/'+file, 'rb'))

    return file_load


def file_exists(file):
    #Return true if a save file exists
    return os.path.exists('saves/'+file)

def load_all_files():
    #This is a taxing line if code so it should be used as least as possible
    global saves_updated
    if saves_updated:   #Will not run if the files are up to date, this is set to false every time a file is updated
        return False

    files = os.listdir('saves')

    file_list = []

    for file in files:
        filepath = 'saves/'+file
        if os.path.isfile(filepath):
            game_file = read_file(file)

            file_list.append(game_file)

    global saves
    saves = file_list

    saves_updated = True

def list_files():
    load_all_files()

    global saves
    while len(saves) < 5:
        saves.append(None)

    i = 0
    for file in saves:
        if file:
            file.display_file(i)
            i += 1
        else:
            client.divider()
            client.line(f'{i+1}. Empty',0)
            i += 1
    
    client.divider()

def load_file(check_empty=False):

    show_files()
    while True:
        chosen_file = choose_file(show_file_list=False, load=True)

        if chosen_file == False:
            return False
        if chosen_file == None and check_empty:
            client.line('{c.YELLOW}File is empty',0)
            continue

        break

    global game
    game = chosen_file
    return True

def show_files():
    client.line(' ',0)
    client.line('0: Cancel',0)
    list_files()

def choose_file(prompt='Choose a file:', load=True, return_index=False, show_file_list=True):
    if load and len(saves) == 0:
        client.line("{c.YELLOW}No save file to load.", 0)
        return False

    if show_file_list:
        show_files()

    while True:
        choice = client.entry(prompt, f='text').strip().lower()

        if choice in ['0', 'back', 'cancel', 'quit', 'exit']:
            return False

        if not choice.isdigit():
            client.line('Enter a number',0)
            continue

        choice = int(choice)

        if choice < 1 or choice > len(saves):
            client.line('Not within range',0)
            continue

        chosen_file = saves[choice-1]

        

        if return_index:
            return choice-1
        else:
            return chosen_file




load_all_files()



# def new_game():
#     global game
#     game = Game()

# def save_file():
#     global game
#     pickle.dump(game, open( 'saves/save.bipole3', 'wb'))

# def load_file(file, vers=None):
#     global game


    
#     try:
#         file_load = pickle.load( open( f'saves/{file}.bipole3', 'rb'))
#     except:
#         print('\33[31mCorrupt file!\33[0m')
#         return False
    
#     #Check version to see if at or above current version (saves are backwards compatible)
#     if vers and file_load.version != vers:
#         client.line('{c.RED}This save file is from an incompatible version!',0)
#         return False

#     game = file_load
#     return True

# def file_exists():
#     #Return true if a save file exists
#     return os.path.exists('saves/save.bipole3')
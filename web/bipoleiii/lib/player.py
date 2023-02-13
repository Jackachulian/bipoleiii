import sys

import random, math, copy

import game as g
from colors import TextCodes as c

import moves, util, afflictions, items
import client

class Player:
    player = True

    def __init__(self):
        self.name = "Lead"
        self.gold = 0           #currency

        # --- Initial battle stats
        self.max_hp = 20.0
        self.hp = 20.0

        self.starting_sp = 5
        self.max_sp = 5
        self.sp = 5

        self.starting_le = 0
        self.le = 0

        self.decision = None
        self.target = None

        # --- In-battle hand/stats
        self.hand = []          # List of held cards
        self.hand_slots = 5      #Total amt. of cards that can be held
        self.starting_cards = 3     #Amt. of cards drawn at the start of battle

        self.discard = []       # discard pile

        # --- Inventory
        self.inventory_cards = []
        self.inventory_items = []

        # All cards that can be drawn
        self.deck = ["Slice", "Fireball", "Shock", "Dual Magic", "Salvage", "Recover", "Pickpocket", "ULT Magic", "ULT Sword", "ULT Recovery"]
        self.deck_slots = 10              
        
        # Cards that can be used att any time and aren't consumed on use
        self.skills = ["Punch", "Defend", "Life Transfer", "Discard 1", "Discard 2", "Testing"]           

        # Moves that don't use your turn
        self.actions = ["Stats", "Main", "Check", "Info"]

        self.strings_to_moves()

        # --- Levelup tree
        self.level = 0
        self.xp = 0
        self.level_health = 0
        self.level_power = 0
        self.level_mana = 0
        self.level_stealth = 0
        self.level_utility = 0

        # --- Other stats
        self.afflictions = []
        #List of afflictions (status effects) effects that the player/enemy has

        self.crit_chance = 0.1  
        self.crit_mul = 1.5
        self.dodge_chance = 0.1
        
        self.heal_mul = 1.0     #Incoming healing mult
        self.resistance = 1.0   #Damage taken from status effects mult
        self.pharmacy = 1.0     #Item healing mult
        self.greed = 1.0        #Gold dropped by enemies mult (Multiplies upper value by (1-greed)*2)
        self.resourcefulness = 1.0  #Materials dropped by enemies mult

        self.ironskin = False       #Health lv.9, +2 defendse when defending. +3 total, 4 defense when defending (0.25x damage taken)
        self.blacksmith = False    #Power lv9, regain materials when crafting tools
        self.concussive = False     #Power lv9, crits can sometimes stun
        self.clairvoyant = False    #Magic lv.9, see the next card drawn at all times
        self.alchemist = False      #Magic lv.9, regain materials when crafting potions
        self.combo_breaker = False  #Stealth lv9, chance when critting to gain a move
        self.dripstep = False       #Stealth Lv.9, allows you to dodge and counter while defending
        self.trash_artist = False   #Utility lv9, discard moves do not use up your turn
        self.craftsmanship = False  #Utility lv.9, regain materials when crafting consumables (sigils/booster/other non-potion consumables)
        
        self.atk = 1.0    #all damage is multiplied by this
        self.defense = 1.0  #all incoming damage is divided by this
        self.defending = False
        self.defending_amt = 0  #used by defend moves
        
        self.atk_buffed = 0
        self.defense_buffed = 0

        self.immobile_turns = 0     #Some moves cause you to not be able to act for a certain amount of turns
        self.flying = False       #Only specific moves will target oyu, otherwise dodge all. used on Bounce move
        self.no_turn_draw_turns = 0     #Turns that the player will not draw a card at the start of their turn
        self.in_extra_turn = False     #Whether or not the player is in an extra turn or not

        self.counter = False       #boolean of whether or not the player can counter
        self.counter_chance = 0.0
        self.counter_mul = 1.5      #damage mul when counterattacking

        self.heal_amount = 2        #HP received when healing self
        self.brew_sp     = 1        #SP gained from brews

        self.hit_passive = lambda self, attacker: None     #these are used only by enemies, put here for compatability
        self.post_hit_passive = lambda self, attacker: None
        self.turn_start_passive = lambda self: None
        self.turn_end_passive = lambda self: None
        self.defeat_passive = lambda self: None

        self.next_turn_effect = None    #Set by some moves
        self.this_turn_effect = None    #End ov every turn, next_turn_effect is moves to this_turn_effect and next_turn_effect is cleared. this_turn_effect runs on turn, 
        #usually the user is immobile from a bounce or bounce/like move and will now be able to be targeted

        self.root = 0   #Tsoref ability, 0.25 DMG per turn for each root

        self.reset() #defines HP, SP and LE and sets them to default

        # --- Economy 
        self.interest = 0.20
        self.interest_interest = 0.10
        self.invested = 0

    def __str__(self):
        return self.name

    # ==== INFO
    def check(self, battle=True):
        hp = client.bold("HP:") + f' {self.hp}/{self.max_hp}\t'
        if g.game.gamemode == 'hard':
            battle=True
        
        client.set_line_delay(0)
        client.divider()
        client.line(f' -  {c.VIOLET}{self.name}{c.RESET}  - ')
        client.line(f'  Level {self.level} \t({self.current_level_xp()}/{self.levelup_xp_required()})')
        client.line(f'  {hp}{client.bold("ATK:")} {self.atk}\t{client.bold("DEF:")} {self.defense}')
        if battle:
            client.line(f'  {client.bold("SP:")} {self.sp}/{self.max_sp}\t{client.bold("LE:")} {self.le}')
        client.line(f'  {client.bold("Crit Chance:")} {util.percent(self.crit_chance)}\t{client.bold("Crit DMG:")} +{util.percent(self.crit_mul-1.0)}\t{client.bold("Dodge Chance:")} {util.percent(self.dodge_chance)}')
        if self.counter:
            client.line(f'  {client.bold("Counter Chance:")} {util.percent(self.counter_chance)}\t{client.bold("Counter DMG:")} +{util.percent(self.counter_mul-1.0)}\t{c.BOLD}')
        client.line(f'\n  {client.bold("Deck:")} {self.display_moves("deck", return_string=True, format_string=False)}')
        client.line(f'  {client.bold("Actions:")} {self.display_moves("actions", return_string=True)}')
        client.line(f'  {client.bold("Skills:")} {self.display_moves("skills", return_string=True)}')
        if battle:
            client.line(f'  {client.bold("Hand:")} {self.display_moves("hand", return_string=True)}')

        client.divider()
        client.set_line_delay(1)

    def display_stats(self):
        client.set_line_delay(0)

        player = self
        enemies = g.game.enemies

        client.line('', 0)
        client.divider('')

        enemies.sort(key=lambda e: e.troop_order)
        for enemy in enemies:
            status_list = ''.join( [ f" {aff.color}({aff}){c.RESET}" for aff in enemy.afflictions ] ) + ('{c.GREY}' if enemy.dead else '{c.RESET}')
            status_list += ' {c.ITALIC}(Flying){c.RESET}' if enemy.flying else ''
            client.line(f'  {c.GREY if enemy.dead else ""}{enemy.name}{status_list}\tHP: {enemy.hp}/{enemy.max_hp}\tATK: {enemy.atk}')
            client.divider()

        status_list = ''.join( [ f" {aff.color}({aff}){c.RESET}" for aff in self.afflictions ] )
        status_list += ' {c.ITALIC}(Flying){c.RESET}' if self.flying else ''
        client.line(f'  {player.name}{status_list}\tHP: {player.hp}/{player.max_hp}\tSP: {player.sp}/{player.max_sp}\tLE: {player.le}')

        if self.clairvoyant:
            client.line(' {c.BEIGE}*{c.BLUE}*{c.VIOLET}*{c.VIOLET2} Next Card: '+str(self.next_card)+' {c.VIOLET}*{c.BLUE}*{c.BEIGE}*{c.RESET} ')

        player.display_moves("hand")
        client.divider()
        client.set_line_delay(1)

    def move_info(self):
        move = self.select_move("Choose a move to get info on:", use_actions=False, info=True)
        move.check()

    # ==== MOVES
    def strings_to_moves(self):
        self.deck = [moves.move_from_string(card) for card in self.deck]
        self.skills = [moves.move_from_string(skill) for skill in self.skills]
        self.actions = [moves.move_from_string(action) for action in self.actions]

    
    def mulligan(self): #Choose cards to remove from hand and draw another card, runs at start
        mulligan_list = []
        while True:
            hand_display = list( map(lambda card: '{c.REDBG}' + str(card) + '{c.RESET}' if card.mulliganed else card, self.hand) )
            selection = client.numchoice(hand_display, prompt="Choose cards to add to your mulligan:", cancel_label='Done', cancel_index=0, rows=3 if self.hand_slots > 3 else 4)

            if not selection:
                break

            selection = self.hand[ selection - 1 ]

            selection.mulliganed = not selection.mulliganed     #Toggles mulliganed

            mulligan_list = list( filter(lambda card: card.mulliganed, self.hand) )
            
            if len(self.hand) == len(mulligan_list):    #Exit if all are mulliganed
                break

        for mcard in mulligan_list:
            self.discard_card(mcard)
            
        for mcard in mulligan_list:
            self.draw(1)


    def obtain(self, item, amt=1, announce=True):
        #Input a string, convert to move, and append to appropriate list.

        if type(item) == str:
            found_item = items.item_from_string(item)
            if found_item:
                item = found_item
            else:
                found_item = moves.move_from_string(item)
            
                if found_item:
                    item = found_item
                else:
                    return

            if not found_item:
                return

        if item.item_type == 'move':
            if item.move_type == "action":
                if announce:
                    client.line(f'{self} can now use {item.name}!')
                self.actions.append(item)
            elif item.move_type == "skill":
                if announce:
                    client.line(f'{self} learned {item.name}!')
                self.skills.append(item)
            elif item.move_type == "card":
                if announce:
                    client.line(f'Obtained {item.name}!')
                if len(self.deck) >= self.deck_slots:
                    if announce:
                        client.line(f'{self}\'s deck is full. {item} sent to inventory.')
                    self.inventory_cards.append(item)
                else:
                    self.deck.append(item)

        elif item.item_type == 'item':
            existing_item = util.fsearch(self.inventory_items, lambda x: x.name == item.name)
            if existing_item:
                existing_item.quantity += amt
            else:
                item.quantity = amt
                self.inventory_items.append(item)
            
            if announce:
                client.line(f'Obtained {amt} {item}!')

    def item_list(self):
        return [ f'{i} ({i.quantity})' for i in self.inventory_items ]

    # BATTLE
    def reset(self):
        self.dead = False
        self.hand = []
        self.discard = []
        self.next_card = copy.copy(random.choice( self.deck ))

        self.sp = self.starting_sp
        self.le = self.starting_le

        #Remove buffs
        if self.atk_buffed:
            self.atk -= self.atk_buffed
            self.atk_buffed = 0
        if self.defense_buffed:
            self.defense -= self.defense_buffed
            self.defense_buffed = 0

        #Clear afflictions
        for aff in self.afflictions:
            aff.remove(self, announce=False)
        
    


    def add_gold(self, amt):
        self.gold += amt
        client.line(f'{self} gained {amt} gold!    Balance: {self.gold}G')

    def remove_gold(self, amt):
        if self.gold >= amt:
            self.gold -= amt
            return True
        else:
            client.line(f'Not enough gold!')
            return False


    # ---- BATTLE ----

    #Per turn
    def per_turn(self):
        #Things to run at the start of each turn, after player decides
        #Run self turn start passive
        self.turn_start_passive(self)

        #start tick afflictions
        self.aff_tick()

    def per_end_turn(self):
        #Run at the end of every turn
        #Run self turn end passive
        self.turn_end_passive(self)

        #Remove defense
        self.defense -= self.defending_amt
        self.defending = False
        self.defending_amt = 0

        #Take root damage (Tsoref's ability)
        if self.root > 0:
            self.take_damage(None, 0.25 * self.root, counterable=False)

        #end tick afflictions
        self.aff_end_tick()

        #Tick down immobile turns
        if self.immobile_turns > 0:
            self.immobile_turns -= 1

        #Next turn effect = this turn effect, and clear this_turn_effect from this turn
        if self.this_turn_effect:
            self.this_turn_effect = None

        if self.next_turn_effect:
            self.this_turn_effect = self.next_turn_effect
            self.next_turn_effect = None

        #Player only
        #No turn draw decrement
        if self.player:
            if self.no_turn_draw_turns > 0:
                self.no_turn_draw_turns -= 1


    #Afflictions

    def afflict(self, aff, chance=1, dur=3, dodge_announce=False):
        aff = aff.lower().strip()

        if type(dur) == tuple:  #If the dur is somethinglike (3,5), pick a random duration between
            dur = random.randint(dur[0], dur[1])

        if random.random() < chance:
            if aff in [a.name for a in self.afflictions]:  #If already affected, renew the duration but keep the same affliction
                existing_aff = list( filter(lambda a: a.name.lower().strip() == aff, self.afflictions) )[0]
                if dur >= existing_aff.duration:
                    existing_aff.duration = dur
                    client.line( existing_aff.afflict_text.format(name=user, aff=existing_aff) )
                    existing_aff.afflict_effect(existing_aff, user)
            else:
                affliction = copy.deepcopy(afflictions.aff_from_string(aff))
                self.afflictions.append(affliction)
                affliction.on_afflict(self, dur)
        else:
            if dodge_announce:
                client.line(f'{self} dodged the {aff}!')
            return False
        
        return True
        


    def clear_afflict(self, aff):
        if aff == 'all':
            for a in self.afflictions:
                a.remove(self, clear=True)

        elif type(aff) == str:
            for a in self.afflictions:
                if a.name == aff:
                    a.remove(self, clear=True)

        else:   #iterable
            for a in self.afflictions:
                for af in aff:
                    if a.name == af:
                        a.remove(self, clear=True)
        
        
    def aff_tick(self):  
        #The way this is set up, status effects will only run once even if the user is affected by the same status multiple times            

        for aff in self.afflictions:
            aff.tick(self)

    def aff_end_tick(self):             
        for aff in self.afflictions:
            aff.end_tick(self)

    def has_aff(self, name):
        return name.lower() in [aff.name.lower() for aff in self.afflictions]


                



    #Damage

    def target_and_deal_damage(self, damage, crit_chance=None, crit_type='mult', target_type='one', tags=None):
        target = self.select_target(target_type)
        if not target:
            return False

        self.deal_damage(target, damage, crit_chance, crit_type, tags)


    def deal_damage(self, target, damage, crit_chance=None, crit_type='mult', tags=None):
        #Deal damage with the player, accounting for damage / crit / dodge buffs

        if crit_chance:
            if crit_type == 'add':
                crit_chance = self.crit_chance + crit_chance
            else:   #mult
                crit_chance = self.crit_chance * crit_chance
        else:
            crit_chance = self.crit_chance

        if random.random() < crit_chance:
            crit = True
            client.line(client.bold("CRITICAL HIT!"))
        else:
            crit = False
            
        damage_dealt = target.take_damage(self, damage, crit)

        for aff in self.afflictions:
            aff.deal_damage_effect(aff, self, target, damage)

        if crit and self.player:
            if self.concussive:
                target.afflict('stun', 0.25, 1)
            if self.combo_breaker and not self.in_extra_turn and util.rng( (1-self.crit_chance)/2 ):
                self.extra_turn()

        return damage_dealt


    def take_damage(self, attacker, damage, crit=False, counterable=False):

        if self.hit_passive(self, attacker):  #If hit passive returns true the damage was negated
            return

        atk = attacker.atk if attacker else 1

        #Damage formula

        damage = round(damage * atk * (self.crit_mul if crit else 1) / (1 if crit else self.defense), 2)    

        self.hp = round (self.hp - damage, 2)
        client.line(f'{self.name} took {damage} damage')
        if self.hp <= 0:
            self.hp = 0
            self.defeat()
            return

        if self.post_hit_passive(self, attacker):  #If hit passive returns true then will not counter
            return

        for aff in self.afflictions:
            aff.on_damage(self, attacker, damage)

        if counterable and attacker and self.counter and random.random() < self.counter_chance:
            client.line(url("COUNTER ATTACK!"))
            self.deal_damage(attacker, damage * self.counter_mul)

        return damage

    def defend(self, amt):
        #Add defense until the end of the turn

        if self.player:
            if self.ironskin:
                amt += 2

        self.defense += amt
        self.defending = True
        self.defending_amt += amt

    def defeat(self):
        self.dead = True
        client.line(f"{self.name} was defeated...", t=1.5)


    #Point gain/lose

    def heal(self, amt, announce=True):
        if g.game.check():  #No need to heal if the game is over
            return

        amt *= self.heal_mul

        old = self.hp
        self.hp += amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp <= 0:
            return self.defeat()

        if announce:
            if amt >= 0:
                client.line(f'{self.name} healed {amt} HP! ({old} -> {self.hp})')
            else:
                client.line(f'{self.name} lost {amt*-1} HP! ({old} -> {self.hp})')


    def gain_sp(self, amt):
        old = self.sp
        self.sp += amt
        if self.sp > self.max_sp:
            self.sp = self.max_sp
        if self.sp < 0:
            self.sp = 0
        if amt >= 0:
            client.line(f'{self.name} gained {amt} SP! ({old} -> {self.sp})')
        else:
            client.line(f'{self.name} lost {amt*-1} SP! ({old} -> {self.sp})')
    

    def gain_le(self, amt):
        old = self.le
        self.le += amt
        if self.le < 0:
            self.le = 0
        if amt >= 0:
            client.line(f'{self.name} transferred {amt} LE! ({old} -> {self.le})')
        else:
            client.line(f'{self.name} lost {amt*-1} LE! ({old} -> {self.le})')

    
    #Stat related

    xa = 5 #xp start
    xd = 1 #xp difference

    def levelup_xp_required(self):
        #Return the current amount of XP of the current level required to level up
        return self.xa + self.xd*(self.level-1)

    def current_levels_xp(self):
        #Return the total XP that constitutes all levels
        n = self.level-1
        return round((n/2) * (2*self.xa + (n-1)*self.xd)) #Arithmetic sum formula

    def current_level_xp(self):
        #Return the current XP invested into the current level
        return self.xp - self.current_levels_xp()

    def next_levelup(self):
        #Return the XP needed to reach the next level
        #XP to next level: 5, 6, 7, 8, 9, 10, etc
        n = self.level
        return (n/2) * (2*self.xa + (n-1)*self.xd)

    def xp_bar(self):
        #Display the player's XP bar
        length = 50

        bar_fill = math.floor((self.current_level_xp() / self.levelup_xp_required()) * length) 

        client.line(f'Level {self.level} ' + c.REVERSE + '_'*bar_fill + c.RESET + c.URL + ' '*(length-bar_fill) + c.RESET + f' {self.current_level_xp()}/{self.levelup_xp_required()}')

    def gain_xp(self, xp):
        if self.hp >= 1475:
            return

        self.xp += xp
        client.line(f'{self.name} gained {xp} XP', t=1)

        old_level = self.level
        levelup_count = 0
        while self.xp >= self.next_levelup():
            self.level += 1
            levelup_count += 1

        if self.level > 50:
            self.level = 50
            self.xp = 1475
        
        if not old_level == self.level:
            client.line(f'{c.VIOLET2}Level Up!{c.RESET} {old_level} -> {self.level}', t=1.5)

        levels_added = 0
        for _ in range(levelup_count):
            levels_added += 1
            if old_level + levels_added >= 50:
                break
            self.class_raise()

        self.xp_bar()

    def class_raise(self):

        classes = list( stats.keys() )  # health, power, mana, stealth, utility

        classes_display = list( map(lambda c: f'({getattr(self, "level_"+c)}) ' + c.capitalize(), classes) )

        
        while True:
            c = client.numchoice(classes_display, flist=classes)

            level = getattr(self, "level_"+classes[c])

            if level >= 10:
                client.line(f'{classes[c].capitalize()} cannot be leveled any further!', 0)
                continue
            
            break

        self.levelup_class(classes[c])


    levelup_paths = {
        'health': (
            ( 'Hearty', '+4 Max HP', lambda u: u.stat_change('max_hp', 4), (
                ('Healthy', '+8 Max HP', lambda u: u.stat_change('max_hp', 8) ),
                ('Pharmacist', 'Items heal +50% HP', lambda u: u.stat_change('pharmacy', 0.5) ) ) ),

            ( 'Resistant', '-25% affliction damage', lambda u: u.stat_change('resistance', 0.25), (
                ('Immunity', '-25% affliction damage', lambda u: u.stat_change('resistance', 0.25) ),
                ('Ironskin', '+2 DEF when defending', lambda u: u.stat_change('ironskin', True, message='{user}\'s defend becomes stronger!') ) ) ) ), 

        'power': (
            ( 'Powerful', '+0.5 ATK', lambda u: u.stat_change('atk', 0.5), (
                ('Dangerous', '+0.5 ATK', lambda u: u.stat_change('atk', 0.5) ),
                ('Blacksmith', 'Reduced materials required to craft tools and weapons', lambda u: u.stat_change('blacksmith', True, message='{user} mastered the art of smithing!') ) ) ),

            ( 'Forceful', '+25% Crit DMG', lambda u: u.stat_change('crit_mul', 0.25), (
                ('Fatal', '+25% Crit DMG', lambda u: u.stat_change('crit_mul', 0.25) ),
                ('Concussive', 'All Critical Hits have a 25% chance to stun for 1 turn', lambda u: u.stat_change('concussive', True, message='{user}\'s Critical Hits can now stun enemies!') ) ) ) ),

        'mana': (
            ( 'Spellcaster', '+2 starting SP', lambda u: u.stat_change('max_sp', 2), (
                ('Perparation', '+2 starting SP', lambda u: u.stat_change('max_sp', 2) ),
                ('Clairvoyant', 'Allways see the top card of your deck', lambda u: u.stat_change('clairvoyant', True, message='{user} gained the power of clairvoyance!') ) ) ),

            ( 'Materialistic', '+1 card drawn on first turn', lambda u: u.stat_change('starting_cards', 1), (
                ('Initiator', '+1 card drawn on first turn', lambda u: u.stat_change('starting_cards', 1) ),
                ('Alchemist', '30% chance to recover ingredients when crafting potions', lambda u: u.stat_change('alchemist', True, message='{user} mastered the art of alchemy!') ) ) ) ),

        'stealth': (
            ( 'Backstab', '+5% crit chance', lambda u: u.stat_change('crit_chance', 0.05), (
                ('Headshot', '+10% crit chance', lambda u: u.stat_change('crit_chance', 0.1) ),
                ('Combo Breaker', 'When scoring a Crit, chance equal to half the chance of not critting to gain an extra move', lambda u: u.stat_change('combo_breaker', True, message='{user} learned how to combo break!') ) ) ),

            ( 'Shady', '+5% dodge chance', lambda u: u.stat_change('dodge_chance', 0.05), (
                ('Dankness', '+10% dodge chance', lambda u: u.stat_change('dodge_chance', 0.1) ),
                ('Dripstep', 'Allows you to dodge and counter while defending', lambda u: u.stat_change('dripstep', True, message='{user} discovered the power of the Dripstep!') ) ) ) ),

        'utility': (
            ( 'Greedy', '+25% gold dropped by enemies', lambda u: u.stat_change('greed', 0.25), (
                ('Monopolizer', '+25% gold dropped by enemies', lambda u: u.stat_change('greed', 0.25) ),
                ('Trash Artist', 'All Discard moves do not use up the turn', lambda u: u.stat_change('trash_artist', True, message='{user} mastered the art of... trash?!') ) ) ),

            ( 'Resourceful', '+25% materials found', lambda u: u.stat_change('resourcefulness', 0.25), (
                ('Survivalist', '+50% materials found', lambda u: u.stat_change('resourcefulness', 0.5) ),
                ('Craftsmanship', '30% chance to recover materials when crafting consumables', lambda u: u.stat_change('craftsmanship', True, message='{user} mastered the art of craftsmanship!') ) ) ) ),
    }


    def levelup_class(self, c):
        old_level = getattr(self, 'level_'+c)
        setattr(self, 'level_'+c, old_level+1)
        level = getattr(self, 'level_'+c)

        level_function = getattr(self, 'levelup_'+c)

        level_string = stats[c] + c.capitalize() + '{c.RESET}'

        client.line(f'{level_string} Level UP! {old_level} -> {level}', t=1)
        level_function(level)

        class_branch = self.levelup_paths[c]
        if level == 3:
            primary_branches = [f'{b[0]}: {b[1]}' for b in class_branch] #Combine name+desc and put into list

            client.divider()
            client.line(client.italic(' ---- Choose a trait ---- '),0)
            primary_branch_index = client.numchoice( primary_branches, cancellable=False )
            primary_branch = class_branch[ primary_branch_index ]

            primary_branch[2](self) #Runs the lambda

            setattr(self, 'branch_'+c, primary_branch_index )

        elif level == 6:
            primary_branch_index = getattr(self, 'branch_'+c)
            primary_branch = class_branch[ primary_branch_index ][3]

            secondary_branches = [f'{b[0]}: {b[1]}' for b in primary_branch] #Combine name+desc and put into list

            client.divider()
            client.line(client.italic(' ---- Choose a trait ---- '),0)
            secondary_branch_index = client.numchoice( secondary_branches, cancellable=False )
            secondary_branch = primary_branch[ secondary_branch_index ]

            secondary_branch[2](self) #Runs the lambda


    def levelup_health(self, level):
        self.stat_change('max_hp', 4)
        self.heal(4, announce=False)
        if level == 3:
            self.obtain("Lesser Heal")
        elif level == 6:
            self.obtain("Heal")
        elif level == 9:
            self.obtain("Greater Heal")
            

    def levelup_power(self, level):
        if level == 3:
            self.stat_change('atk', 0.5)
            self.obtain('Strong Punch')
        elif level == 6:
            self.stat_change('atk', 0.5)
            #Punch upgrade
            punch = util.fsearch(self.skills, lambda s: s.name == 'Punch')
            prev = punch.damage
            punch.damage += 0.5
            client.line(f'Punch was upgraded! {prev} DMG -> {punch.damage} DMG')
        elif level == 9:
            self.stat_change('atk', 0.5)
            self.obtain('Hyper Punch')
        else:
            self.stat_change('crit_mul', 0.05)

    def levelup_mana(self, level):
        self.stat_change('max_sp', 1)
        if level == 3:
            self.stat_change('starting_sp', 1)
            self.obtain("Lesser Brew")
        elif level == 6:
            self.stat_change('starting_sp', 1)
            self.obtain("Brew")
        elif level == 9:
            self.stat_change('starting_sp', 1)
            self.obtain("Greater Brew")

    def levelup_stealth(self, level):
        self.stat_change('dodge_chance', 0.02)
        self.stat_change('crit_chance', 0.02)
        if level > 3:
            self.stat_change('counter_chance', 0.05)

        if level == 3:
            self.obtain("Steal")
            self.counter = True
            client.line(f'{self} can now counter enemies!', 1.5)
            self.stat_change('counter_chance', 0.15, show_raise=False)
        elif level == 6:
            self.stat_change('counter_mul', 0.5)
        elif level == 9:
            self.obtain("Shadow")
        

    def levelup_utility(self, level):
        self.add_gold(5)
        self.stat_change('deck_slots', 1)
        if level == 3:
            self.stat_change('hand_slots', 1)
            self.add_gold(10)
            self.obtain("Discard 3")
            self.obtain("Refresh")
        elif level == 6:
            self.stat_change('hand_slots', 1)
            self.add_gold(15)
            self.obtain("Discard 4")
            self.obtain("Lookup")
        elif level == 9:
            self.stat_change('hand_slots', 1)
            self.add_gold(25)
            self.obtain("Discard 5")

    def stat_change(self, stat, amt, show_raise=True, show=True, buff=False, message=None):

        stat_text_replace = {
            'max_hp': "Max HP",
            'max_sp': 'Max SP',
            'starting_sp': 'Starting SP',
            'crit_chance': 'Crit Chance',
            'counter_chance': 'Counter Chance',
            'dodge_chance': 'Dodge Chance',
            'crit_mul': 'Crit DMG',
            'counter_mul': 'Counter DMG',
            'atk': 'ATK',
        }
        percent_values = ['crit_chance', 'counter_chance', 'dodge_chance', 'crit_mul'] #all properties that should be changed to percents

        if stat in stat_text_replace:
            stat_text = stat_text_replace[stat]
        else:
            stat_text = stat.replace("_", " ").title()

        old_val = getattr(self, stat)
        if type(amt) == bool:
            show_raise = False

            setattr(self, stat, amt)
            new_val = getattr(self, stat)
        else:   #int  
            setattr(self, stat, old_val + amt)
            new_val = getattr(self, stat)

        if buff and stat == "atk":
            self.atk_buffed += amt
        if buff and stat == "defense":
            self.defense_buffed += amt

        if stat in percent_values:
            old_val = util.percent(old_val)
            new_val = util.percent(new_val)

        if show:
            if message:
                client.line(message.format(user=self, old=old_val, new=new_val))
            else:
                if show_raise:
                    client.line(f'{stat_text}: {old_val} -> {new_val}')
                else:
                    client.line(f'{stat_text}: {new_val}')
            
        

    #Card related
    def turn_draw(self):
        if self.no_turn_draw_turns > 0:
            client.line(f'{self} cannot draw a card')
        else:
            self.draw(1)


    def draw(self, amt=1):
        for _ in range(amt):
            if not self.hand_full():                
                drawn_card = self.next_card
                self.hand.append(drawn_card)
                client.line(f'Drew {drawn_card.name}')
                self.next_card = copy.copy(random.choice( self.deck ))

                if drawn_card.cd > 0 and self.player:
                    drawn_card.cd = 0
            else:
                return client.line(f'{self.name}\'s hand is full. No card drawn.')

    def hand_full(self):
        #Returns true if the player's hand is full
        return len(self.hand) >= self.hand_slots

    def discard_card(self, card, say=True):
        #Send a card to discard.
        if not card in self.hand:
            print(card)
            raise Exception(f'{card} not in {self}\'s hand!')
        self.hand.remove(card)
        self.discard.append(card)
        if say:
            client.line(f'Discarded {card} from hand')

    def num_discard(self, amt=1, card_filter=lambda card: not card.being_used):
        #Randomly discards cards. -1 to discard all cards.
        if not self.player:
            return

        discardable = list(filter(card_filter, self.hand))
        if len(discardable) == 0:
            return client.line(f'{self} has no cards to discard!')

        if amt == -1:
            for card in discardable:
                self.discard_card(card, say=False)
            client.line(f'Discarded all cards from hand')
        else:
            for _ in range(amt):
                if len(discardable) > 0:
                    discarded_card = random.choice(discardable)
                    self.discard_card(discarded_card)
                    discardable.remove(discarded_card)
                else:
                    return client.line(f'{self}\'s hand is empty')

    def steal(self, target, amt=1):
        if not self.player:
            return
        
        if len(target.special_cards) < 1:
            return client.line(f'{target} has no stealable cards!')

        if type(amt) == tuple:
            amt = random.randint(amt[0], amt[1])

        for _ in range(amt):
            if self.hand_full():
                return client.line(f'{self.name}\'s hand is full')
                break

            stolen_card = random.choice(target.special_cards[:])
            stolen_card.move_type = 'card'
            self.hand.append(stolen_card)
            client.line(f'{self.name} stole {stolen_card.name} from {target.name}!')

    def immobility(self, turns):
        #Become immobile for this many turns. (If not already immobile, +1 to account for current turn)
        if self.immobile_turns > 0:
            self.immobile_turns += turns
        else:
            self.immobile_turns = turns + 1

    def no_turn_draw(turns):
        #Do not draw a card at start of turn for this many turns.
        if self.no_turn_draw_turns > 0:
            self.no_turn_draw_turns += turns
        else:
            self.no_turn_draw_turns = turns + 1

    # ==== GAME RELATED
    def changename(self):
        while True:
            while True:
                chosen_name = client.entry("Choose a player name:", f="text")
                if len(chosen_name) > 12:
                    client.line("That name's too long.")
                elif len(chosen_name) == 0:
                    chosen_name = "Lead"
                    break
                elif chosen_name.lower().strip() in ['0', 'cancel', 'quit', 'exit', 'back']:
                    return False
                elif valid_name(chosen_name):
                    break

            name_display = str(c.VIOLET2 if chosen_name=="Lead" else c.BEIGE) + chosen_name + c.RESET

            if client.entry(f'Are you sure you wish to be named {name_display}? You cannot change this later!', f='yes_or_no'):
                self.name = chosen_name
                return True


    # --- DISPLAY
    def display_moves(self, l="hand", format_string=True, return_string=False):
        def move_format(move):
            if self.player and format_string:     #These are split up becausse the Enemy class inherits the player's methods, and didnt want to define an entirely new method which is mostly the same
                return ('{c.RED}' if move.sp_cost > self.sp or move.le_cost > self.le or not move.validate_all(self) else '') + ('{c.BLUE}' if move.cd > 0 else '') + move.name + '{c.RESET}'
            else:
                return move.name
                
        string = str(', '.join(list(map(move_format, getattr(self, l)))))
        if return_string:
            return string
        else:
            client.line(string)


    def select_move(self, prompt='Enter a move to use:', use_actions=True, info=False):
        mode = 'hand'
        select_lists = {
            'hand': self.hand,
            'skill': self.skills,
            'action': self.actions
        }
        
        while True:
            selection = client.entry(prompt, f="text").lower().replace(' ','')

            if selection in list( select_lists.keys() ):
                mode = selection
                client.line(f'Number mode: {mode.capitalize()}', 0)

                select_list = select_lists[mode]
                move_string = ''
                for i, move in enumerate(select_list):
                    move_string += f'{i+1}. {move}\t'
                client.line(move_string, 0)
                continue

            actionFound = False
            for card in self.hand:
                if card.name.lower().replace(' ','') == selection:
                    return card
            for skill in self.skills:
                if skill.name.lower().replace(' ','') == selection:
                    return skill
            for action in self.actions:
                if action.name.lower().replace(' ','') == selection:
                    actionFound = True
                    if use_actions:
                        self.make_decision(action)
                        self.act()
                        continue
                    else:
                        return action
            if info:
                for card in self.deck:
                    if card.name.lower().replace(' ','') == selection:
                        return card
                for enemy in g.game.enemies:
                    for card in enemy.special_cards:
                        if card.name.lower().replace(' ','') == selection:
                            return card

            if selection.isdigit():
                select_index = int(selection) - 1
                select_list = select_lists[mode]

                if select_index >= 0 and select_index < len(select_list):
                    if mode == 'action' and use_actions:
                        actionFound = True
                        self.make_decision(select_list[select_index])
                        self.act()
                    else:
                        return select_list[select_index]
                else:
                    client.line('Not within range')

            if not actionFound:
                client.line('No move found with that name', t=0)

    def extra_turn(self):
        client.line(f'{self} gained an extra move!')

        self.in_extra_turn = True
        self.display_stats()
        self.make_decision()
        self.act()
        self.in_extra_turn = False

    def make_decision(self, move=None):
        #Choose a move, and select targets if needed. Additionally pass a move and select a target with it.

        if self.immobile_turns > 0:
            wait(1)
            return

        while True:
            while True:
                self.decision = move if move else self.select_move()
                if not self.decision:
                    continue
                if self.decision.check_all(self):   #Checks all conditionss to use, and prints a line and returns false if there is a missing requirement, otherwise true
                    break

            self.target = self.select_target()

            return True

    def select_target(self, target_type=None):
        if not target_type:
            target_type = self.decision.target_type

        if target_type == "one":  #Choose an enemy to target if target type is single
            if len(g.game.alive_enemies()) > 1:   #if there is only one enemy, there is no need to select an enemy
                return client.numchoice(g.game.alive_enemies(), prompt="Choose an enemy:", invalidprompt="Enter the enemy number", return_item=True)
            else:
                return g.game.alive_enemies()[0]

    def act(self):
        if g.game.check():  #Stop if the user is dead or all enemies are already dead
            return False

        if self.this_turn_effect:
            self.this_turn_effect(self, self.target)

        for aff in self.afflictions:
            if not aff.on_act(self):   #Will return false if the user cannot act
                return

        if self.immobile_turns > 0:
            if not self.this_turn_effect:   #Do not announce if a turn effect happened this turn, but still cancel action
                client.line(f'{self} cannot move!')
            return

        if self.decision in self.hand:
            self.discard_card(self.decision, say=False)
        self.decision.use(self)

        if self.decision.next_turn_effect:
            self.next_turn_effect = self.decision.next_turn_effect

def valid_name(name):

    banned_names = {
        "pedestrian": "This doesn't seem right.",
        "norshu": "Sorry, I don't accept identity theft.",
        "xuirbo": "Hey! It's MY job to crash the economy!",
        "tsoref": "Thou may not steal the title of the head of the forest.",
        "ardnut": "There is an impostor among us.",
        "cinaclov": "YOOOOOO! YOU CAN'T BE NAMED THAT!!! WHAAAAAAA!?!??!",
        "draug": "That name's taken, I guess.",
        "roam": "You dare try to steal my own name? From I, Roam!?",
        "advent": f"{c.RED}This is unforgivable...{c.RESET}"
    }

    valid = ':.\,^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGH IJKLMNOPQRSTUVWXYZ'
    if name.lower() in banned_names:
        client.dialog(banned_names[name.lower()], noinput=False)
        return False
    for char in name:
        if not char in valid:
            return False

    return True

#Used by the stat methods
stats = {
        'health': '{c.GREEN}', 
        'power': '{c.RED2}', 
        'mana': '{c.BEIGE}', 
        'stealth': '{c.VIOLET}', 
        'utility': '{c.YELLOW}'
    }
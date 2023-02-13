import random, copy

import client

import game as g
import util

move_list = []

move_type_set = "action"

class Move:
    item_type = 'move'
    
    def __init__(self, name, desc="A move", move_type=None, use_text=None, hit_count=1, crit_chance=None, crit_type='mult', miss_text=None, dodge_text=None, defend_text=None,
    validate = lambda user: True, validate_use=None, effect = lambda user: True, effect_target = lambda user, target: True, next_turn_effect=None, damage_formula=None,
    invalid_text=None, sp_cost=0, le_cost=0, damage=0, accuracy=0.95, target_type=None, tags=[], drain=0, undodgeable=False, uncounterable=False,
    cooldown=0, weight=10, uses=-1, priority=False):
        self.name = name
        self.target_type = target_type
        self.desc = desc

        self.sp_cost = sp_cost
        self.le_cost = le_cost
        self.damage = float(damage)

        self.accuracy = accuracy
        self.cooldown = cooldown       #The move's turn cooldown after using
        self.cd = self.cooldown       #Current cooldown, used during battle
        self.uses = uses      #Amount of times the move can be used per battle (applies to skills only)
        self.weight = weight    #Determine the AI use weight. Can be a number or function.
        self.priority = priority    #If ture, activates before the player, only applies to enemies.
        self.hit_count = hit_count
        self.undodgeable = undodgeable
        self.uncounterable = uncounterable
        self.crit_chance = crit_chance
        self.crit_type = crit_type

        if type(tags) == str:
            self.tags = [tags]
        else:   #list
            self.tags = tags
        self.drain = drain  #Whether or not to drain damage dealt

        if target_type:
            self.target_type = target_type
        else:
            if damage > 0:
                self.target_type = "one"
            else:
                self.target_type = "none"

        if use_text:
            self.use_text = use_text
        else:
            if self.target_type == "one":
                self.use_text = "{user} uses {move} on {target}"
            else:
                self.use_text = "{user} uses {move}"

        self.miss_text = miss_text
        self.dodge_text = dodge_text
        self.defend_text = defend_text

        if self.target_type == "none":
            self.accuracy = None

        global move_type_set
        self.move_type = move_type if move_type else move_type_set     

        self.validate = validate    #An optional function to determine if the move is usable by the player or enemy at the current moment (OTHER THAN CHECKING COSTS & COOLDOWN).
        self.invalid_text = invalid_text
        if not validate_use:
            self.validate_use = self.validate
        else:
            self.validate_use = validate_use

        self.effect = effect       #An optional effect of the move, i.e user.drawCards(2), leeroyRush(user, target).
        self.effect_target = effect_target   #Optional effect to run on each target. Works with single and all targeting moves.

        self.damage_formula = damage_formula #Optional, can be used to define a custom damage formula without making a function for it. damage_formula(user, target)

        #Sets the players' next_turn_effect to this. will be activated on the following turn by the user
        self.next_turn_effect = next_turn_effect    #format of lambda user, target: None.

        self.being_used = False   #used during gameplay to tell if the move is being used or not
        self.mulliganed = False     #used in mulligan player function, here for compatability

        global move_list
        move_list.append(self)

    def __str__(self):
        return self.name

    def check(self):
        def statif(stat, display=None, percent=None):
            val = getattr(self, stat.lower())
            if percent and val:
                val = util.percent(val)
            
            if val:
                val = str(val).capitalize()
                if display:
                    return client.bold(str(display)+": ")+val+'\t'
                else:
                    return client.bold(str(stat.replace("_", " "))+": ")+val+'\t'
            else:
                return ''

        client.set_line_delay(0)
        client.divider()
        client.line(f' -  {client.cb(self.name, "VIOLET")}  - ')
        client.line('  '+self.desc)
        if self.cd:
            client.line(f'Current cooldown: {self.cd}')
        client.line('  '+statif('move_type', 'Type'))
        client.line(f'  {statif("Damage")}{statif("Tags")}{statif("Accuracy", percent=True)}{statif("Target_Type")}')
        client.line(f'  {statif("SP_Cost")}{statif("LE_Cost")}{statif("Cooldown")}')
        client.divider()
        client.set_line_delay(1)

    def set_desc(self, desc=None, source=None):
        if desc:
            self.description = desc
        if source:
            self.source = source

    def move_use_text(self, user, target="the enemy"):
        if user == target:
            target = 'themself'
        if self.move_type != "action":
            client.line(self.use_text.format(user=user, move=self, target=target))

    def cooldown_tick(self, user):
        old = self.cd
        if self.cd:
            self.cd -= 1
            if self.cd > 0:
                client.line(f'{user}\'s {self} CD: {self.cd}', t=0.25)

        

    def use_on(self, user, target):
        if type(self.hit_count) == tuple:
            hit_count = random.randint(self.hit_count[0], self.hit_count[1])
        else:
            hit_count = self.hit_count

        hits = 0
        for _ in range(hit_count):
            hits += 1
            #Deal damage to target if this move has any damage, then run effect target
            if not self.move_type == 'action':
                if target.flying and not 'sky' in self.tags:
                    client.line(f'{target} is in the clouds!')
                    return

                if random.random() > self.accuracy:
                    if self.miss_text:
                        client.line(client.italic( self.miss_text.format(user=user, target=target, move=self) ))
                    else:
                        client.line(client.italic(f'{self} missed!'))
                    return

                if not self.undodgeable and not target.defending and user.player != target.player and random.random() < target.dodge_chance:
                    if self.dodge_text:
                        client.line(client.italic( self.dodge_text.format(user=user, target=target, move=self) ))
                    else:
                        client.line(client.italic(f'{target.name} dodged the attack!'))
                    return

                if self.damage > 0 or self.damage_formula:
                    #I dont care that this is unreadable as fuck
                    if self.defend_text and target.defending:
                        client.line(self.defend_text.format(user=user, target=target))

                    damage_dealt = user.deal_damage(target, self.damage_formula(user, target) if self.damage_formula else self.damage, self.crit_chance)
                    if self.drain and damage_dealt:
                        user.heal(damage_dealt * self.drain)
            self.effect_target(user, target)

            if g.game.check() or len(g.game.alive_enemies()) < 1:
                break

        if hit_count > 1:
            client.line(f'Hit {hits} time{"" if hits==1 else "s"}!')

    def validate_costs(self, user):
        #Validate that the user has the required SP and LE to use the move, and that cooldown is not up
        if user.player:
            return (user.sp >= self.sp_cost and user.le >= self.le_cost and self.cd == 0 and not self.uses == 0)
        else:
            return self.cd == 0

    def validate_all(self, user):
        #Checks both the moves' customiable validate function and checks costs/cd and stuff
        return (self.validate(user) and self.validate_costs(user))

    def get_weight(self, user):
        #A formula that determines the effectiveness of the move. Used by enemy AI.
        #Too lazy to  figure out how to code this right now so here is a static number, take it or leave it.
        if type(self.weight) == int or type(self.weight) == float:
            return self.weight
        else:
            return self.weight(user)

    def check_costs(self, user):
        #Sends lines if cannot deduct costs from user / cooldown/uses insufficient
        if self.uses == 0:
            client.line(f'{self} has no more uses!')

        if self.cd > 0:
            client.line(f"{user.name}'s {self.name} is on cooldown! Turns of cooldown left: {self.cd}")
            return False

        if user.player:
            if user.sp < self.sp_cost:
                client.line(f"{user.name} has insufficient SP to use {self.name}! Required SP: {self.sp_cost}")
                return False

            if user.le < self.le_cost:
                client.line(f"{user.name} has insufficient LE to use {self.name}! Required LE: {self.le_cost}")
                return False

        return True

    def check_validate(self, user, use=False):
        if use:
            valid = self.validate_use(user)
        else:
            valid = self.validate(user)
        if not valid:
            if self.invalid_text:
                if user.target:
                    client.line(self.invalid_text.format(user=user.name, move=self.name, target=user.target.name))
                else:
                    client.line(self.invalid_text.format(user=user.name, move=self.name))
            else:
                client.line(f'{self.name} cannot be used!')
            return False
        return True

    def check_all(self, user, use=False):
        return self.check_costs(user) and self.check_validate(user, use=use)

    def deduct_costs(self, user, use=False):
        #Deducts costs, and sends lines if it cannot deduct costs
        if not self.check_all(user, use=use):
            return False

        user.sp -= self.sp_cost
        user.le -= self.le_cost
        if not user.player:
            self.cd = self.cooldown
        return True

    def use(self, user):
        #Use the spell on a target.
        #User can be either a player or enemy

        #If the move cannot be used, the method will return false and the game will go back to move selection.

        game = g.game #for convenience

        if not self.deduct_costs(user, use=True):
            return False

        self.being_used = True
        if self.uses > 0:
            self.uses -= 1

        #Run this move's effect on each target, and deal damage if this moves' damage > 0
        if user.player:
            if self.target_type == "one":
                self.move_use_text(user, user.target)
                self.use_on(user, user.target)

            elif self.target_type == "random":
                self.move_use_text(user, user.target)
                self.use_on(user, random.choice(g.game.enemies))

            elif self.target_type == "all":
                self.move_use_text(user, "all enemies")
                for enemy in game.alive_enemies():
                    self.use_on(user, enemy)

            elif self.target_type == "everything":
                self.move_use_text(user, "everything")
                for enemy in game.alive_enemies():
                    self.use_on(user, enemy)
                self.use_on(user, user)

            elif self.target_type == "allies" or self.target_type == "ally":
                self.move_use(user, user)

            else:
                self.move_use_text(user)

            

        else:
            if self.target_type == "none":
                self.move_use_text(user)
            elif self.target_type == "everything":
                self.move_use_text(user, "everything")
                self.use_on(user, game.player)
                for ally in game.alive_enemies():
                    self.use_on(user, ally)
            elif self.target_type == "allies" or self.target_type == "alliesnotself":
                self.move_use_text(user, "all allies")
                for ally in game.alive_enemies():
                    if not ally == user or self.target_type == "allies":
                        self.use_on(user, ally)
            elif self.target_type == "ally":
                self.move_use_text(user, user.target)   #Should be an ally
            else:
                self.move_use_text(user, game.player)
                self.use_on(user, game.player)

        #after all target handling, run move effect
        self.effect(user)

        self.being_used = False


def move_from_string(string):
    if not type(string) == str:
        return string
    filter_list = list(filter(lambda move: move.name.lower().replace(' ','') == string.lower().replace(' ',''), move_list))
    if len(filter_list) > 0:
        return filter_list[0]
    else:
        raise Exception(f'No move found with name {string}')


# -------- Actions - Use at any time, does not use up turn
move_type_set = "action"

Move("Main", "Display the main battle window", target_type="none", effect=lambda user: user.display_stats())

Move("Stats", "Displays your full stats", target_type="none", effect=lambda user: user.check())

Move("Check", "Displays the stats of an enemy", target_type="one", accuracy=1, effect_target=lambda user, target: target.check())

Move("Info", "Look up the info of a move (Why are you looking this up?)", effect=lambda user: user.move_info())


# -------- Skills - Use at any time, uses up turn

move_type_set = "skill"

Move("Punch", "Deal 1 damage", damage=1, use_text="{user} punches {target}")

Move("Defend", "Raise DEF by 1 for a turn.", use_text="{user} defends!", weight=3, priority=True, target_type="none",
effect=lambda user: user.defend(1)) # used by the player and most enemies

Move("Life Transfer", "Gain 1 Life Energy", use_text="{user} charges life energy", effect=lambda user: user.gain_le(1))

Move("Testing", "Dont use this", damage=50, accuracy=1, undodgeable=True, target_type="all", use_text="{user} does the whip and nae nae")

# === Health
Move("Lesser Heal", "Recover 3 HP", sp_cost=1, use_text="{user} heals!", uses=5, effect=lambda user: user.heal(3))
Move("Heal",        "Recover 6 HP", sp_cost=1, use_text="{user} heals!", uses=5, effect=lambda user: user.heal(6))
Move("Greater Heal","Recover 9 HP", sp_cost=1, use_text="{user} heals!", uses=5, effect=lambda user: user.heal(9))

# === Power
# Lv 3
Move("Strong Punch", "Deal 3 damage and lose your next turn", damage=3, use_text="{user} punches {target} with high strength!", effect=lambda user: user.immobility(2))

def hyper_punch_next_turn_effect(user, target):
    client.line(f'{user} uses Hyper Punch!')
    user.deal_damage(target, 5)
    user.immobility(1)

def hyper_punch_effect(user, target):
    user.immobility(1)
    client.line(f'{user} charges up...')
    user.next_turn_effect = hyper_punch_next_turn_effect

# Lv 9
Move("Hyper Punch", "Charge up for a turn, then deal 5 damage, then lose your next turn", use_text="{user} uses Hyper Punch!", effect=hyper_punch_effect)

def isle_slash_effect(user):
    for enemy in g.game.alive_enemies():
        enemy.deal_damage(2)
Move("Isle Slash", "Deal 3 DMG, then 2 DMG to all enemies", damage=3, tags='slash', le_cost=1, use_text="{user} slashes {target} with {move}!", effect=isle_slash_effect)

# === Mana
Move("Lesser Brew", "Brew a Lesser Mana potion", use_text="{user} brews a potion...")
Move("Brew", "Brew a Lesser Mana potion", use_text="{user} brews a potion...")
Move("Greater Brew", "Brew a Lesser Mana potion", use_text="{user} brews a potion...")

# Steal
Move("Steal", "Steal a special card from the enemy", use_text="{user} steals from {target}...", effect_target=lambda user,target: user.steal(target))

Move("Shadow", "Avoid all attacks this turn, but no card drawn next turn", sp_cost=1, use_text="{user} hides in the shadows...")

Move("Discard 1", "Randomly discard one card from your hand", use_text="{user} discards cards...", effect=lambda user: user.num_discard(1))
Move("Discard 2", "Randomly discard two cards from your hand", use_text="{user} discards cards...", effect=lambda user: user.num_discard(2))
Move("Discard 3", "Randomly discard three cards from your hand", use_text="{user} discards cards...", effect=lambda user: user.num_discard(3))
Move("Discard 4", "Randomly discard four cards from your hand", use_text="{user} discards cards...", effect=lambda user: user.num_discard(4))
Move("Discard 5", "Randomly discard five cards from your hand", use_text="{user} discards cards...", effect=lambda user: user.num_discard(5))

Move("Scan", "Chance to learn a skill/card from the enemy", use_text="{user} scans {target}...")

Move("Refresh", "Discard a card from hand and draw 2 cards", sp_cost=1, uses=5, use_text="{user} refreshes...")

Move("Lookup", "Choose a card to draw. No card drawn next turn.", sp_cost=1, uses=5, use_text="{user} looks up a card...")

Move("Loot", "Deal 0.5 damage, with a chance to obtain items from the enemy", use_text="{user} loots {target}!")

Move("Wave", "Deal 0.5 damage to all enemies for each card in the user's hand", sp_cost=1, target_type="all", use_text="{user} casts {move}!", 
damage_formula=lambda user,target: len(user.hand)*0.5, tags='water')

Move("Thunder Blade", "Deal 7 damage and lose 1 HP", damage=7, tags='electric', use_text="{user} uses {move} on {target}!")

Move("Salt Rant", "Say a salty rant about the enemy")

# -------- Cards - Use from hand, uses up turn
move_type_set = "card"

Move("Slice", "Deal 2 damage", damage=2, tags='slash', use_text="{user} slices {target}!")

def shadow_effect(user):
    user.afflict('Shadow', 1, (1,3))     #If the affliction is successful this will return true
    user.no_turn_draw(2)
        
#Stealth lv9
Move("Shadow", "Gain +100% dodge chance for 1-3 turns. Do not draw a card next turn. Effect wears off when dealing damage", sp_cost=1, effect=shadow_effect )

Move("Stab", "Deal 1 DMG, deal 4 DMG if target is defending", use_text="{user} stabs {target}!", target_type='one', tags='pierce', 
damage_formula=lambda user, target: 4 if target.defending else 1, defend_text='{user}\'s defend was pierced!' )

Move("Hyper Slash", "Deal 4 damage, charge 1 LE and lose your next turn", damage=4, tags='slash', use_text="{user} hyper slashes {target}!", effect=lambda user: user.gain_le(1))

Move("Final Slash", "Deal 5 damage. Can only be used if it is the only card in your hand.", damage=5, tags='slash', use_text="{user} slashes {target}!", 
validate=lambda user: len(user.hand) == 1, invalid_text='Final Slash must be the only card in your hand!' )

Move("Sword of Greed", "Deal 4 damage", damage=4, tags='slash', use_text="{user} slashes {target} with the Sword of Greed!")

Move("Blade of the Stock Market", "Deal 6.9 damage", damage=6.9, tags='slash', use_text="{user} slashes {target} with the Blade of the Stock Market!")

Move("Wrath of the Ultimate Shareholder", "Deal 10 damage to all enemies", damage=10, target_type="all", use_text="{user} slashes {target} with the Blade of the Stock Market!")

def shuffle_effect(user):
    card_count = len(user.hand)
    user.num_discard(-1)    #Discard hand
    user.draw(card_count)   #Draw the same amount of cards

Move("Shuffle", "Discard your hand and draw as many as you had before", use_text="{user} shuffles their hand...", effect=shuffle_effect)

def salvage_effect(user):
    user.num_discard(3)
    user.draw(1)

Move("Salvage", "Discard 3 random cards and draw a card", use_text="{user} salvages cards...", 
effect=salvage_effect, validate=lambda user: len(user.hand) >= 4, validate_use=lambda user: len(user.hand) >= 3, invalid_text="{user} must have 3 or more other cards in their hand.")

Move("Recover", "Recover 5 HP", sp_cost=1, use_text="{user} recovers!", effect=lambda user: user.heal(5))

Move("Dual Magic", "Deal 2 damage and recover 2 HP", sp_cost=1, damage=2, tags='magic', effect_target=lambda user, target: user.heal(2))

Move("Fireball", "Deal 3 damage, 30% chance to burn for 2-4 turns", damage=3, tags='fire', accuracy=0.9, sp_cost=2, use_text="{user} casts {move} on {target}!", cooldown=3, weight=12,
effect_target=lambda user,target: target.afflict('burn', 0.3, (2,4)))

Move("Shock", "Deal 1.5 damage to all enemies, 30% chance to electrocute for 2-4 turns", tags='electric', sp_cost=1, damage=1.5, target_type="all", use_text="{user} casts {move}!",
effect_target=lambda user,target: target.afflict('electrocuted', 0.3, (2,4)))

Move("Volcanic Blast", "Deal 7.5 damage to all enemies", tags='fire', damage=7.5, sp_cost=4, target_type="all", use_text="{user} casts {move}!")

def rush_attack_target(user,target):
    damage_dealt = user.counter_chance * 10
    user.deal_damage(target, damage_dealt)
    if user.player and counter_chance/10 > random.random():
        user.stat_boost('counter_chance', 0.05)

Move("Rush Attack", "Deal 1 damage 2-4 times.", damage=1, hit_count=(2,4))

Move("ULT Recovery", "Heal 10 HP.", le_cost=3, accuracy=1, effect=lambda user: user.heal(10))

Move("ULT Sword", "Deal 7.5 damage.", tags='slash', le_cost=3, damage=7.5, accuracy=1,)

Move("ULT Blade", "Deal 10 damage.", tags='slash', le_cost=4, damage=10, accuracy=1,)

Move("ULT Magic", "Deal 5 damage and recover 5 HP.", tags='magic', sp_cost=2, le_cost=3, damage=5, accuracy=1, cooldown=5, effect_target=lambda user, target: user.heal(5))

Move("ULT Pierce", "Deal 4 damage. Will always crit if the target is defending", damage=4, accuracy=1, tags='pierce', le_cost=2, cooldown=6, weight=15)

Move("ULT Blast", "Deal 5 damage to all enemies", le_cost=4, damage=5, accuracy=1, target_type="all")

Move('ULT Smash', 'Deal 5 DMG and discard 2 cards from the targets\' hand', tags='blunt', le_cost=3, damage=5, accuracy=1, cooldown=6, weight=15,
effect_target=lambda user, target: target.num_discard(2))

Move("Pickpocket", "Steal 1-2 special cards from the enemy", target_type="one", use_text="{user} pickpockets {target}...", 
effect_target=lambda user,target: user.steal(target, (1,2)))

def leeroy_rush_effect(user):
    card_count = len(user.hand)
    user.num_discard(-1)    #Discard hand
    for i in range(card_count):
        if g.game.check():
            break
        client.line('LEEROY! '+str(i+1), 0.5)
        enemies = g.game.alive_enemies()

        user.deal_damage(random.choice(enemies), 1)

Move("Leeroy Rush", "Discard your hand and deal 1 damage to a random foe for each card discarded", effect=leeroy_rush_effect)

Move("Life Punch", "Deal 2 damage and gain 2 LE", sp_cost=1, damage=2, tags='plant', use_text="{user} life punches {target}!", effect_target=lambda user, target: user.gain_le(2))

def summoning_effect(user):
    user.draw(1)
    user.gain_sp(1)
    user.gain_le(1)

Move("Summoning", "Draw 1 card and gain 1 SP and LE", use_text="{user} uses summoning...", effect=summoning_effect)

Move("Lesser Mana Potion", "Gain 1 SP", use_text="{user} drinks {move}", effect=lambda user: user.gain_sp(1))
Move("Mana Potion", "Gain 2 SP", use_text="{user} drinks {move}", effect=lambda user: user.gain_sp(2))

Move("Lesser Healing Potion", "Heal 2 HP", use_text="{user} drinks {move}", effect=lambda user: user.heal(3))
Move("Healing Potion", "Heal 4 HP", use_text="{user} drinks {move}", effect=lambda user: user.heal(6))

def slime_potion_effect(user):
    user.heal(2)
    user.gain_mp(2)

Move("Slime Potion", "Heal 2 HP and 2 MP", use_text="{user} drinks {move}", effect=slime_potion_effect)

Move("Plunder", "Steal three special cards from the enemy", sp_cost=2, use_text="{user} plunders {target}...", 
effect_target=lambda user,target: user.steal(target, 3))

Move("Blast", "Deal 8 damage", damage=5, sp_cost=2, use_text="{user} uses {move} on {target}!")



#Crafted


Move("Wooden Sword", "Deal 2.5 damage", damage=2.5, tags='slash', use_text="{user} slashes {target}!")  #3 copper, 3 wood

Move("Stone Mace", "Deal 1.25 damage to all enemies", damage=1.25, target_type='all', tags='blunt', 
use_text="{user} smashes {target}!")  #3 copper, 2 wood, 1 stone

Move("Wooden Bow", "Deal 1 damage twice at range, 1.5x Crit Chance", damage=1, hit_count=2, crit_chance=1.5,
tags='pierce', uncounterable=True, accuracy=0.85, use_text="{user} shoots {target}!")  #3 copper, 2 wood, 1 cloth


Move("Copper Sword", "Deal 3 damage", damage=3, tags='slash', use_text="{user} slashes {target}!")  #3 copper, 3 wood

Move("Copper Mace", "Deal 1.5 damage to all enemies", damage=1.5, target_type='all', tags='blunt', 
use_text="{user} smashes {target}!")  #3 copper, 2 wood, 1 stone

Move("Copper Bow", "Deal 1 damage twice at range, doubled Crit Chance", damage=1, hit_count=2, crit_chance=2.0, 
tags='pierce', uncounterable=True, accuracy=0.9, use_text="{user} shoots {target}!")  #3 copper, 2 wood, 1 cloth


Move("Iron Sword", "Deal 3.5 damage", damage=3.5, tags='slash', use_text="{user} slashes {target}!")  #3 iron, 4 wood, 2 stone

Move("Iron Mace", "Deal 2 damage to all enemies", damage=2, target_type='all', tags='blunt', 
use_text="{user} smashes {target}!")  #3 iron, 1 copper, 1 wood, 5 stone

Move("Iron Bow", "Deal 1.5 damage twice at range, 1.5x Crit Chance", damage=1.5, hit_count=2, crit_chance=1.5, 
tags='pierce', uncounterable=True, accuracy=0.9, use_text="{user} shoots {target}!")  #3 iron, 3 wood, 2 cloth


Move("Steel Sword", "Deal 4 damage", damage=4, tags='slash', use_text="{user} slashes {target}!")  #3 steel, 6 wood, 3 stone

Move("Steel Mace", "Deal 2.5 damage to all enemies", damage=2.5, target_type='all', tags='blunt', 
use_text="{user} smashes {target}!")  #3 steel, 1 iron, 2 wood, 8 stone

Move("Steel Bow", "Deal 1 damage 3-5 times at range, doubled Crit Chance", damage=1, hit_count=(3,5), crit_chance=2.0, 
tags='pierce', uncounterable=True, accuracy=0.9, use_text="{user} shoots {target}!")  #3 steel, 6 wood, 1 stone, 3 cloth


Move("Crystal Sword", "Deal 4.5 damage", damage=4.5, tags='slash', use_text="{user} slashes {target}!")  #3 crystal, 6 steel

Move("Crystal Mace", "Deal 3 damage to all enemies", damage=3, target_type='all', tags='blunt', 
use_text="{user} smashes {target}!")  #3 crystal, 3 steel, 2 wood, 10 stone

Move("Crystal Bow", "Deal 1.5 damage 2-5 times at range, doubled Crit Chance", damage=1.5, hit_count=(2,5), crit_chance=2.0, 
tags='pierce', uncounterable=True, accuracy=0.975, use_text="{user} shoots {target}!")  #3 crystal, 3 steel, 10 wood, 2 stone, 5 cloth


#Enemy skills
move_type_set = "skill"

# ======= Slimes
# --- Red Slime
Move("Attack", "Deal 1 damage", damage=1, use_text="{user} attacks {target}") # used by most enemies

# Defend

def bounce_next_turn_effect(user, target):
    bounce_fall = move_from_string('Bounce Fall')
    bounce_fall.use(user)
    user.flying = False

def bounce_effect(user, target):
    user.immobility(1)
    client.line(f'{user} bounces into the air!')
    user.flying = True
    user.next_turn_effect = bounce_next_turn_effect

Move("Bounce", "Spring into the air. Deal 5 damage next turn with a 25% stun chance for 1 turn", target_type='one', undodgeable=True, accuracy=1.0, weight=15, cooldown=4, use_text='{user} uses {move}', effect_target=bounce_effect) # used by all slimes

Move("Bounce Fall", "Deal 5 damage, 25% stun chance for 1 turn", target_type='one', undodgeable=True, accuracy=0.95, damage=5, use_text='{user} lands on {target}!', 
effect_target=lambda user,target: target.afflict('stun', 0.25, 1 if user.player else 2)) # If used by player, only stuns for 1 turn, because canccelling 2 moves is kinda OP

# ======= Rogue
# --- Rogue Scout
#Attack, Defend

Move("Jab", "Deal 2 damage twice", damage=2, tags='pierce', hit_count=2, use_text="{user} jabs {target}", cooldown=3, weight=6)

Move("Sharpen", "Raise ATK by 0.5", use_text="{user} sharpens their blade...", effect=lambda self: self.stat_change('atk', 0.25, buff=True), weight=6)

#ULT Pierce

# --- Rogue Mage
#Attack, Defend

#Fireball

Move("Forcefield", "Give an ally a forcefield for 4 turns", target_type="ally", use_text="{user} protects {target} with a forcefield!", weight=16,
effect_target=lambda user, target: target.afflict("Forcefield", 1, 4))

#ULT Magic

# --- Rogue Brute
Move("Shield", "Raise DEF by 3 for a turn.", use_text="{user} shields!", weight=4, priority=True,
effect=lambda user: user.defend(3)) # used by the player and most enemies

Move("Spiky Balls", "Deal 0.5 DMG 3-6 times", damage=0.5, hit_count=(3,6), use_text="{user} throws some spiky balls!", cooldown=3, weight=6)

Move('Slam', 'Deal 3 DMG and discard a card from the enemy\'s hand', damage=3, tags='blunt', use_text="{user} slams {target}!", 
cooldown=4, weight=8, effect_target=lambda user, target: target.num_discard(1))

#ULT Smash

# --- Green Slime
#Attack, Defend, Bounce

Move("Healing Powder", "Heal all allies and self for 3 HP", use_text="{user} spreads healing powder!", target_type="allies", cooldown=4, weight=12, sp_cost=1,
effect_target=lambda user, target: target.heal(3))

Move("Poison Powder", "Poison all opponents, 75% chance for each", use_text="{user} spreads poison powder!", cooldown=4, weight=12, sp_cost=1,
target_type="all", effect_target=lambda user, target: target.afflict('poison', 0.75, (4,6), True))

# --- Blue Slime
#Attack, Defend, Bounce

Move("Explode", "Deal 10 damage to all allies and enemies", damage=10, target_type="everything", use_text="{user} self-destructs!!", cooldown=5, weight=25)


# ======= Spirits
# --- Plant Spirit
#Attack, Defend
Move("Spore", "Deal 3 damage, 30% chance to put target asleep for 3 turns", damage=3, tags='plant', accuracy=0.9, sp_cost=2, use_text="{user} casts {move} on {target}!", cooldown=3, weight=12,
effect_target=lambda user,target: target.afflict('asleep', 0.3, 3))

Move("Grassy Surge", "Give an ally +0.5 ATK, +0.5 DEF and heal 2HP per turn for 3 turns", use_text="{user} uses Grassy Surge on {target}!", target_type="ally", cooldown=4, weight=15, 
effect_target=lambda user, target: target.afflict("Grassy Surge", 1, 3))

# --- Ice Spirit
#Attack, Defend
Move("Ice Orb", "Deal 3 damage, 30% chance to freeze", damage=3, tags='ice', accuracy=0.9, sp_cost=2, use_text="{user} casts {move} on {target}!", cooldown=3, weight=12,
effect_target=lambda user,target: target.afflict('freeze', 0.3, -1))

# --- Fire Spirit
#Attack, Defend
#Fireball

Move('Combustion', 'Deal 1 DMG for each card in the target\'s hand', tags='fire',
damage_formula=lambda user, target: len(target.hand), target_type='one', cooldown=4, weight=11)

# Forcefield


# ======= Tundra
# --- Wolf
#Attack, Defend

def roar_effect(user, target):
    #If used by player (only by stealing probably), raise CD of all enemies' moves by 1
    for skill in target.skills:
        if user.player and not skill.name in ['Attack', 'Punch', 'Defend']:
            skill.cd += 1
            client.line(f'{skill} gained 2 cooldown! CD: {skill.cd}', 0.25)

    #then discard a card (Only works on the player, no effect when used on enemy)
    target.num_discard(1)

Move('Roar', 'Discard a random card from the target\'s hand and raise CD of all enemies\' skills by 2', target_type="all", use_text="{user} roars!", cooldown=2, weight=8, effect_target=roar_effect)

Move('Fang', 'Deal 2 DMG and drain 50% of DMG dealt. 30% chance to inflict Bleed for 2-4 turns.', use_text='{user} uses Fang on {target}!',
drain=0.5, cooldown=3, weight=16, effect_target=lambda user, target: target.afflict("Bleed", 0.3, (2,4)))


# ======= Volcanic
# --- Coal Entity
# Attack, Defend

def taunt_effect(user, target):
    target.target = user    #Sets the target of the player/enemy this is used on to the user
    client.line( '{target} fell for the taunt!' )

Move('Taunt', 'Redirect the target\'s moves to the user', priority=True, use_text='{user} taunts {target}!', target_type='one', 
accuracy=0.75, miss_text='{target} did not fall for the taunt!', undodgeable=True, effect_target=taunt_effect )

# ======= Bosses
# --- Tsoref
# Attack, Defend

def root_effect(user, target):
    target.root += 1
    client.line(f'A root is planted under {target}!')

Move("Root", "Deal 0.25 damage every turn to a target", tags='plant', weight=6)

Move("Wooden Rain", "Deal 1 damage 2-5 times", use_text='{user} rains down wooden spikes!', tags='plant', damage=1, target_type="all", hit_count=(2,5), weight=12, cooldown=4)

Move("Sap Punch", "Deal 3 DMG and drain damage dealt", damage=3, drain=1, weight=12, cooldown=4 )

# --- Ardnut
#Attack, Shield

#Ice Orb

Move("Blizzard", "Deal 2 damage to all enemies 2-4 times, 15% chance to freeze for each hit", tags='ice', damage=2, hit_count=(2,4), sp_cost=4, cooldown=5, weight=9, target_type="all", use_text="{user} casts {move}!")

Move("Spruce", "Raise ATK of all allies by 0.5", target_type='allies', effect_target=lambda user, target: target.stat_change('atk', 0.5, buff=True), weight=8, cooldown=5)

Move("Golem", "Summon a Stone Golem", effect=lambda user: g.game.spawn(user, 'Stone Golem'), weight=12, cooldown=7)

# --- Cinaclov

def heat_wave_effect(self, target):
    target.gain_sp(-1)
    target.gain_le(-1)
    if user.player:
        for skill in target.skills:
            if not skill.name in ['Attack', 'Punch', 'Defend']:
                skill.cd += 2
                client.line(f'{skill} gained 2 cooldown! CD: {skill.cd}')

Move('Heat Wave', 'Lower all targets\' SP and LE by 1 and raise CD of all moves by 2', target_type='all', sp_cost=1, cooldown=3, weight=7)

#Combustion

Move('Inferno', 'Deal 1.5 DMG to a random foe 2-5 times, 20% burn chance for 2-4 turns for each hit', use_text='{user} unleashes an inferno!', tags='fire',
target_type='random', damage=1.5, hit_count=(2,5), effect_target=lambda user, target: target.afflict('burn', 0.2, (2,4)), sp_cost=2, cooldown=5, weight=13)
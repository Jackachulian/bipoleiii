aff_list = []

import game as g
import client, random

class Affliction:
    def __init__(self, name, color='',
    afflict_text="{name} became afflicted with {aff}!", persist_text="{name} is afflicted with {aff}",
    remove_text="{name} is no longer afflicted with {aff}", cannot_move_text="{name} cannot move because of {aff}!",
    clear_text="", immune_text="{name} is immune to {aff}!",
    damage_per_turn=0, cannot_move=0, remove_chance=0, remove_tags=None, damage_clear_chance=0,
    atk_boost=0, def_boost=0, dodge_boost=0.0,
    turn_start=lambda user: None, turn_end=lambda user: None, act_effect=lambda user: None, 
    deal_damage_effect=lambda self, user, target, damage: None, take_damage_effect=lambda self, user, attacker, damage: None,
    afflict_effect=lambda self, user: None, remove_effect=lambda self, user: None):
        self.name = name
        self.color = color

        self.afflict_text = afflict_text    #Plays when afflicted
        self.persist_text = persist_text    #Plays at the start of each turn
        self.remove_text = remove_text      #Plays when the affliction wears off
        self.cannot_move_text = cannot_move_text    #Plays whenever the user cannot move during their turn because of this affliction
        if clear_text == "":
            self.clear_text = self.remove_text
        else:
            self.clear_text = clear_text
        self.immune_text = immune_text

        self.duration = 1   #Decreases by 1 at the start of each turn, then if at 0 removes, then runs effects if still active
        self.damage_per_turn = damage_per_turn  #takke this much damage each turn afflicted
        self.cannot_move = cannot_move      #A float between 0.0 and 1.0, the chance that the user cannot move during the turn when afflicted
        self.remove_chance = remove_chance  #Chance per turn for the affliction to be removed
        self.damage_clear_chance = damage_clear_chance    #Chance when damaged to clear self
        self.atk_boost = atk_boost
        self.def_boost = def_boost
        self.dodge_boost = dodge_boost

        if type(remove_tags) == str:      #When hit by moves with these tags, remove the affliction
            self.remove_tags = [remove_tags]
        else:
            self.remove_tags = remove_tags

        self.turn_start = turn_start    #Methods to play at the start and end
        self.turn_end = turn_end
        self.afflict_effect = afflict_effect    #Methods to run when affected, when acting and when removed
        self.deal_damage_effect = deal_damage_effect
        self.take_damage_effect = take_damage_effect
        self.act_effect = act_effect
        self.remove_effect = remove_effect

        global aff_list
        aff_list.append(self)

    def __str__(self):
        return self.name

    def on_afflict(self, user, dur):
        #Thhis is ran after this affliction is appended to the user's afflictions.
        self.duration = dur

        #Announce the beginning of this affliction's wrath
        client.line( self.afflict_text.format(name=user, aff=self) )  

        #Add buffs 
        if self.atk_boost:
            user.stat_change('atk', self.atk_boost, show=False)
        if self.def_boost:
            user.stat_change('defense', self.def_boost, show=False)
        if self.dodge_boost:
            user.stat_change('dodge_chance', self.dodge_boost, show=False)

        #Run afflict effect
        self.afflict_effect(self, user)
            

    def tick(self, user):
        self.turn_start(user)

    def end_tick(self, user):

        if self.duration != 1:
            client.line(self.persist_text.format(name=user, aff=self) + f' ({self.duration-1} turn{"" if self.duration == 2 else "s"} left)')
        elif self.damage_per_turn:
            client.line(self.persist_text.format(name=user, aff=self))

        if self.damage_per_turn:
            user.take_damage(None, self.damage_per_turn)

        if self.duration > 0:
            self.duration -= 1
        
        if self.duration == 0:
            self.remove(user)
            return

        

    def on_act(self, user):
        #Returns true if the user can act, and false if it has been stopped by something from this afflictio

        if random.random() < self.cannot_move:
            client.line(self.cannot_move_text.format(name=user, aff=self))
            return False

        return True

    def on_damage(self, user, attacker, damage):
        self.take_damage_effect(self, user, attacker, damage)

        if random.random() < self.damage_clear_chance:
            self.remove(user, clear=True)

    def remove(self, user, clear=False, announce=True):
        #Announce the removal of this affliction
        if announce:
            if clear:
                client.line(self.clear_text.format(name=user, aff=self))
            else:
                client.line(self.remove_text.format(name=user, aff=self))  

        #Remove buffs
        if self.atk_boost:
            user.stat_change('atk', -1*self.atk_boost, show=False)
        if self.def_boost:
            user.stat_change('defense', -1*self.def_boost, show=False)
        if self.dodge_boost:
            user.stat_change('dodge_chance', -1*self.dodge_boost, show=False)

        #Run remove effect
        self.remove_effect(self, user)  

        user.afflictions.remove(self)   #Remove from player aff list (which will delete this object, I think)
        
            

def aff_from_string(string):
    filter_list = list(filter(lambda move: move.name.lower().replace(' ','') == string.lower().replace(' ',''), aff_list))
    if len(filter_list) > 0:
        return filter_list[0]
    else:
        raise Exception(f'No affliction found with name {string}')

def all_affs(names=False):
    #Returns a list of all afflictions
    if names:
        return [aff.name for aff in aff_list]
    else:
        return aff_list

#Poison - 1 DMG per turn
Affliction('Poison', '{c.GREEN}', '{name} was poisoned!', '{name} is poisoned!', '{name}\'s poison wore off.', 
clear_text='{name}\'s poison was cured!', immune_text='{name} cannot be poisoned',
damage_per_turn=1)

#Burn - 2 DMG per turn
Affliction('Burn', '{c.RED2}', '{name} was lit aflame!', '{name} is burning!', '{name} has stopped burning.', 
clear_text='{name}\'s burn was extinguished!', immune_text='{name} is inflammable and cannot be burned',
damage_per_turn=2, remove_tags='water')

#Wet - -0.5 ATK, reduced accuracy
Affliction('Wet', '{c.BLUE}', '{name} is wet!', remove_text='{name} is now dry.', atk_boost=-0.5,
clear_text='{name}\'s wetness was dried!', immune_text='{name} is waterproof', remove_tags=['fire', 'electric'])

#Bleed - 0.5 DMG per turn, -0.5 DEF
Affliction('Bleed', '{c.RED}', '{name} is bleeding!', '{name} is bleeding!', '{name}\'s bleeding stopped.', def_boost=-0.5, damage_per_turn=0.5,
immune_text='{name} cannot bleed')

def confused_effect(user):
    if random.random() < 0.33:
        client.line('{name} can\'t think straight...'.format(name=user))
        if user.player:
            user.target = user
        else:
            user.target = random.choice(g.game.enemies)

#Confused - Chance to target ally/self when attacking
Affliction('Confused', '{c.VIOLET}', '{name} got confused!', '{name} is confused.', '{name} is no longer confused.',
act_effect=confused_effect)

#Stun - cannot move
Affliction('Stun', '{c.BOLD}', '{name} became stunned!', cannot_move_text='{name} is stunned and cannot move!', remove_text='{name} is no longer stunned', cannot_move=1, remove_chance=0.5)

#Electrocution - 50% chance of not being able to move each turn
Affliction('Electrocuted', '{c.YELLOW2}', '{name} became electrocuted!', persist_text='{name} is electrocuted', remove_text='{name}\'s electrocution wore off.', 
clear_text='{name}\'s electrocution was removed!', immune_text='{name} cannot be electrocuted', cannot_move=0.5,
cannot_move_text='{name} is paralyzed from electrocution!', remove_tags=['earth'])

#Asleep - cannot move, removes when taking damage
Affliction('Asleep', '{c.BEIGE2}', '{name} fell asleep!', '{name} is asleep.', '{name} woke up!', cannot_move_text='{name} is fast asleep...',
cannot_move=1, damage_clear_chance=1)

#Frozen - cannot move
Affliction('Freeze', '{c.BEIGE}', '{name} froze!', '{name} is still frozen!', '{name} is no longer frozen',
clear_text='{name} was melted!', immune_text='{name} cannot be frozen', remove_tags='fire',
cannot_move_text='{name} is frozen solid!', cannot_move=1, remove_chance=0.25, damage_clear_chance=0.25)

# - Buffs
#Grassy Surge - +0.5 ATK, +0.5 DEF, 2 HP healed per turn
Affliction('Grassy Surge', '{c.GREENBG2}', '{name} is fueled by grass energy!', remove_text='{name}\'s grassy surge wore off.',
atk_boost=0.5, def_boost=0.5, turn_end=lambda user: user.heal(2))

# Shadow - from stealth lv9 move
Affliction('Shadowed', '{c.GREY}', '{name} hides within the shadows...', remove_text='{name}\'s shadow wore off.', clear_text='{name} emerges from the shadows!',
dodge_boost=1.0, deal_damage_effect=lambda self, user, target, damage: self.remove(user, clear=True))

Affliction('Lesser Boost', '{c.RED2}', '{name} is boosted!', remove_text='{name}\'s boost wore off.',
atk_boost=0.5)

Affliction('Boost', '{c.RED2}', '{name} is boosted!', remove_text='{name}\'s boost wore off.',
atk_boost=1)

Affliction('Greater Boost', '{c.RED2}', '{name} is boosted!', remove_text='{name}\'s boost wore off.',
atk_boost=1.5)


def forcefield_on_afflict(self, user):
    self.forcefield_hp = 10

def forcefield_take_damage(self, user, attacker, damage):
    old_hp = self.forcefield_hp
    self.forcefield_hp -= damage
    if self.forcefield_hp < 0:
        self.forcefield_hp = 0
    client.line(f'{self}\'s forcefield takes {damage} damage ({old_hp} -> {self.forcefield_hp})')
    if self.forcefield_hp <= 0:
        self.remove(user, clear=True)

#Forcefield - +3 DEF, breaks when the forcefield takes 10 damage
Affliction('Forcefield', '{c.BLUE2}', '{name} is surrounded by a forcefield!', '{name} is protected by a forcefield!', '{name}\'s forcefield wore off.', clear_text='{name}\'s forcefield shattered!',
def_boost=3, afflict_effect=forcefield_on_afflict, take_damage_effect=forcefield_take_damage)
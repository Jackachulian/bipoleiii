import random, copy

import game as g
game = g.game

import client, moves, util, areas
from colors import TextCodes as c

import player

enemy_list = []

class Enemy(player.Player): #Inherits from the player (This class inherits most of its methods from the player)
    player = False

    def __init__(self, name, hp=10.0, atk=1.0, xp=(3,7), gold=(3,7), defense=1.0,
    skills=["Attack", "Defend"], special_cards=["Life Punch", "Summoning", "Mana Potion", "Healing Potion", "Leeroy Rush"], 
    crit_chance=0.1, crit_mul=1.5, dodge_chance=0.05,
    counter=False, counter_chance=0.15, counter_mul=1.5, heal_mul=1,
    hit_passive=lambda self, attacker: None, post_hit_passive=lambda self, attacker: None,
    turn_start_passive=lambda self: None, turn_end_passive=lambda self: None, defeat_passive=lambda self: None,
    drops=[], scan_drops=[], loot_drops=[], desc=""):
        self.name = name
        self.rname = name #Name may be altered by game.rename_enemies, use this in check() to return the root name
        self.troop_order = 0  #Used at the start of the battle, it is the order that the enemies are displayed in lists
        self.scanned = False    #Reveals additional information after an enemy of its type has been scanned

        self.desc = desc    #Description when checked
        
        self.max_hp = hp
        self.hp = hp
        self.dead = False

        self.afflictions = []

        self.skills = skills

        self.gold = gold
        self.xp = xp

        self.special_cards = special_cards
        self.drops = drops
        self.scan_drops = scan_drops
        self.loot_drops = loot_drops
        
        self.atk = atk    #all damage is multiplied by this
        self.defense = defense      #all incoming damage is divided by this (unless CRIT)
        self.defending = False
        self.defending_amt = 0
        self.heal_mul = heal_mul     # Multiplies incoming healing
        
        self.counter = counter       #boolean of whether or not the player can counter
        self.counter_chance = counter_chance
        self.counter_mul = counter_mul      #damage mul when counterattacking
        self.crit_chance = crit_chance
        self.crit_mul = crit_mul
        self.dodge_chance = dodge_chance

        self.atk_buffed = 0
        self.defense_buffed = 0
        self.frigid_buffed = 0      #Defense from Ardnut's frigid ability

        self.max_sp = 0
        self.sp = 0
        self.le = 0
        self.starting_le = 0    #Purely for compatability, no moves will likely use these values if they are on an enemy

        self.immobile_turns = 0     #Some moves cause you to not be able to act for a certain amount of turns
        self.flying = False       #Only specific moves will target oyu, otherwise dodge all. used on Bounce move

        self.decision = None
        self.target = None      #Used only in ally-targeting effects for enemies

        self.hit_passive = hit_passive
        self.post_hit_passive = post_hit_passive
        self.turn_start_passive = turn_start_passive
        self.turn_end_passive = turn_end_passive
        self.defeat_passive = defeat_passive

        self.next_turn_effect = None    #Set by some moves
        self.this_turn_effect = None    #End ov every turn, next_turn_effect is moves to this_turn_effect and next_turn_effect is cleared. this_turn_effect runs on turn, 
        #usually the user is immobile from a bounce or bounce/like move and will now be able to be targeted

        self.renamed = False    #Used in enemy renaming function, specifially useful when other enemies are spawned

        self.root = 0   #Tsoref's move, player can technically steal root from Tsoref so this should be here

        self.strings_to_moves()

        for skill in self.skills:
            if not skill.name in ['Attack', 'Defend']:
                s = copy.deepcopy(skill)
                s.cooldown = 0
                s.cd = 0
                self.special_cards.append(s)

        global enemy_list
        enemy_list.append(self)

    def __str__(self):
        return self.name

    # ==== INFO
    def check(self):
        client.set_line_delay(0)
        client.divider()
        client.line(f' -  {c.VIOLET}{self.name}{c.RESET} -  ')
        client.line(f'  {c.BOLD}HP:{c.RESET} {self.hp}/{self.max_hp} \t{c.BOLD}ATK:{c.RESET} {self.atk}\t\t{c.BOLD}DEF:{c.RESET} {self.defense}')
        if self.scanned:
            client.line(f'  {c.BOLD}Crit Chance:{c.RESET} {util.percent(self.crit_chance)}\t{c.BOLD}Crit DMG:{c.RESET} +{util.percent(self.crit_mul-1.0)}\t{c.BOLD}Dodge Chance:{c.RESET} {util.percent(self.dodge_chance)}')
            client.line(f'  {c.BOLD}Special Cards:{c.RESET} {self.display_moves("special_cards", return_string=True)}')

        client.line(f'  {c.BOLD}Skills:{c.RESET}  ')
        for move in self.skills:
            client.line(f'    {move.name}\tCD: {move.cd}/{move.cooldown}')

        client.line('\n'+self.desc)
        client.divider()
        client.set_line_delay(1)

    # ==== MOVES
    def strings_to_moves(self): #(Overrides player)
        self.skills = [copy.copy(moves.move_from_string(skill)) for skill in self.skills]
        self.special_cards = [moves.move_from_string(skill) for skill in self.special_cards]


    # ==== DAMAGE
    # deal_damage() inherit from player

    # take_damage() from player
    
    # defend()

    def defeat(self):
        self.dead = True
        client.line(f'{self.name} was defeated!')

        self.defeat_passive(self)

        game = g.game
        player = g.game.player

        #Clear afflictions
        for aff in self.afflictions:
            aff.remove(self, announce=False)

        # Gain drops
        #Format: (item, chance, rolls, minimum)
        for drop in self.drops:

            if type(drop) == str:
                item = drop
                chance = 1
                rolls = 1
                minimum = 0
            else:   #Tuple
                if len(drop) == 4:
                    item, chance, rolls, minimum = drop
                else:
                    item, chance, rolls = drop
                    minimum = 0

            amt = 0
            for _ in range(rolls):
                if chance > random.random():
                    amt += 1

            if minimum > amt:
                amt = minimum

            if amt > 0:
                player.obtain(item, amt)

        # User gains gold and XP (Gold and XP are tuples of two or integers)
        if type(self.gold) == tuple:
            gold = random.randint(self.gold[0], self.gold[1])
        else:
            gold = self.gold

        if type(self.xp) == tuple:
            xp = random.randint(self.xp[0], self.xp[1])
        else:
            xp = self.xp

        # - On first level, when slime is defeated, XP gained will always be at least 5
        if game.area == areas.port and game.level == 1 and xp < 5:
            xp = 5

        player.add_gold(gold)
        player.gain_xp(xp)


    # ==== BATTLE
    def make_decision(self):    
        #The enemy makes their decision at the start of the turn, before the player attacks, and attacks after the player acts. 
        # Certain moves activate before the player, but most happen after the player attacks.
        if self.dead:
            return

        if self.immobile_turns > 0:
            return
        
        usable_moves = list( filter( lambda move: move.validate_all(self), self.skills ) )

        if len(usable_moves) == 0:
            self.decision = None
            return

        move_weights = list( map(lambda move: move.get_weight(self), usable_moves) )

        self.decision = random.choices(usable_moves, weights=move_weights)[0]

        if self.decision.target_type == "ally":
            self.target = random.choice(g.game.enemies)
        else:
            self.target = g.game.player

        if self.decision.priority:      #Activate immediately if priority move (like Defend)
            self.act(priority_activate=True)

    def act(self, priority_activate=False):
        if self.dead:
            return

        if g.game.check():
            return

        if self.this_turn_effect:
            self.this_turn_effect(self, self.target)

        for aff in self.afflictions:
            if not aff.on_act(self):   #Will return false if the user cannot act
                return

        if self.immobile_turns > 0:
            if not self.this_turn_effect:   #Do not announce if a turn effect happened this turn, but still cancel action
                client.line(f'{self} cannot move!')
            return
            
        if not self.decision:
            self.make_decision()
            if not self.decision:
                return client.line(f'{self.name} has no usable moves!')

        if self.decision.priority and not priority_activate:
            #If the move is priority and it is NOT being priority used, then return.
            #If the move is priority and it is being activated at the start via make_decision, then continue
            return

        self.decision.use(self)

        if self.decision.next_turn_effect:
            self.next_turn_effect = self.decision.next_turn_effect

    # --- DISPLAY
    # display_moves()


def spawn_enemy(user, spawned):
    game = g.game
    enemy = enemy_from_string(spawned)
    game.enemies.append(enemy)
    game.init_enemies()
    client.line(f'Spawned {enemy}')


def enemy_from_string(string):
    filter_list = list(filter(lambda enemy: enemy.name.lower().replace(' ','') == string.lower().replace(' ',''), enemy_list))
    if len(filter_list) > 0:
        return copy.deepcopy(filter_list[0])
    else:
        raise Exception(f'No enemy found with name {string}')

# ======= Slimes
Enemy('Red Slime', 8.0, 1.0, skills=["Attack", "Defend", "Bounce"],
drops=[('Slime', 0.5, 5)], xp=(3,7), gold=(3,7),
desc="A common Red Slime. Legends say that they mark the start of a grand quest. While not very powerful, you shouldn't underestimate them.")

def green_slime_passive(self, attacker):    #Post-hit passive
    #When hit, 25% chance to poison the attacker for 2-4 turns
    attacker.afflict('poison', 0.25, (2,4), dodge_announce=False)

Enemy('Green Slime', 12.0, 0.5, skills=["Attack", "Defend", "Bounce", "Healing Powder", "Poison Powder"], post_hit_passive=green_slime_passive,
drops=[('Slime', 0.6, 5), ('Wood', 0.25, 10)], xp=(6,10), gold=(3,7),
desc="Weak but potent, Green Slimes inhabit the deep forests of Rogue. Their toxin is strong, so travelers should take caution when enraging one. They also have a nature to protect their fellow slimes with their healing.")

def blue_slime_passive(self, attacker): #Post-hit passive
    #When hit with a Fire move, fucking die
    pass    #ill code this once damage tpyes are implemeneted

Enemy('Blue Slime', 4.0, 3.0, dodge_chance=0.2, skills=["Attack", "Defend", "Bounce", "Explode"], post_hit_passive=blue_slime_passive,
drops=[('Slime', 0.4, 5)], xp=(3,7), gold=(6,10),
desc="A highly dangerous slime. When they get angry, they have a tendency to self-destruct on their opponents. They are also highly flammable and should not get anywhere near fire, lest they cause a deadly explosion.")

def black_slime_passive(self):  #Defeat passive
    client.line(f'{self} splits in half!')
    spawn_enemy(self, 'Red Slime')
    spawn_enemy(self, 'Red Slime')

Enemy('Black Slime', 16.0, 2.0, skills=["Attack", "Defend", "Bounce"], defeat_passive=black_slime_passive,
drops=[('Slime', 0.3, 8)], xp=(6,9), gold=(6,9),
desc='Black Slimes are beasts of slimes, and have been known to split into smaller parts when in danger.')

# ======= Rogue
Enemy('Rogue Scout', 12.0, 1.5, counter=True, crit_chance=0.15,
skills=['Attack', 'Defend', 'Jab', 'Sharpen', 'ULT Pierce'],
drops=[('Wood', 0.5, 5), ('Copper', 0.25, 5)], xp=(4,10), gold=(6,14),
desc='A low-level recruit from Rogue, sent out to scout out the lands of Rogue and eliminate suspicious activity. Wields a copper-tipped spear.')

Enemy('Rogue Mage', 16.0, 1.5, counter=True, crit_chance=0.15, skills=['Attack', 'Fireball', 'Forcefield', 'ULT Magic'])

Enemy('Rogue Brute', 24.0, 3.0, counter=True, crit_mul=2.0, skills=['Attack', 'Shield', 'Spiky Balls', 'Slam', 'ULT Smash'],
drops=[('Rogue Badge', 1, 1), ('Wood', 0.75, 4), ('Copper', 0.1, 10), ('Iron', 0.25, 5)], xp=(8,15), gold=(12,18),
desc="A powerful force of the Rogue Nation to be reckoned with. Wields an iron shield and club.")

# ======= Spirits
Enemy('Plant Spirit', 16.0, 2.0, skills=["Attack", "Defend", "Spore", "Grassy Surge"])

Enemy('Ice Spirit', 16.0, 2.0, skills=["Attack", "Defend", "Ice Orb", "Forcefield"])

Enemy('Fire Spirit', 16.0, 2.0, skills=["Attack", "Defend", "Fireball", "Combustion"])


# ======= Tundra
def fierce(self, attacker):   #Post hit passive
    if util.rng( 0.30 ):
        print('{self} firecely roars!')
        self.stat_change('atk', 0.25, buff=True)

Enemy('Wolf', 11.0, 1.0, counter=True, counter_chance=0.20, skills=["Attack", "Defend", "Roar", "Fang"],
post_hit_passive=fierce)

# ======= Volcanic
def burst(self):    #Defeeat passive
    client.line('{self} bursts!')
    player.deal_damage(g.game.player, 2)
    for enemy in g.game.enemies:
        if not enemy == self:
            player.deal_damage(enemy, 2)

Enemy('Coal Entity', 5.0, 2.5, defense=4.0, skills=["Attack", "Defend", "Taunt"])

# ======= Bosses
Enemy('Tsoref', 40.0, 3.0, heal_mul=2.0, skills=["Attack", "Defend", "Root", "Wooden Rain", "Sap Punch"])

def frigid(self, attacker): #Post hit passive
    hp_percent = self.hp / self.max_hp

    frigid_map = {
        0.75: 0.5,
        0.5: 1.0,
        0.35: 1.5,
        0.25: 2,
        0.15: 2.5,
        0.1: 3.0
    }

    prev_frigid = self.frigid_buffed
    for val in frigid_map:
        if hp_percent >= val:
            self.frigid_buffed = frigid_buffed[val]
            break

    total_frigid_buffed = self.frigid_buffed - prev_frigid

    if total_frigid_buffed: #If there is any change, announce the change
        #Only announce frigid if Frigid goes up, but still change DEF if healed above a frigid threshold
        if total_frigid_buffed > 0:
            client.line(f'{self}\'s Frigid activates!')
        self.stat_change('defense', total_frigid_buffed)

Enemy('Ardnut', 40.0, 2.0, skills=["Attack", "Defend", "Blizzard", "Spruce", "Golem"], post_hit_passive=frigid)


def escalation(self):    #Turn end passive
    self.stat_change('atk', 0.25, buff=True)

Enemy('Cinaclov', 32.0, 2.0, skills=["Attack", "Defend", "Heat Wave", "Combustion", "Inferno"], turn_end_passive=escalation)

Enemy('Draug', 50.0, 3.5,
desc="Draug believes he isn't paid enough for his work. You'd be suprised how many people try to steal boats on this dock; and it's his, and ONLY his, job to protect them from thieves like you.")


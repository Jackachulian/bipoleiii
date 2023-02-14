import math, random

import game as g
import moves, items, areas, util
from client import *

norshu = []
xuirbo = []
current_shop = norshu

class ShopItem:
    def __init__(self, name, cost, buy_comment='', broke_comment='', quantity=3, cost_difference=5,
    itemname=None, itemtype=None, no_requirement_message='', requirement=lambda user: True, condition=None,
    upgrade=False, run_upgrade=lambda user: True):

        self.cost = cost
        self.mood_cost = cost #Current cost, which is infuenced by Norhsu's mood
        self.requirement = requirement

        #Find the matching item
        #Check moves
        self.name = name
        self.itemname = itemname
        if not self.itemname:
            self.itemname = self.name

        self.upgrade = upgrade
        self.run_upgrade = run_upgrade

        self.itemtype = itemtype
        if itemtype:
            if itemtype == 'move':
                self.item = moves.move_from_string(self.itemname)
            elif itemtype == 'upgrade':
                self.item = name
            else:   #Item
                items.item_from_string(self.itemname)
        else:
            if not self.upgrade:
                item = items.item_from_string(self.itemname)
                if item:
                    self.item = item
                else:
                    self.item = moves.move_from_string(self.itemname) 
            else:
                self.item = name        

        self.condition = condition #at every post game, run this to see if it should appear in the shop yet. lambda/tuple
        self.appeared = False

        self.buy_comment = buy_comment
        self.broke_comment = broke_comment

        self.quantity = quantity
        self.cost_difference = cost_difference  #Cost goes up by this much on each buy

        current_shop.append(self)

    def __str__(self):
        if type(self.item) == str:  #Upgrade name / other random thing
            return self.item
        else:   #Item/move object
            return self.item.name

    def item_string(self, user):
        cost = f'({self.cost}G)\t' if self.cost else '\t'
        name = str(self)+'\t'
        return f'{cost}{name}'

    def enough_gold(self):
        return g.game.player.gold >= self.cost

    def can_buy(self):
        user = g.game.player
        return self.enough_gold() and self.requirement(user) and self.quantity > 0

    def say_broke_comment(self):
        norshu_broke_comments = [
            'Sorry {name}, I don\'t give credit.',
            f'Come back when you\'re... hmm... {bold("NOT  POOR")}',
            'I also have lamp oil, ropes, and bombs, but you probably can\'t afford them either.',
            f'I diagnose you with {bold("NOT RICH")}',
            'Someone hasn\'t been sacrificng their savings account to the stock market.',
            'I smell plebians.',
            'I would hire you, but you\'re too poor.',
            'Come back when you\'re not working minimum wage.'
        ]

        if self.broke_comment == '':
            line(random.choice(norshu_broke_comments).format(name=g.game.player))
        else:
            line(self.broke_comment.format(name=g.game.player))

    def check_condition(self):
        cond = self.condition
        user = g.game.player
        
        if type(cond) == list:  #Check each condition, and if one is not met then stop. If all do not return stop then all are met.
            for c in cond:
                if not self.parse_cond(c):
                    return False
            return True

        else:   #single condition, check if condition met
            return self.parse_cond(cond)
        
    def parse_cond(self, cond):
        user = g.game.player
        game = g.game

        if cond:
            if type(cond) == tuple:
                if cond[0] == 'area':
                    if len(cond) > 1:
                        if cond[1] == 'split':
                            return game.area in (areas.forest, areas.tundra, areas.volcanic)
                        else:
                            check_area = getattr(areas, cond[1])
                        if not game.area == check_area:
                            return False

                        level = cond[2]
                        return game.level >= level
                    else:
                        check_area = getattr(areas, cond[1])
                        return game.area == check_area

                elif cond[0] == 'level':
                    return user.level >= cond[1]
                    
                elif cond[0] in ['health', 'power', 'mana', 'stealth', 'utility']:
                    return getattr(user, 'level_'+cond[0]) >= cond[1]

            else:   #only other type is lambda
                return self.condition(user)
        else:
            return True

    def buy(self):
        #Attempt to buy the item, and if cannot return none. If bought, return true
        user = g.game.player

        if not self.quantity > 0:
            line(f'{self} is out of stock.')
            return

        if not self.requirement(user):
            line(self.no_requirement_message.format(name=user))
            return

        if not self.enough_gold():
            line(self.say_broke_comment())
            return

        user.gold -= self.cost

        line(self.buy_comment)

        if self.upgrade:
            self.run_upgrade(user)
        else:
            user.obtain(self.item)

        self.quantity -= 1

        return True

    def add_to_shop(self, quantity=None, announce=True, shop=None):
        if not shop:
            shop = norshu

        if not quantity:
            quantity = self.quantity

        if self.name in [i.name for i in shop]:
            same_item = list( filter(lambda i: i.name == self.name, shop) )[0]
            if same_item.appeared:
                same_item.quantity += quantity
                if announce:
                    line(f'{self} has been restocked!')
                    return 'restock'
            else:
                self.appeared = True
                if announce:
                    line(f'Norshu is now selling {self}!')
                    return 'new'
            
        else:
            shop.append(self)
            self.appeared = True
            if announce:
                line(f'Norshu is now selling {self}!')
                return 'new'

# NO LONGER IN SHOPITEM CLASS

def list_items(shop=None):
    if not shop:
        shop = norshu

    i = 0
    for item in shop:
        if not item.appeared and not g.game.shop_show_all:
            continue

        number = f'{i+1}. '
        color = '' if item.can_buy() else '{c.GREY}'
        quantity = f'[{item.quantity}] ' if item.quantity >= 0 else ''
        name = item.name+'\t'
        cost = f'({item.cost}G)\t'
        line(f'{color}{number}{quantity}{name}{cost}', 0)

        i += 1

def find_item(shop=None):
    if not shop:
        shop = norshu

    while True:
        selection = entry('What do you want to buy?', f='text').lower().replace(' ','')

        if selection in ['0', 'no', 'nothing', 'fuckoff', 'cancel', 'back', 'quit', 'exit']:
            return False

        if selection == "list":
            list_items()
            continue

        i = 0
        for item in shop:
            if not item.appeared and not g.game.shop_show_all:
                continue

            if item.name.lower().replace(' ','') == selection:
                return item
            if selection.isdigit():
                if i+1 == int(selection):
                    return item

            i += 1
        
        line('No item found with that number', 0)

def update_shop(shop=None, announce=True):
    #Updates the shop before each post-battle, announcing the new items added
    if not shop:
        shop = norshu

    new_list = []
    restock_list = []

    for item in shop:
        if not item.appeared and item.check_condition():
            add_type = item.add_to_shop(announce=False)
            if add_type == 'new':
                new_list.append(item)
            elif add_type == 'restock':
                restock_list.append(item)
    
    if announce:
        if new_list:
            line(f'Norshu is now selling: { util.sep_list( new_list ) }!')
        if restock_list:
            line(f'Norshu has restocked: { util.sep_list( restock_list ) }!')
    

def talk(s=None):

    mood = norshu_mood
    if mood == 0:
        mood = 0.1

    talk_list = norshu_talking[math.ceil(mood)-1]  #Will be a list of speech tuples

    speech = random.choice(talk_list)   #Will be a tuple

    if type(speech) == tuple:
        for s in speech:
            dialog(s.format(name=g.game.player))
    else:
        dialog(speech.format(name=g.game.player))

    return True

def greeting(s=None):
    norshu_greetings = [
        'Lamp oil, ropes, bombs? They\'re yours, {name}, as long as you have enough GOLD!',
        'Welcome, {name}. Here to give me gold for some uselsss stuff again?',
        'Welcome back, my one and only loyal customer.',
        'mmmmmmmmmmmmmmmmmmm?',
        'I sell only the finest wares in the land! ...What\'s this about me having only one customer? ...Irrelevant!',
        '**TRADE DEAL** I receive all your savings, you receive a crappy blade.',
        'YOOOOOOOOOOO!!!'
        'Always remember, {name}, I don\'t accept credit.'
    ]

    line('Norshu: '+random.choice(norshu_greetings).format(name=g.game.player))

def parting(s=None):
    norshu_partings = [
        'Come back when you\'re a little more... mmmm... RICHER!',
        'Finally, more money to invest in GME...',
        'Aight, I\'mma head out.',
        'Goodbye, number 1 customer!',
        'Farewell.',
        'See ya when youre... mmmm... RICHER!!!',
        'Thanks for buying some random crap I found on an abandoned street!',
        'Another day gone without being shoplifted.'
    ]

    line(random.choice(norshu_partings))

norshu_mood = 3
norshu_price_mul = 1 - 0.5*round(norshu_mood-3)

norshu_talking = [
        [   #Mood 0=<
            ('Y\'know, {name}, I have a pistol...', 'And I\'m not afraid to be charged with multiple crimes...', 'I\'ve done enough tax evasion in my days to know how to avoid charges from the government.', 'Don\'t tell Isle I said that.'),
            ('I pity you. You don\'t even have a hundredth of what I own in wealth.'),
            ('Begone, shoplifter...', 'You\'re not worth my time.'),
            ('If only I weren\'t contractually obligated to assist you on this journey...'),
            ('Fool... Why must you pester me? I hope your ULT Sword misses and you die to a Red Slime.')
        ],
        [   #Mood 1<
            ('You really want to bribe me out of my precious lamp oil, ropes and bombs? Eh, {name}?', 'I\'ve been doing shopkeeping far too long to know the difference between a scam and a bargain.'),
            ('You\'re acting real sus over there. Don\'t think you can get away with a quick one; I\'ve punished many shoplifters in the past.'),
            ('Why must you inquire to speak with me? Are you trying to lighten up to me so you can ease me into giving away my precious wares?', 'Nice try. Though I must add, I commend your ambition for bargaining.', 'Just... try it on someone who is more naive next time.'),
            ('I\'m starting to regret going with you on this jorney...' '*sigh* Governmental obligations, SMH...', 'Now I have another problem to deal with, alongside my mass tax evasion...'),
            ('Y\'know, I was never really fond of Isle anyways.', 'They\'re just full of fools who wouldn\'t know how to spend their coins if their lives depended on it... Pitiful.')
        ],
        [   #Mood 2<
            ('So, {name}, regretting starting this journey yet, eh?', 'Don\'t worry, I\'ll be sure to keep good care of your precious gold!', 'Kidding, of course. I\'ll only scam you out of 90% of it.'),
            ('Lamp oil, ropes, bombs?', 'They\'re yours, {name}, as long as you have enough GOLD!', '...Ah, I just love saying that. And then when the unsuspecting shoppers see my prices, I get to say,', 'Come back when you\'re a little... mmmm... RICHER!!!', 'And then watch as all the BROKE noobs saunter away in inferiority, as they do not hold the wealth that I, Norshu, possess!'),
            ('Why are we even investigating Rogue?', 'I mean, unless they have bombs, I don\'t understand why we\'re in going balls deep just to chase some ordinary guys carrying a box.', 'Seems kinda over the top to me.', 'Y\'know, I even respect them for whatever shady deals they might be doing. I love seeing people supporting the economy in inhumane ways.'),
            ('You\'re an investigator, right?', 'I always hated when the investigators would come around to my shop at Isle and chastise me for making perfectly balanced prices.', 'What fools they were. Don\'t they know I\'m the greatest shopkeeper on the continent of Bipole?'),
            ('How much gold do I own?', 'Hm.... I don\'t know, probably a couple hundred thousand gold at this point.', 'I don\'t keep track anymore, I\'ve scammed too many innocent souls.', 'I\'m not a good person? What are you saying!? I\'m the best businessman this nation\'s ever had! Do you know how much money I make?!')
        ],
        [   #Mood 3<
            ('Bruh, I made the best deal the other day. Some random kid came up to me and gave me a whole 20 gold for a slash card! Are they braindead, am I right?'),
            ('I\'ve been getting into some weird books recently.', 'You ever read {c.ITALIC}The Hand of the Neville Prophecy{c.RESET}?', 'It\'s about this random kid nmed Neville who saves the world. I heard it\'s available on infinityjka.itch.io!'),
            ('Xuirbo keeps pressing me into investing in these random memecoins I\'ve never heard of.', 'Get a load of this guy! I mean, who would waste their money on random collectibles that have little to no economic value?', 'Doesn\'t sound familiar at all to me, amirite?'),
            ('Why don\'t I just give you all my wares so you can save Isle?', 'Hmmm... good question...', 'I think you know enough about me to know the answer to that... hehe.'),
            ('My least favorite people are those who disvalue the concept of economy.', 'Currency is what gives life meaning, it gives those who give what they deserve.', 'And my work just so happens to be scamming the ignorant into giving me moneey that I deserve, not them.', 'I\'m a hypocrite, you say? Prepostorous, {name}! I\'m taking money that is rightfully mine, as I am the master of deals!')
        ],
        [   #Mood 4<
            ('You know, if everyone was like you, {name}, then I would be a whole lot richer.', 'Too bad most people just can\'t recognize a good deal when they see it.'),
            ('Who would\'ve known that on this journey, where I am restricted to one customer, I would yield so much money!?', 'I\'ve done more scams in the past week than I have done all year!', '..Uhh, I mean, thanks for supporting the business, pal, means a lot!'),
            ('I always talk about stealing money from people, but you know, I have some standards.', 'If a homeless guy approached my shop and asked for something, I would only offer my wares for double the market value instead of fives times it.', 'What can I say, I\'m kind of a generous man.'),
            ('The business has been going well lately.', 'Not like it ever has gone bad, as I, the greatest businessman, can adapt to any customer to make the best deal possible.'),
            ('I\'m considering starting to sell items near their market value for once...', 'Actually, nah. Just thinking about giving someone an actually reasonable offer just makes me want to puke.', 'Exploiting the economy is where it\'s at.')
        ]
    ]


current_shop = norshu

ShopItem('Slice', 5, 'Ah yes, the basic Slice.')

ShopItem('Lesser Healing Potion (Deck)', 30, 'Yes, the potion is cardboard. I don\'t make them, I only sell them.', itemname='Lesser Healing Potion', itemtype='move', condition=('health', 1))

ShopItem('Healing Potion (Deck)', 30, 'Yes, the potion is cardboard. I don\'t make them, I only sell them.', itemname='Healing Potion', itemtype='move', condition=('health', 4))

ShopItem('Rush Attack', 15, '[B].', condition=('power', 3))

ShopItem('Hyper Slash', 20, 'You need to buy Slash? You do have a sword, right?', condition=('power', 4))

ShopItem('Shock', 10, 'Shock? What\'s that gonna do, make the enemy surprised?', condition=('mana', 2))

ShopItem('Fireball', 10, 'Fireball? Seems kinda generic.', condition=('mana', 3))

ShopItem('Lesser Mana Potion (Deck)', 30, 'Yes, the potion is cardboard. I don\'t make them, I only sell them.', itemname='Lesser Mana Potion', itemtype='move', condition=('mana', 1))

ShopItem('Mana Potion (Deck)', 30, 'Yes, the potion is cardboard. I don\'t make them, I only sell them.', itemname='Mana Potion', itemtype='move', condition=('mana', 4))

ShopItem('Stab', 10, 'Uh oh...', condition=('stealth', 2))

ShopItem('Pickpocket', 25, 'UMMMMMMM....... Why might you be buying this?', condition=('stealth', 3))



ShopItem('Shuffle', 10, 'What are you even shuffling, your spells? Why do you shuffle them?', condition=('utility', 2))

ShopItem('Sword of Greed', 100, 'Bruh you really be buying something called \"Sword of Greed\", what does that say about you?', 'You cannot handle the power of the Sword of Greed.', 1, condition=('utility', 10))

ShopItem('Blade of the Stock Market', 250, 'The blade has chosen you as its user.', 'Do not dare touch the Blade of the Stock Market, you plebian trash.', 1, condition=('level', 10))

ShopItem('Wrath of the Ultimate Shareholder', 10000, 'Congratulations.', 'Do not dare approach the Wrath of the Ultimate Shareholder... You are not worthy enough to even be near its presence.', 1, condition=lambda user: user.gold >= 500)

ShopItem('ULT Recovery', 10, 'Hey this actually looks useful.', condition=[('level', 5), ('health', 3)])

ShopItem('ULT Sword', 10, 'You already have a sword, why do you need a card of a sword?', condition=[('level', 5), ('power', 3)])

ShopItem('ULT Magic', 10, 'Wdym \'ULT Magic\', it\'s just another card.', condition=[('level', 5), ('mana', 3)])

ShopItem('ULT Pierce', 10, 'How many ULTs do you even need!?', condition=[('level', 5), ('stealth', 3)])

ShopItem('ULT Blast', 10, 'Explosions.', condition=[('level', 5), ('utility', 3)])

ShopItem('Scan', 15, 'Now you can scan stuff. Scan enemies to learn their powers.', condition=('area', 'port', 4))

ShopItem('Loot', 15, 'Now you can loot stuff. If you defeat enemy using Loot, you will obtain extra rewards.', condition=('area', 'port', 4))

ShopItem('Salt Rant', 15, 'bruh this is not poggers :kappa:', condition=lambda user: user.hp <= 1.0)


#Items
ShopItem('Lesser Booster', 5, 'Lesser Booster? Doesn\'t sound like a boost to me.', quantity=10)

ShopItem('Booster', 10, 'I don\'t even know what this is.', quantity=10)

ShopItem('Greater Booster', 20, 'Whatever this thing is, I don\'t know if I would eat it.', quantity=10)

ShopItem('Power Cell', 30, 'Don\'t ask how I got this. My sources are beyond your mind\'s comprehension.', quantity=5, condition=('area', 'split', 4) )


#Upgrade
ShopItem('EcoMul +20%', 20, 'I don\'t get it, how will this singlehandly save the economy?', upgrade=True, run_upgrade=lambda x: True, quantity=5, condition=lambda user: user.gold >= 40)

ShopItem('EcoMul +30%', 35, 'Don\'t spend money you\'re not afraid to lose.', upgrade=True, run_upgrade=lambda x: True, quantity=5, condition=lambda user: user.gold >= 80)


# +=========== XUIRBO
current_shop = xuirbo

ShopItem('Cigar', 5, 'Hey, don\'t buy all of these, I need to keep some for... scientific reasons.', quantity=15)

ShopItem('Xuirleaf', 10, 'Don\'t get addicted.', quantity=10, condition=('health', 1))

ShopItem('Antidote', 8, 'Plague begone.', quantity=5, condition=('health', 2))

ShopItem('Water', 8, 'Ice salt aye!', quantity=5, condition=('health', 3))

ShopItem('Bandage', 8, 'Trust me, it\'s cheaper than the hospital.', quantity=5, condition=('health', 4))

ShopItem('Dank Leaf', 25, 'This is the good stuff.', quantity=5, condition=('health', 5))
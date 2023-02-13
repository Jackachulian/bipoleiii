
import game as g
import client, util, moves
from recipes import recipe_list as recipes

item_list = []

craft_type_set = 'consumable'

class Item:
    item_type = 'item'

    def __init__(self, name, desc="An item", consumable=True, craft_type=None, usable=(0,0), use_turn=True, validate=lambda user: True, invalid_text=None,
    damage=0, tags=None, hp=0, sp=0, le=0, atk_buff=0, def_buff=0, razor=False, armor=False, effect=lambda user: None ):
        self.name = name
        self.desc = desc

        self.quantity = 1   #In inventory, this is how much of the item is in the stack

        if type(usable) == tuple:
            self.usable = usable    # Two-part tuple: ( usable in battle, usable in post-battle )
        else:
            self.usable = (usable, usable)    # Integer, means 1 or 0 for both battle and post-battle

        if craft_type:
            self.craft_type = craft_type
        else:
            global craft_type_set
            self.craft_type = craft_type_set

        if self.craft_type in ['consumable', 'potion']:
            self.consumable = True
        else:
            self.consumable = consumable    # Whether or not the item is consumed on use

        self.use_turn = use_turn    # If the item uses up a turn during battle or not
        self.validate = validate    # Runs to see if the item can be used at the given time
        self.invalid_text = invalid_text

        self.damage = damage
        self.tags = tags

        self.hp = hp
        self.sp = sp
        self.le = le    #Stat boosts
        self.atk_buff = atk_buff
        self.def_buff = def_buff

        self.razor = True if razor else ('Razor' in self.name)  #Idk why but these lines of code are satisfying
        self.armor = True if armor else ('Armor' in self.name)

        self.effect = effect    # Runs when using the item

        global item_list
        item_list.append(self)

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
        client.line(f'  {statif("Consumable")}')
        client.line(f'  {statif("Damage")}{statif("Tags")}{statif("HP")}{statif("SP")}{statif("LE")}{statif("ATK_Buff")}{statif("DEF_Buff")}')
        client.divider()
        client.set_line_delay(1)

    def validate_all(self, user):
        return self.validate(user) and self.is_usable()
 

    def check_usable(self, user):
        if self.usable == (0,0):
            return client.line(f'{self} cannot be used')

        if not self.validate(user):
            if self.invalid_text:
                return client.line(self.invalid_text.format(user=user))

        if g.game.in_battle:
            if not self.usable[0]:
                return client.line(f'{self} cannot be used during battle!')
        else:
            if not self.usable[1]:
                return client.line(f'{self} can only be used during battle.')

        return True

    def is_usable(self):
        if g.game.in_battle:
            return self.usable[0]
        else:
            return self.usable[1]

    def use(self, user):
        if not self.check_usable(user):
            return

        client.line(f'{user} used {self}!')

        if self.consumable:
            self.quantity -= 1

        if self.damage and game.in_battle:
            user.target_and_deal_damage(self.damage)

        if self.hp:
            user.heal(self.hp * user.pharmacy )
        if self.sp > 0:
            user.gain_sp(self.sp)
        if self.le > 0:
            user.gain_le(self.le)
        if self.atk_buff > 0:
            user.stat_change('atk', 0.5, buff=True)
        if self.def_buff > 0:
            user.stat_change('defense', 0.5, buff=True)

        self.effect(user)

        if self.quantity < 1:
            user.inventory_items.remove(self)   #Should delete this object
            return 'Used All'

        return 'Used'

def item_from_string(string, warn_not_found=False):
    if not type(string) == str:
        return string
    filter_list = list(filter(lambda item: item.name.lower().replace(' ','') == string.lower().replace(' ',''), item_list))
    if len(filter_list) > 0:
        return filter_list[0]
    else:
        if warn_not_found:
            raise Exception(f'No item found with name {string}')
        else:
            return None


# Crafting

def add_recipes():
    #  [ ( [(Ingredient, #), (Ingredient, #)], (Product, #)  ) ]
    game = g.game

    for recipe in recipes:
        if not recipe in game.recipes and check_recipe(recipe):
            game.recipes.append(recipe)
            product = recipe[1]
            if type(product) == str:
                product_name = product
            else:   #Tuple
                product_name = product[0]
            client.line(f'{game.player} learned how to craft {product_name}!')


def check_recipe(recipe, one=False):   #Returns true if the user contains all required items, or at least one if one=True
    player = g.game.player

    for material in recipe[0]:
        if not check_material(material, one):
            return False

    return True

def check_material(material, one=False):
    player = g.game.player

    if type(material) == str:
        mat = material
    else:
        mat = material[0]

    if not mat in [i.name for i in player.inventory_items]:
        return False

    item = util.fsearch(player.inventory_items, lambda i: i.name == material[0])
    
    if not one and not material[1] <= item.quantity:
        return False

    return True

def recipe_list(ingredients=False, productonly=False, grey_out=True):
    return [recipe_format(r, productonly, grey_out) for r in g.game.recipes]
    
def recipe_format(recipe, productonly=False, grey_out=True):

    if productonly:
        return recipe[1][0]

    ing_list = []

    for ingredient in recipe[0]:
        if type(ingredient) == str:
            mat = ingredient
            amt = 1
        else:
            mat = ingredient[0]
            amt = ingredient[1]

        ing_str = f'{mat}({amt})'

        if grey_out and not check_material(ingredient):
            ing_str = '{c.GREY}' + ing_str + '{c.RESET}'

        ing_list.append( ing_str )

    product = recipe[1]
    if type(product) == str:
        mat = product
        amt = 1
    else: #tuple
        mat = product[0]
        amt = product[1]

    if amt > 1:
        product_str = f'{mat} ({amt})'
    else:
        product_str = mat

    if grey_out and not check_recipe(recipe):
        product_str = '{c.GREY}' + product_str

    string = ' + '.join(ing_list) + ' >> ' + product_str

    return string


def craft(recipe):
    product_name = recipe[1] if type(recipe[1]) == str else recipe[1][0]

    if not check_recipe(recipe):
        return client.line(f'You are missing the required materials to craft {product_name}.')

    player = g.game.player

    for ingredient in recipe[0]:
        if type(ingredient) == str:
            mat = ingredient
            amt = 1
        else:
            mat = ingredient[0]
            amt = ingredient[1]

        matching_item = util.fsearch(player.inventory_items, lambda i: i.name == mat)

        matching_item.quantity -= amt

    product = recipe[1]
    if type(product) == str:
        mat = product
        amt = 1
    else: #tuple
        mat = product[0]
        amt = product[1]

    product_item = item_from_product(mat)

    player.obtain(product_item, amt)

    #Adjust amount for skill classes
    pict = product_item.craft_type
    if player.blacksmith and pict == 'tool' or player.alchemist and pict == 'potion' or player.craftsmanship and pict == 'consumable':
        rand_refund(recipe)


def rand_refund(recipe):
    for ingredient in recipe[0]:
        if type(ingredient) == str:
            mat = ingredient
            amt = 1
        else:
            mat = ingredient[0]
            amt = ingredient[1]

        refund_amt = 0
        for n in range(amt):
            if random.random() < 0.3:
                refund_amt += 1

        if refund_amt > 0:
            client.line(f'Saved {refund_amt} {mat}!')
            matching_item = util.fsearch(player.inventory_items, lambda i: i.name == mat)
            player.obtain(matching_item, amt, announce=False)


def item_from_product(mat):
    product_item = item_from_string(mat)

    if not product_item:
        product_item = moves.move_from_string(mat)

    return product_item


# Materials
craft_type_set = 'material'
Item('Life Energy', 'The pure essence of life. Illegal in most countries.')

Item('Slime', 'Some slimy slime. Dropped by most... slimes.')

Item('Slime Eye', 'The large, slimy eye of a... slime.')

Item('Wood', 'Some scraps of wood. A versatile crafting material.')

Item('Stone', 'Some stones. Heavy, and could be used to add weight to crafting items.')

Item('Copper', 'A weak scrap of metal.')

Item('Iron', 'A sturdy, heavy piece of metal.')

Item('Steel', 'A refined sheet of metal that can be used to create strong tools.')  #2 iron, 1 copper, also dropped commonly by Mechanicals

Item('Crystal', 'A dense mineral dropped by strong enemies. Can be crafted into very powerful gear.')


#Enemy Drops
craft_type_set = 'other'
Item('Rogue Badge', '+0.25 ATK for the rest of the battle', True, (1,1), atk_buff=0.25 )   #Dropped by ROgue Brutes and Mages, can be used or saved for powerful crafting items


# Consumables
craft_type_set = 'consumable'
Item('Lesser Booster', 'Heal 2 HP, gain 2 SP and +0.5 ATK for 5 turns', True, (1,1), hp=2, sp=2, effect=lambda user: user.afflict('Lesser Boost', 1, 5) )   #Recipe: 2 copper, 1 life essence

Item('Booster', 'Heal 4 HP, gain 4 SP and +1 ATK for 5 turns', True, (1,1), hp=4, sp=4, effect=lambda user: user.afflict('Boost', 1, 5) )   #Recipe: 2 iron, 2 life essence

Item('Greater Booster', 'Heal 6 HP, gain 6 SP and +1.5 ATK for 5 turns', True, (1,1), hp=6, sp=6, effect=lambda user: user.afflict('Greater Boost', 1, 5) )   #Recipe: 2 steel, 3 life essence

Item('Power Cell', '+6 SP', True, (1,1), sp=6 )   #Endgame crafting material and can be used to gain some SP

Item('Life Sigil', 'Recover 2 LE', True, (1,0), le=2 )   #Recipe: 3 life energy

Item('Mana Sigil', 'Recover 4 SP', True, (1,0), sp=4 )   #Recipe: 3 life energy

# Potions
craft_type_set = 'potion'
Item('Slime Restore', 'Recover 6 MP and 4 MP.', True, (1,1), hp=5, sp=3 )   #Recipe: 5 slime, 1 slime eye


#Crafted Tools
craft_type_set = 'tool'
#Copper set     #Unlocked after rogue scout battle at port
Item('Copper Throwing Knife', 'Deal 2.5 damage', True, (1,0), damage=2.5, tags='pierce' )   #1 copper, 1 wood

Item('Copper Razor', '+0.15 ATK', False, (1,0), atk_buff=0.15 )   #3 copper, 2 stone

Item('Copper Armor', '+0.15 DEF', False, (1,0), def_buff=0.15 )   #3 copper, 2 wood


#Iron set   #unlocked middle of forest/tundra/volcano
Item('Iron Throwing Knife', 'Deal 3 damage', True, (1,0), damage=3, tags='pierce' )   #1 iron, 2 wood, 1 stone

Item('Iron Razor', '+0.25 ATK', False, (1,0), atk_buff=0.25 )   #3 iron, 1 copper, 3 stone

Item('Iron Armor', '+0.25 DEF', False, (1,0), def_buff=0.25 )   #3 iron, 1 copper, 6 wood


#Steel
Item('Steel Throwing Knife', 'Deal 3.5 damage', True, (1,0), damage=3.5, tags='pierce' )   #1 steel, 1 wood, 3 stone

Item('Steel Razor', '+0.35 ATK', False, (1,0), atk_buff=0.35 )   #3 steel, 2 iron, 4 stone

Item('Steel Armor', '+0.35 DEF', False, (1,0), def_buff=0.35 )   #3 steel, 2 iron, 6 wood


#Crystal
Item('Crystal Throwing Knife', 'Deal 4 damage', True, (1,0), damage=4, tags='pierce' )   #1 Crystal, 2 steel

Item('Crystal Razor', '+0.5 ATK', False, (1,0), atk_buff=0.5 )   #3 Crystal, 1 steel, 1 iron, 1 copper, 1 stone

Item('Crystal Armor', '+0.5 DEF', False, (1,0), def_buff=0.5 )   #3 Crystal, 4 steel


#Shop-Exclusive
craft_type_set = 'consumable'
# --- Xuirbo
Item('Cigar', 'Take 2 damage and gain 2 SP and 2 LE.', True, (1,1), hp=-2, sp=2, le=2, validate=lambda user: user.hp > 2, invalid_text='You will literally die if you use this, bruh.' )   #Xuirbo shop

Item('Xuirleaf', 'Recover 5 HP.', True, (1,1), hp=5 )   #Recipe: 3 slime, 1 slime eye

Item('Antidote', 'Removes Poison', True, (1,0), effect=lambda user: user.clear_afflict('Poison') )

Item('Water', 'Removes Burn', True, (1,0), effect=lambda user: user.clear_afflict('Burn') )

Item('Bandage', 'Heals 2 HP, removes Bleed', True, (1,0), hp=2, effect=lambda user: user.clear_afflict('Bleed') )

Item('Dank Leaf', 'Removes all status effects', True, (1,1), effect=lambda user: user.clear_afflict('all') )   #Recipe: 3 slime, 1 slime eye
#All Bipole III areas.

#FORMAT
#List - battle
#'postbattle' - Post-Battle
#'area' - Go to the specified area, or if choice, choose between all following areas
#'cts' - cutscene, play the cutscene with the given in name in /cutscenes

class Area:
    def __init__(self, name, desc, forage, level_map, forage_chance=0.5):
        self.name = name
        self.desc = desc    #Shows during foraging
        self.level_map = level_map

        self.forage = forage #List of forage tuples ( (item, amt) or (item, amt, item_type) )
        self.forage_chance = forage_chance  #Chance per item to obtain it

    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.level_map)


sets = {
    'Copper Tool': ['Copper Throwing Knife', 'Copper Razor', 'Copper Armor', 'Copper Sword', 'Copper Mace', 'Copper Bow'],
    'Iron Tool': ['Iron Throwing Knife', 'Iron Razor', 'Iron Armor', 'Iron Sword', 'Iron Mace', 'Iron Bow'],
    'Steel Tool': ['Steel Throwing Knife', 'Steel Razor', 'Steel Armor', 'Steel Sword', 'Steel Mace', 'Steel Bow'],
    'Crystal Tool': ['Crystal Throwing Knife', 'Crystal Razor', 'Crystal Armor', 'Crystal Sword', 'Crystal Mace', 'Crystal Bow'],
}

port = Area('Port', 'A route by the sea.',

forage = [ 
    ('Wood', 500), ('Stone', 250), 
    ('Slime', 50), ('Cloth', 25), 
    ('Copper', 75), ('Iron', 25), ('Steel', 10),
    ('Lesser Healing Potion', 20), ('Lesser Mana Potion', 20), ('Lesser Attack Potion', 20), ('Lesser Life Potion', 20),
    ('Healing Potion', 10), ('Mana Potion', 10), ('Attack Potion', 10), ('Life Potion', 10),
    ('Copper Tool', 10, 'set'),    #Adds one of each item to the collection with the given amount
    ('Iron Tool', 5, 'set'),
    ('Isle Slash', 1, 'card')
    ],

level_map = [
    'cts intro', ['Red Slime'], 'postbattle',
    ['Red Slime', 'Red Slime'], 'cts xuirbo', 'postbattle',
    ['Red Slime', 'Rogue Scout'], 'postbattle',
    ['Rogue Brute'], 'postbattle', 'area choice forest tundra volcanic'
])

forest = [
    ['Red Slime', 'Green Slime'], 'postbattle',
    ['Red Slime', 'Green Slime', 'Blue Slime'], 'postbattle',
    ['Plant Spirit', 'Plant Spirit'], 'postbattle',
    ['Rogue Scout', 'Rogue Brute', 'Rogue Mage'], 'postbattle',
    ['Red Slime', 'Red Slime', 'Red Slime', 'Green Slime', 'Blue Slime'], 'postbattle',
    ['Plant Spirit', 'Tsoref', 'Plant Spirit'], 'postbattle', 'area city'
]

tundra = [
    ['Red Slime', 'Blue Slime'], 'postbattle',
    ['Wolf', 'Wolf'], 'postbattle',
    ['Rogue Scout', 'Rogue Scout', 'Rogue Scout'], 'postbattle',
    ['Blue Slime', 'Blue Slime', 'Ice Spirit'], 'postbattle',
    ['Rogue Mage', 'Rogue Mage', 'Rogue Brute', 'Rogue Mage'], 'postbattle',
    ['Wolf', 'Wolf', 'Wolf'], ['Wolf', 'Wolf', 'Wolf'], 'postbattle',
    ['Ice Spirit', 'Ardnut', 'Ice Spirit'], 'postbattle', 'area city'
]

volcanic = [
    ['Black Slime'], 'postbattle',
    ['Coal Entity', 'Black Slime', 'Coal Entity'], 'postbattle',
    ['Fire Spirit', 'Black Slime', 'Fire Spirit'], 'postbattle',
    ['Coal Entity', 'Coal Entity', 'Coal Entity', 'Black Slime', 'Black Slime'], 'postbattle',
    ['Coal Entity', 'Fire Spirit', 'Cinaclov', 'Fire Spirit', 'Coal Entity'], 'postbattle', 'area city'
]
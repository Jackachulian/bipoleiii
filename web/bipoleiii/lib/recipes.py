

recipe_list = [     #Tuples of two, containing a list of item/amount tuples at the start and end
    #crafting crafting
    ( [('Iron', 2), ('Copper', 1)], 'Steel' ),

    # === Consumables
    #Boosters
    ( [('Copper', 2), ('Life Energy', 1)], 'Lesser Booster' ),
    ( [('Iron', 2), ('Life Energy', 2)], 'Booster' ),
    ( [('Steel', 2), ('Life Energy', 3)], 'Greater Booster' ),

    #Other
    ( [('Slime', 5), ('Slime Eye', 1)], 'Slime Restore' ),
    ( [('Life Energy', 3)], 'Life Sigil' ),
    ( [('Life Energy', 3)], 'Mana Sigil' ),

    # === Tools
    #Throwing Knives
    ( [('Copper', 1), ('Wood', 1)], 'Copper Throwing Knife' ),
    ( [('Iron', 1), ('Wood', 2), ('Stone', 1)], 'Iron Throwing Knife' ),
    ( [('Steel', 1), ('Wood', 3), ('Stone', 2)], 'Steel Throwing Knife' ),
    ( [('Crystal', 1), ('Steel', 2)], 'Crystal Throwing Knife' ),

    #Razors
    ( [('Copper', 3), ('Stone', 1)], 'Copper Razor' ),
    ( [('Iron', 3), ('Copper', 1), ('Stone', 3)], 'Iron Razor' ),
    ( [('Steel', 3), ('Iron', 2), ('Stone', 4)], 'Steel Razor' ),
    ( [('Crystal', 3), 'Steel', 'Iron', 'Copper', 'Stone'], 'Crystal Razor' ),

    #Armor
    ( [('Copper', 3), ('Wood', 2)], 'Copper Armor' ),
    ( [('Iron', 3), ('Copper', 1), ('Wood', 6)], 'Iron Armor' ),
    ( [('Steel', 3), ('Iron', 2), ('Wood', 6)], 'Steel Armor' ),
    ( [('Crystal', 3), ('Steel', 4)], 'Crystal Armor' ),

    #Swords
    ( [('Wood', 3), ('Stone', 1)], 'Wooden Sword' ),
    ( [('Copper', 3), ('Wood', 3)], 'Copper Sword' ),
    ( [('Iron', 3), ('Wood', 4), ('Stone', 2)], 'Iron Sword' ),
    ( [('Steel', 3), ('Wood', 6), ('Stone', 3)], 'Steel Sword' ),
    ( [('Crystal', 3), ('Steel', 6)], 'Crystal Sword' ),

    #Maces
    ( [('Stone', 3), ('Wood', 1)], 'Stone Mace' ),
    ( [('Copper', 3), ('Wood', 2), ('Stone', 1)], 'Copper Mace' ),
    ( [('Iron', 3), ('Copper', 1), ('Wood', 1), ('stone', 2)], 'Iron Mace' ),
    ( [('Steel', 3), ('Iron', 1), ('Wood', 2), ('stone', 4)], 'Steel Mace' ),
    ( [('Crystal', 3), ('Steel', 3), ('Wood', 2), ('stone', 8)], 'Crystal Mace' ),

    #Bows
    ( [('Wood', 2), ('Cloth', 1)], 'Wooden Bow' ),
    ( [('Copper', 3), ('Wood', 2), ('Cloth', 1)], 'Copper Bow' ),
    ( [('Iron', 3), ('Wood', 3), ('Cloth', 2)], 'Iron Bow' ),
    ( [('Steel', 3), ('Copper', 1), ('Wood', 4), ('Cloth', 3)], 'Steel Bow' ),
    ( [('Crystal', 3), ('Steel', 3), ('Wood', 6), ('Stone', 2), ('Cloth', 4)], 'Crystal Bow' )
]
"""Code for implementing Player class and its methods"""
from __future__ import annotations

from cave import Cave
from material import Material
from trader import Trader, RandomTrader, RangeTrader, HardTrader
from food import Food
from random_gen import RandomGen
from hash_table import LinearProbeTable
from avl import AVLTree
from linked_stack import LinkedStack

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():
    """ Player class

    attributes:
        name (string) - name of the player
        self.balance (int) - amount of emerals Player has
        self.hunger_bars (int) - the number of hunger bars Player has, used to mine materials
        self.traders (list) - the different available traders
        self.food (list) - the different options of food available to buy
        self.materials (list) - materials available to mine
        self.caves (list) - caves available to mine materials from
    
    complexity:
        unless otherwise stated methods have a complexity of O(1)
    """
    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """Initialisation of Player class"""
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.hunger_bars = 0
        self.traders = []
        self.food = []
        self.materials = []
        self.caves = []
        
    def set_traders(self, traders_list: list[Trader]) -> None:
        ''' Set traders available '''
        self.traders = traders_list

    def set_foods(self, foods_list: list[Food]) -> None:
        ''' Set food options available '''
        self.food = foods_list

    @classmethod
    def random_player(cls) -> Player:
        ''' Generates a random player from list of player names '''
        return Player(RandomGen.random_choice(PLAYER_NAMES))

    def set_materials(self, materials_list: list[Material]) -> None:
        ''' Set materials available to mine '''
        self.materials = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        ''' Set caves available to mine materials from '''
        self.caves = caves_list

    def __str__(self) -> str:
        '''String representation of Player Class'''
        return f"<{self.name}: {self.balance}>"

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """ Generate tuple containing: Food player will buy, emerald balance after player makes move,
                    list of all caves plundered on journey- paired with quanity of each material mined

        Complexity:
            best/worst case: O(M + T + F * C * logC) 
                where  F = #Foods, T = #Traders, C=#Caves, M=#Materials

        Motivation:
            Food is iterated through and from that the best cave run and profit made is determined
            Materials and the best sell price are added to a hash table to reduce the complexity
                of finding the best deal for each material
            We then used an AVLTree with the keys as $ per hunger bar, and value as the 
                associated cave - this cave based on the best possible Trader sell price for the 
                cave material and the available hunger bars the food provides - this reduces the 
                complexity of trying to find the best profit, by sorting them in a self-balancing AVL tree.
                Using a stack also reduces complexity as all its methods are O(1)  
        """
        # check that there is food, traders, materials and caves accessible to the player
        assert(len(self.traders) > 0), 'there are no available traders'    
        assert(len(self.food) > 0), "there is no food to buy"
        assert(len(self.materials) > 0), "there are no materials to mine"
        assert(len(self.caves) > 0), "there are no caves around"

        # Setup material -> best selling price hash table
        # Allows for O(1) access to best Trader sell price for each material
        # hash table containing: material name : max selling price
        trader_materials = LinearProbeTable(len(self.materials))
        
        # Put all materials in hash table by name
        for mat in self.materials:      # O(M)
            trader_materials[mat.name] = 0      # O(1)
        # Assign Trader with max selling price to materials in trader_materials
        for trader in self.traders:     # O(T)
            # Get current material
            current_material_name = trader.current_deal()[0].name

            # assign the key of material to the max selling price for that material
            trader_materials[current_material_name] = max(trader.current_deal()[1], trader_materials[current_material_name])    # O(1)

        best_food = None
        best_balance = self.balance
        best_cave_day = []


        # iterate through each food to find which makes the most profit
        for food in self.food:          # O(F)

            # stores the each cave with the profit the player can make from it
            # keys will have $ per hunger bar consumed
            caves_money_hunger_ratio = AVLTree()

            # add each cave to an AVL tree with the $ per hunger as the key and a stack of caves as the value
            for cave in self.caves:        # O(C)
                mat = cave.material
                selling_price = trader_materials[mat.name]
                # only use caves with materials that traders can buy
                if selling_price is not None:
                    sell_hunger_ratio = selling_price / mat.mining_rate     # $ per hunger bar

                    # add the cave and linked stack
                    if sell_hunger_ratio not in caves_money_hunger_ratio:
                        caves_money_hunger_ratio[sell_hunger_ratio] = LinkedStack()

                    caves_money_hunger_ratio[sell_hunger_ratio].push(cave)      # O(logC)

            # initialise collector list
            caves_mined = []
            # initialise hunger bars
            hunger_bars = food.hunger_bars
            # initialise emeralds
            emeralds = self.balance - food.price

            # iterate through each cave or until the player has no hunger left
            # for each cave the player mines as much as they can
            while hunger_bars > 0 and len(caves_money_hunger_ratio) > 0:        # O(C) worst case
                # find the cave with the best sell to hunger bar ratio
                ratio, best_cave_stack = caves_money_hunger_ratio.get_max()         # O(logC)
                best_cave = best_cave_stack.pop()       # O(1)
                mat = best_cave.material
                
                # if the best cave was the last item on the stack remove the item from the AVL tree
                if len(best_cave_stack) == 0:
                    del caves_money_hunger_ratio[ratio]

                # now mine
                # determine how much we can mine and the hunger cost
                quantity = best_cave.get_quantity()
                hunger_needed = quantity * mat.mining_rate
                
                # if hunger bars needed is greater than hunger bars we have
                if hunger_needed > hunger_bars:
                    # mine as much as possible with our hunger bars
                    quantity = hunger_bars / mat.mining_rate
                    # update hunger needed to be as much as remaining hunger bars
                    hunger_needed = hunger_bars  

                # Otherwise, we mine all of it
                caves_mined.append((best_cave, quantity))
                hunger_bars -= hunger_needed

                # calculate emeralds earned
                emeralds += quantity * trader_materials[mat.name]

            # now compare with other iterations to determine which food and cave run is the best
            if emeralds > self.balance and (best_balance is None or emeralds > best_balance):
                best_balance = emeralds
                best_cave_day = caves_mined
                best_food = food

        # return the tuple
        return (best_food, best_balance, best_cave_day)


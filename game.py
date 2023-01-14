"""Contains code implementing the Game, SoloGame, and MultiplayerGame class"""
from __future__ import annotations

__author__ = "Scaffold by FIT1008 teaching team, Code by Felicity, Virani, Dylan, Edward"

from player import Player
from trader import Trader, RandomTrader, RangeTrader, HardTrader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from hash_table import LinearProbeTable
from avl import AVLTree
from constants import EPSILON
from linked_stack import LinkedStack


class Game:
    """ The game base class
    
    Attributes:
        caves (list[Cave]) - the list of caves that the game has
        materials (list[Materials]) - the list of materials the game has
        traders (list[Trader]) - the list of traders the game has
        
    Complexity:
        Unless otherwise stated, the complexity for methods is O(1)
    """
    
    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """Initialisation of Game attributes"""
        self.caves = []
        self.materials = []
        self.traders = []
        
    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        """Assign given data to instance variables"""
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        """Sets self.materials attribute to list of all materials"""
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """Sets self.caves attribute to list of all caves"""
        self.caves = caves

    def set_traders(self, traders: list[Trader]) -> None:
        """Sets self.traders attribute to list of all traders"""
        self.traders = traders

    def get_materials(self) -> list[Material]:
        """Returns entire list of materials"""
        return self.materials

    def get_caves(self) -> list[Cave]:
        """Returns entire list of materials"""
        return self.caves

    def get_traders(self) -> list[Trader]:
        """Returns entire list of traders"""
        return self.traders

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)

        Complexity:
            O((A + S) * A * CompN) 
                    where A is the amount of materials needed,
                    S is the number of times a material with the same name or mining rate is generated,
                    and CompN is the cost of comparison between material names
        """
        self.materials = []
        # loop until there is the correct amount of materials
        while len(self.materials) < amount:
            # generate a random material
            new_mat = Material.random_material()
            isin = False
            # check that the material has a different name and mining rate to all other materials we have
            for mat in self.materials:
                if mat.name == new_mat.name or mat.mining_rate == new_mat.mining_rate:      # O(compN)
                    isin = True
                    break
            # if its different add it to the list of materials
            if not isin:      
                self.materials.append(new_mat)
                    

    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)

        Complexity:
            O((A + S) * A * CompN) where A is the amount of caves needed and
                    S is the number of times a cave with the same name is generated
                    and CompN is the cost of comparison between cave names
        """
        self.caves = []
        # loop until there is the correct amount of caves
        while len(self.caves) < amount:
            # generate a random material
            new_cave = Cave.random_cave(self.materials)
            isin = False
            # check that the material has a different cave name to all the other caves
            for cave in self.caves:
                if cave.name == new_cave.name:      # O(compN)
                    isin = True
                    break
            # if its unique add it to the list of caves
            if not isin:      
                self.caves.append(new_cave)


    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
        
        Complexity:
            O((A + S) * A * compN) where A is the amount of traders needed and
                    S is the number of times a trader with the same name is generated
                    and CompN is the cost of comparison between trader names
        """
        self.traders = []
        # loop until there is the correct amount of traders
        while len(self.traders) < amount:   # O(A + S)
            # generate a random class of trader between the 3 classes
            trader_type = RandomGen.randint(1,3)
            isin = False

            # generate a RandomTrader
            if trader_type == 1:
                new_trader = RandomTrader.random_trader()
            # generate a RangeTrader
            elif trader_type == 2:
                new_trader = RangeTrader.random_trader()
            # generate a HardTrader
            else:
                new_trader = HardTrader.random_trader()

            # check that the trader has a different name
            for trader in self.traders:         # O(A)
                if trader.name == new_trader.name:          # O(compN)
                    isin = True
                    break
            
            # if it has a different name add materials and add to trader list
            if not isin:
                new_trader.set_all_materials(self.materials)
                self.traders.append(new_trader)
            
    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)


class SoloGame(Game):
    """
    SoloGame class(inherited from Game)

    Attributes:
        caves (list[Cave]) - the list of caves that the game has
        materials (list[Materials]) - the list of materials the game has
        traders (list[Trader]) - the list of traders the game has
    
    """

    def __init__(self):
        """Initialisation of SoloGame class"""
        Game.__init__(self)

    # Given method
    def initialise_game(self) -> None:
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    # Given method
    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    # Given method
    def simulate_day(self):
        """ simulates a day of mining """
        # 1. Traders make deals
        for trader in self.traders:
            trader.generate_deal()
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)

        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        print(food, balance, caves)
        
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        '''
        when called with the result of select_food_and_caves is passed in:
        1. Checks that the result makes sense - That:
            a. Quantities are in line with what the player provided
            b. The food is purchasable
            c. The remaining balance is correct
            d. Any other sanity checks you can think of
        2. Updates the quantities within each cave accordingly.

        Complexity:
            O(C * T) where C is the number of caves mined during that day
                    and T is the number of traders
        '''
        # checks that the food is purchasable
        assert(food.price < self.player.balance), "Player cannot afford the food"

        possible_balance = self.player.balance
        possible_balance -= food.price

        # check cave quantities are correct
        for cave, quantity in caves:
            assert(quantity <= cave.quantity), "cave does not have enough of that material"
            cave.remove_quantity(quantity)

            # find trader selling the material for the most emeralds
            max_sell_price = 0
            for trader in self.traders:
                if cave.material == trader.current_deal()[0] and trader.current_deal()[1] > max_sell_price:
                    max_sell_price = trader.current_deal()[1]

            possible_balance += quantity * max_sell_price
            
        # check remaining balance is possible
        assert(balance <= possible_balance)
        # set player balance to the given balance
        self.player.balance = balance


class MultiplayerGame(Game):
    """ Multiplayer Game
    
    Only 1 food is offered per day - everyone can either buy this or not go mining at all.
    Each player can only visit one cave per day
    Players go mining in order, so player #1 does all of their mining, followed by player
    #2, then player #3, and so on.
    
    Attributes:
        caves (list[Cave]) - the list of caves that the game has
        materials (list[Materials]) - the list of materials the game has
        traders (list[Trader]) - the list of traders the game has
    
    """

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []

    # Given method
    def initialise_game(self) -> None:
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """Generate <amount> random players. Don't need anything unique, but you can do so if you'd like.
        
        Complexity:
            O((A + S) * A) where A is the amount of players needed and
                    S is the number of times a player with the same name is generated
        """
        self.players = []
        while len(self.caves) < amount:     # O(A + S)
            # generate a random player
            new_player = Player.random_player()
            isin = False
            # check that the player has a different  name to all the other players
            for player in self.players:     # O(A)
                if player.name == new_player.name:
                    isin = True
                    break
            # if its unique add it to the list of caves
            if not isin:      
                self.players.append(new_player)

    # Given method
    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    # Given method
    def simulate_day(self):
        # 1. Traders make deals
        for trader in self.traders:
            trader.generate_deal()
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")

        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)

        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
        Returns a tuple containing:
        - list of what foods the players buy (or None if no food is bought), 
        - list of what emeralds the players have at the end of the day,
        - list of what caves each player visits, paired with how much of the material they mined.

        Complexity:
            O(M + T + C * log C + P * log C)
                Given that M=#Materials, T=#Traders, C=#Caves, P=#Players

        Motivation:
            Materials and the best sell price are added to a hash table to reduce the complexity
                of finding the best deal for each material
            We then used an AVLTree with the keys as max emerald earnings, and value as the 
                associated cave - this cave based on the best possible Trader sell price for the 
                cave material and the available hunger bars the food provides - this reduces the 
                complexity of trying to find the best profit, by sorting them in a self-balancing AVL tree.
            Then we loop through the players and if the highest emerald earning cave has a earning 
                higher then the price of buying the food, they mine in that cave and get those earnings   
        """

        # Setup material -> best selling price hash table
        # Allows for O(1) access to best Trader sell price for each material
        # hash table containing: material name : max selling price
        trader_materials = LinearProbeTable(len(self.materials))
    
        # Put all materials in hash table
        for mat in self.materials:      # O(M)
            trader_materials[mat.name] = 0
        # Assign Trader with max selling price to materials in trader_materials
        for trader in self.traders:     # O(T)
            # Get current material
            current_material_name = trader.current_deal()[0].name

            # assign the key of material to the max selling price for that material
            trader_materials[current_material_name] = max(trader.current_deal()[1], trader_materials[current_material_name])


        # binary tree with caves as values and keys as max emerald calculation:
        # max emerald = min(mat quantity, hunger bars of selling food / mining rate)  * selling price of best trader(for one item)
        max_cave_emeralds = AVLTree()

        for cave in self.caves:         # O(C)
            best_selling_price = trader_materials[cave.material.name]
            # only add to the AVL tree if the selling price is above 0 (aka there is a trader buying)
            if best_selling_price > 0:
                # eg cave has: 10 Prismarine Crystal, mining rate 11.48 | with 100 hunger bars from food can mine 100 / 11.48 = 8.71
                # max quantity possible to be mined 
                max_quantity_mined = min(cave.get_quantity(), food.hunger_bars / cave.material.mining_rate)
                # max amount of emeralds that can be earned from mining this cave
                max_emeralds = max_quantity_mined * best_selling_price

                # add each cave to an AVL tree with the max emeralds at the key, and the cave and how much has already been mined as the value
                if max_emeralds not in max_cave_emeralds:
                    max_cave_emeralds[max_emeralds] = LinkedStack()        # worst O(D) where D is the depth of the tree (logC)
                # there is already an item there with the same key
                max_cave_emeralds[max_emeralds].push((cave, 0)) # (cave instance, quantitity already mined) # O(logC) (stack all O(1))
                              
        # initialise collector lists
        food_consumed = []
        end_day_balance = []
        caves_visited = []

        # iterate through each player and determine what the best cave to mine is
        for player in self.players:         # O(P)
            # initialise variables
            player_food = None
            player_balance = player.balance
            cave_visited = None

            # check if they they even afford the food
            if player.balance >= food.price:
                # get the best earning and the corresponding cave and amount
                max_earnings, max_caves = max_cave_emeralds.get_max()        # O(D) or O(logC)
                # get the cave instance and the quantity already mined
                max_cave, quantity_already_mined = max_caves.pop()            # O(1)
                # get the selling price of the material the cave has
                selling_price = trader_materials[max_cave.material.name]     # O(1)

                # if they make a profit they buy the food and mine the cave
                if max_earnings > food.price:
                    player_food = food
                    # set player's final balance
                    player_balance -= food.price
                    player_balance += max_earnings

                    # find the quantity they mined and add both to the running list
                    quantity_mined = max_earnings / selling_price
                    cave_visited = (max_cave, quantity_mined)

                    # delete current tree node if there are no more caves with that earnings
                    if len(max_caves) == 0:
                        del max_cave_emeralds[max_earnings]
                        
                    # add new key and cave with possible profit of left over materials
                    left_over = max_cave.quantity - quantity_already_mined - quantity_mined     

                    # if you havent mined everything add the rest back onto the tree
                    if not ((abs(left_over) < EPSILON) or left_over <= 0):
                        # recalculate the profit
                        left_over_profit = min(left_over, food.hunger_bars / cave.material.mining_rate) * selling_price
                        
                        if left_over_profit not in max_cave_emeralds:
                            max_cave_emeralds[left_over_profit] = LinkedStack()        # worst O(D) where D is the depth of the tree (logC)
                        max_cave_emeralds[left_over_profit].push((max_cave, quantity_mined + quantity_already_mined))
                else:
                    # if its not worth it, push it back onto the stack
                    max_caves.push((max_cave, quantity_already_mined))
                    
            # add players choices to appropriate lists
            food_consumed.append(player_food)
            end_day_balance.append(player_balance)
            caves_visited.append(cave_visited)
        
        return (food_consumed, end_day_balance, caves_visited)
        

    def verify_output_and_update_quantities(self, foods: Food | None, balances: float, caves: list[tuple[Cave, float]|None]) -> None:
        """
        Similar to the verify_output_update_quantities in the solo game
        Complexity:  O(P * T * compN) where P = #Players and T = #Traders
                and CompN is the cost of comparison between material names
        """
        # loop through each player and check everything
        for i in range(len(self.players)):      # O(P)
            player = self.players[i]
            food = foods[i]

            possible_balance = player.balance
            if food is not None:
                 # checks that the food is purchasable
                assert(food.price < player.balance), "Player cannot afford the food"
                possible_balance -= food.price

            # check cave quantities are correct
            if caves[i] is not None:
                cave, quantity = caves[i]

                if (cave.get_quantity() < 0):
                    cave.quantity = 0

                assert((abs(quantity - cave.quantity) < EPSILON) or (quantity < cave.quantity)), "cave does not have enough of that material"
                
                # remove the quantity mined
                cave.remove_quantity(quantity)
                
                if (cave.get_quantity() < 0):
                    cave.quantity = 0
                
                # find trader selling the material for the most emeralds
                max_sell_price = 0
                for trader in self.traders:         # O(T)
                    if cave.material == trader.current_deal()[0] and trader.current_deal()[1] > max_sell_price:     # O(compN)
                        max_sell_price = trader.current_deal()[1]

                possible_balance += quantity * max_sell_price
                
            # check remaining balance is possible
            assert(balances[i] <= possible_balance)
            # set player balance to the given balance
            player.balance = balances[i]
            
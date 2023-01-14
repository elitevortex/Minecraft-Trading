"""Code for Trader parent class, RandomTrader, RangeTrader, and HardTrader subclasses"""
from __future__ import annotations

from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen
from avl import AVLTree
from heap import MaxHeap

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    """ Abstract Trader class

    attributes:
        name (string) - name of the trader
        sell (tuple) - a tuple containing the: (Material, selling price)
        material - the stored materials of the trader - different for the different child classes
    
    complexity:
        unless otherwise stated methods have a complexity of O(1)
    """
    
    def __init__(self, name: str) -> None:
        """ initialising variables """
        assert(type(name) == str), "name should be of type string"
        self.name = name
        self.sell = None

    @abstractmethod
    def random_trader(cls) -> Trader:
        """ returns a random Trader of random name"""
        pass
    
    @abstractmethod
    def set_all_materials(self, mats: list[Material]) -> None:
        ''' adding materials to each Trader based on their respective type'''
        pass
    
    @abstractmethod
    def add_material(self, mat: Material) -> None:
        """ adding a material to the list of materials the trader has """
        pass
    
    @abstractmethod
    def remove_material(self, mat: Material) -> None:
        """ removing a material from the list of materials the trader has """
        pass
        
    def is_currently_selling(self) -> bool:
        """ returns whether the trader has a current deal or not """
        return self.sell is not None
    
    def current_deal(self) -> tuple[Material, float]:
        """ returns the trader's current deal """
        # raises an error if the trader is not selling anything
        if not self.is_currently_selling():
            raise ValueError("trader is not selling anything")

        # returns a tuple with the material and the selling price
        return self.sell
    
    @abstractmethod
    def generate_deal(self) -> None:
        """ generates a deal for a Trader based on specification on its type """
        pass
    
    def stop_deal(self) -> None:
        """ removes the current deal, setting it to None"""
        self.sell = None
    
    @abstractmethod
    def __str__(self) -> str:
        """Abstract tring representation of the Trader class - based on type of Trader"""
        pass

class RandomTrader(Trader):
    """ Random Trader class

    attributes:
        name (string) - name of the trader
        sell (tuple) - a tuple containing the: (Material, selling price)
        material (list) - the materials of a Random trader are stored in an inbuilt python List
    
    complexity:
        unless otherwise stated methods have a complexity of O(1)
    """

    def __init__(self, name: str):
        """ Initialisation for the RandomTrader class"""
        Trader.__init__(self, name)
        self.materials = []

    @classmethod
    def random_trader(cls) -> Trader:
        """ returns a RandomTrader of random name"""
        return RandomTrader(RandomGen.random_choice(TRADER_NAMES))

    def add_material(self, mat: Material) -> None:
        """ adding a material to the list of materials the trader has """
        assert type(mat) == Material, "the provided material is not a Material instance"
        self.materials.append(mat)
    
    def remove_material(self, mat: Material) -> None:
        """ removing a material from the list of materials the trader has """
        assert type(mat) == Material, "the provided material is not a Material instance"
        self.materials.remove(mat)
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """ sets all the list of materials to the provided list """
        assert type(mats) == list, "the provided list of materials is not a list"
        # stores materials in a list
        self.materials = mats

    def generate_deal(self) -> None:
        """ generates a deal with a random material """
        assert(len(self.materials) > 0), "there are no materials to generate a deal with"

        mat = RandomGen.random_choice(self.materials)
        price = round(2 + 8 * RandomGen.random_float(), 2)
        self.sell = (mat, price)

    def __str__(self) -> str:
        '''String representation of Random Class
        example:
        "<RandomTrader: Mr Barnes buying [Pickaxe: 7🍗/💎] for 7.57💰>", "Deal check failed>" 
        '''
        string = "<RandomTrader: " + self.name
        if not self.is_currently_selling():
            string += " is not buying anything at the moment"
        else:
            string += " buying " + str(self.sell[0]) + " for " + str(self.sell[1]) + "💰"
        string += ">"
        
        return string

class RangeTrader(Trader):
    """ Range Trader class

    attributes:
        name (string) - name of the trader
        sell (tuple) - a tuple containing the: (Material, selling price)
        material (AVLTree) - the materials of a Range trader are stored in an AVL Tree
    
    complexity:
        unless otherwise stated methods have a complexity of O(1)
    """ 
    def __init__(self, name: str):
        """Initialisation of RangeTrader"""
        Trader.__init__(self, name)
        self.materials = AVLTree()
        
    @classmethod
    def random_trader(cls) -> Trader:
        """ returns a RangeTrader of random name """
        return RangeTrader(RandomGen.random_choice(TRADER_NAMES))
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """ sets all the list of materials to an AVL tree 
        Complexity: 
            O(N * log N) where N is the number of materials
        """
        # add each material to the AVL Tree
        self.materials = AVLTree()
        for mat in mats:
            self.materials[mat.mining_rate] = mat

    def add_material(self, mat: Material) -> None:
        """ adding a material to the list of materials the trader has 
        Complexity:
            O(log N) where N = #Materials
        """
        assert type(mat) == Material, "the provided material is not a Material instance"
        self.materials[mat.mining_rate] = mat

    def remove_material(self, mat: Material) -> None:
        """ removing a material from the AVL Tree of materials the trader has """
        assert type(mat) == Material, "the provided material is not a Material instance"
        del self.material[mat.mining_rate]

    def materials_between(self, i: int, j: int) -> list[Material]:
        """ returns a sorted list of materials between the indexes of i and j

        Complexity:
            O(j - i + log(N)) where N = #Materials
        """
        return self.materials.range_between(i,j)
    
    def generate_deal(self) -> None:
        '''Generates a deal with a material between two random indices
        
        Complexity:
            O(j - i + log(N)) where N = #Materials in self.materials
        '''
        assert(len(self.materials) > 0), "there are no materials to generate a deal with"

        # generate two random indexes
        i = RandomGen.randint(0,len(self.materials)-1)
        j = RandomGen.randint(i,len(self.materials)-1)

        # creates a list of materials
        mat_list = self.materials_between(i, j)

        # gets a random material from above list and a random price
        mat = RandomGen.random_choice(mat_list)
        price = round(2 + 8 * RandomGen.random_float(), 2)
        self.sell = (mat, price)

    def __str__(self) -> str:
        '''String representation of Range Class as follows:
         "<RangeTrader: Mr Barnes buying [Pickaxe: 7🍗/💎] for 7.57💰>", "Deal check failed"
        '''
        string = "<RangeTrader: " + self.name 
        if not self.is_currently_selling():
            string += "is not buying anything at the moment"
        else:
            string += " buying " + str(self.sell[0]) + " for " + str(self.sell[1]) + "💰"
        string += ">"
        return string

class HardTrader(Trader):
    """ Hard Trader class

    attributes:
        name (string) - name of the trader
        sell (tuple) - a tuple containing the: (Material, selling price)
        material (MaxHeap) - the materials of a Hard trader are stored in a MaxHeap
    
    complexity:
        unless otherwise stated methods have a complexity of O(1)
    """

    def __init__(self, name: str):
        """Initialisation of HardTrader"""
        Trader.__init__(self, name)
        self.materials = MaxHeap(15)
        
    @classmethod
    def random_trader(cls) -> Trader:
        """ returns a HardTrader of random name """
        return HardTrader(RandomGen.random_choice(TRADER_NAMES))
        
    def generate_deal(self) -> None:
        """ generates a deal with a random material 

        Complexity:
            O(log N) where N is the number of materials in self.materials

        """
        assert(len(self.materials) > 0), "there are no materials to generate a deal with"
        
        # Gives hardest to mine material
        mat = self.materials.get_max()
        
        price = round(2 + 8 * RandomGen.random_float(), 2)
        self.sell = (mat,price)
        
    def set_all_materials(self, mats: list[Material]) -> None:
        """ sets all the list of materials to the heap 
        Complexity:
            O(N * log N) where N is the number of materials
        """
        # stores materials in a heap
        self.materials = MaxHeap(15)
        for mat in mats:
            self.materials.add(mat)
        
    def add_material(self, mat: Material) -> None:
        """ adding a material to the list of materials the trader has 
        Complexity:
            O(log N) where N = #materials
        """
        assert type(mat) == Material, "the provided material is not a Material instance"
        self.materials.add(mat)

    def remove_material(self, mat: Material) -> None:
        """ can't remove materials from a heap, just take out the biggest item """
        pass

    def __str__(self) -> str:
        '''String representation of Hard Class
        "<HardTrader: Mr Barnes buying [Gunpowder: 8🍗/💎] for 2.01💰>", "Deal check failed"
        '''
        string = "<HardTrader: " + self.name
        if not self.is_currently_selling():
            string += "is not buying anything at the moment"
        else:
            string += " buying " + str(self.sell[0]) + " for " + str(self.sell[1]) + "💰" 
        string += ">"
        return string
        

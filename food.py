""""Contains code implementing Food class its methods"""
from __future__ import annotations
from material import Material
from random_gen import RandomGen

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken",
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

class Food:
    """
    Food class

    Attributes: 
    - name (string) -> Name of food
    - hunger_bars (int) -> number of hunger bars of food will give when eaten
    - price(int) -> emerald cost of food
    
    All methods have best and worst case complexity of O(1).
    """
    
    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        """ initialises the class and arguments are of the correct type """
        assert(type(name) == str), "name is not of type string"
        self.name = name

        assert((type(hunger_bars) == int) and (hunger_bars > 0)), "hunger bars is not of valid type" 
        self.hunger_bars = hunger_bars

        assert((type(price) == int) and (price > 0)), "price is not of valid type"
        self.price = price

    def __str__(self) -> str:
        """String representation of Food item
        eg. '[Cooked Chicken Cuts: 424🍗 for 19💎]'
        """
        return f"[{self.name}: {self.hunger_bars}🍗 for {self.price}💎]"

    @classmethod
    def random_food(cls) -> Food:
        """ creates a random food with random name, hunger bars and cost """
        rand_name = FOOD_NAMES[RandomGen.randint(0, len(FOOD_NAMES) - 1)]
        rand_hunger_bars = RandomGen.randint(1, 500)
        rand_cost = RandomGen.randint(1, 50)
        
        return Food(rand_name, rand_hunger_bars, rand_cost)
        

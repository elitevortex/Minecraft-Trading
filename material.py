""""Contains code implementing Material class and its methods"""

from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:
    """ Material class

    attributes:
        name (string) - name of the material used to identify it
        mining_rate (float) - how many hunger points are needed to mine 
                            a single unit of the material

    complexity:
        unless otherwise stated all methods have a best/worst case complexity of O(1)
    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        """ initialises the class and ensures the mining rate is a float """
        self.name = name
        assert(type(mining_rate) == float or type(mining_rate) == int), "mining rate is not a float"
        self.mining_rate = mining_rate
    
    def __str__(self) -> str:
        """ string representation of the material
        example:
            "[Pickaxe: 7🍗/💎]"
        """
        return f"[{self.name}: {self.mining_rate}🍗/💎]"

    def __eq__(self, other) -> bool:
        """
        Allows for comparison between two Materials' names and returns True if both have the same name
        complexity:
            best/worst case: O(N) where N is the length of the material name
        """
        return other.name == self.name

    def __gt__(self, other) -> bool:
        """
        Allows for greater than comparison between two Materials' mining rates
        """
        return self.mining_rate > other.mining_rate
        
    def __ge__(self, other) -> bool:
        """
        Allows for greater than or equal to comparison between two Materials' mining rates
        """
        return self.mining_rate >= other.mining_rate

    def __lt__(self, other) -> bool:
        """
        Allows for less than comparison between two Materials' mining rates
        """
        return self.mining_rate < other.mining_rate

    def __le__(self, other) -> bool:
        """
        Allows for less than or equal to comparison between two Materials' mining rates
        """
        return self.mining_rate <= other.mining_rate
    

    @classmethod
    def random_material(cls):
        """ creates a material with a random name and mining rate """
        rand_name = RANDOM_MATERIAL_NAMES[RandomGen.randint(0, len(RANDOM_MATERIAL_NAMES) - 1)]
        rand_mining_rate = float(RandomGen.randint(1,30) / 2)
        return Material(rand_name, rand_mining_rate)


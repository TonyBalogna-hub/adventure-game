import random

class WanderingMonster:
    def __init__(self, x, y, monster_type, color, hp):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color
        self.hp = hp
        self.gold = random.randint(20, 100)

    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):
        monster_names = ["Golem", "Fire Spirit", "Lava Hound"]
        m_type = random.choice(monster_names)
        
        hp_map = {"Golem": 100, "Fire Spirit": 20, "Lava Hound": 175}
        color_map = {"Golem": [128, 128, 128], "Fire Spirit": [255, 69, 0], "Lava Hound": [139, 0, 0]}
        
        while True:
            rx = random.randint(0, grid_w - 1)
            ry = random.randint(0, grid_h - 1)
            pos = (rx, ry)
            
            if pos not in occupied and pos not in forbidden:
                return cls(rx, ry, m_type, color_map[m_type], hp_map[m_type])

    @classmethod
    def from_dict(cls, data):
        """Reconstructs the object from JSON data"""
        return cls(data['x'], data['y'], data['monster_type'], data['color'], data['hp'])

    def to_dict(self):
        """Converts object to a JSON-serializable dictionary"""
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    def move(self, occupied, forbidden, grid_w, grid_h):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            new_pos = (new_x, new_y)
            
            if 0 <= new_x < grid_w and 0 <= new_y < grid_h:
                if new_pos not in occupied and new_pos not in forbidden:
                    self.x = new_x
                    self.y = new_y
                    return

class Territory:
    def __init__(self, name, owner, ipc_value=0, is_capital=False, is_water=False, adjacent=None, units=None):
        self.name = name
        self.owner = owner
        self.ipc_value = ipc_value
        self.is_capital = is_capital
        self.is_water = is_water
        self.adjacent = adjacent if adjacent else []
        self.units = units if units else []

class Unit:
    def __init__(self, unit_type, owner):
        self.unit_type = unit_type
        self.owner = owner
        self.attack = self.set_attack_value()
        self.defense = self.set_defense_value()
        self.is_air_unit = unit_type in ['Fighter', 'Bomber']
        self.max_movement = self.set_movement_value()
        self.movement_left = self.max_movement
        self.has_attacked = False
        self.has_moved_combat = False
        self.has_moved_noncombat = False

    def set_attack_value(self):
        if self.unit_type == 'Infantry':
            return 1
        elif self.unit_type == 'Tank':
            return 3
        elif self.unit_type == 'Fighter':
            return 3
        elif self.unit_type == 'Bomber':
            return 4
        else:
            return 0

    def set_defense_value(self):
        if self.unit_type == 'Infantry':
            return 2
        elif self.unit_type == 'Tank':
            return 3
        elif self.unit_type == 'Fighter':
            return 4
        elif self.unit_type == 'Bomber':
            return 1
        else:
            return 0

    def set_movement_value(self):
        if self.unit_type == 'Fighter':
            return 4
        elif self.unit_type == 'Bomber':
            return 6
        elif self.unit_type == 'Tank':
            return 2
        else:
            return 1  # Default for infantry, ships later


class CombatGroup:
    def __init__(self, attacker, from_territory, to_territory):
        self.attacker = attacker
        self.from_territory = from_territory
        self.to_territory = to_territory
        self.ground_units = []    # Infantry, Tanks, etc.
        self.air_units = []       # Fighters, Bombers
        self.declared_landing_zones = {}  # Maps air units to intended landing territories

    def add_unit(self, unit, landing_zone=None):
        if unit.is_air_unit:
            self.air_units.append(unit)
            if landing_zone:
                self.declared_landing_zones[unit] = landing_zone
        else:
            self.ground_units.append(unit)

class DefenseGroup:
    def __init__(self, defender, territory):
        self.defender = defender
        self.territory = territory
        self.ground_units = []
        self.air_units = []
        self.naval_units = []

class Player:
    def __init__(self, name, country, ipc, turn_order, capital, is_human=False):
        self.name = name
        self.country = country
        self.ipc = ipc
        self.turn_order = turn_order
        self.capital = capital
        self.is_human = is_human
        self.purchased_units = []
        self.territories = []

# End of obj.py - Contains only core game object definitions

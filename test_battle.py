# test_battle.py

from obj import Territory, Player, Unit, CombatGroup, DefenseGroup
from combat_logic import CombatManager

# Setup simple test
player1 = Player("Player1", "Germany", 30, 1, "Germany", is_human=True)
player2 = Player("Player2", "Russia", 30, 2, "Moscow", is_human=True)

germany = Territory("Germany", player1)
eastern_europe = Territory("Eastern Europe", player2)

# Units
inf1 = Unit("Infantry", player1)
tank1 = Unit("Tank", player1)

inf2 = Unit("Infantry", player2)
inf3 = Unit("Infantry", player2)

# Groups
attack_group = CombatGroup(player1, germany, eastern_europe)
attack_group.add_unit(inf1)
attack_group.add_unit(tank1)

defense_group = DefenseGroup(player2, eastern_europe)
defense_group.ground_units.append(inf2)
defense_group.ground_units.append(inf3)

# Combat
manager = CombatManager()
manager.resolve_battle(attack_group, defense_group)

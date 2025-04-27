# test_movement.py

from obj import Territory, Player, Unit, CombatGroup, DefenseGroup
from combat_logic import CombatManager

# Setup simple test environment

# Players
player1 = Player("Player1", "Germany", 30, 1, "Germany", is_human=True)
player2 = Player("Player2", "Russia", 30, 2, "Moscow", is_human=True)

# Territories
germany = Territory("Germany", player1)
eastern_europe = Territory("Eastern Europe", player2)

# Board (simple dictionary)
territories = {
    'Germany': germany,
    'Eastern Europe': eastern_europe
}

# Units
germany.units.append(Unit("Infantry", player1))
germany.units.append(Unit("Tank", player1))
eastern_europe.units.append(Unit("Infantry", player2))
eastern_europe.units.append(Unit("Infantry", player2))

# Initialize CombatManager
combat_manager = CombatManager()

# Simulate Combat Movement Phase
print("Combat Movement Phase")
combat_group = CombatGroup(player1, germany, eastern_europe)

# Move 1 Infantry and 1 Tank from Germany to Eastern Europe
moving_units = []
for unit in list(germany.units):  # Use list() to safely modify while iterating
    if unit.unit_type in ["Infantry", "Tank"]:
        moving_units.append(unit)
        germany.units.remove(unit)

for unit in moving_units:
    combat_group.add_unit(unit)

# Add the combat group
combat_manager.add_combat_group(combat_group)

# Now simulate Defense Group setup (automatic for testing)
defense_group = DefenseGroup(player2, eastern_europe)
for unit in eastern_europe.units:
    defense_group.ground_units.append(unit)

# Resolve the combat
print("\nCombat Phase")
combat_manager.resolve_battle(combat_group, defense_group)

# Aftermath
print("\nPost-Combat Status:")
print(f"Owner of Eastern Europe: {eastern_europe.owner.name}")
print(f"Units remaining in Eastern Europe: {[unit.unit_type for unit in eastern_europe.units]}")

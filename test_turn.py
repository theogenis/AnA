# test_turn.py

from obj import Territory, Player, Unit, CombatGroup, DefenseGroup
from combat_logic import CombatManager
from movement_logic import MovementManager
from purchase_logic import PurchaseManager

# --- Setup Simple Test Environment ---

# Players
player1 = Player("Player1", "Germany", 30, 1, "Germany", is_human=True)
player2 = Player("Player2", "Russia", 30, 2, "Moscow", is_human=True)

# Territories
germany = Territory("Germany", player1)
germany.ipc_value = 10

eastern_europe = Territory("Eastern Europe", player2)
eastern_europe.ipc_value = 6

# Board
territories = {
    'Germany': germany,
    'Eastern Europe': eastern_europe
}

# Units
germany.units.append(Unit("Infantry", player1))
germany.units.append(Unit("Tank", player1))

eastern_europe.units.append(Unit("Infantry", player2))
eastern_europe.units.append(Unit("Infantry", player2))

# Managers
combat_manager = CombatManager()
movement_manager = MovementManager(territories, combat_manager)
unit_prices = {
    "Infantry": 3,
    "Tank": 5,
    "Fighter": 10,
    "Bomber": 15
}
purchase_manager = PurchaseManager(unit_prices)

# --- Utility Function ---
def collect_income(player, territories):
    income = 0
    for territory in territories.values():
        if territory.owner == player:
            income += getattr(territory, 'ipc_value', 0)
    player.ipc += income
    print(f"{player.name} collected {income} IPCs. New IPC total: {player.ipc}")

def reset_unit_flags(player, territories):
    for territory in territories.values():
        if territory.owner == player:
            for unit in territory.units:
                unit.has_moved_combat = False
                unit.has_moved_noncombat = False
                unit.has_attacked = False

# --- Simulate One Full Player Turn ---

# 1. Purchase Phase
print("\n=== Purchase Phase ===")
purchase_manager.purchase_units(player1)

# 2. Combat Movement Phase
print("\n=== Combat Movement Phase ===")
movement_manager.combat_movement(player1)

# 3. Combat Phase
print("\n=== Combat Phase ===")
for combat_group in combat_manager.combat_groups:
    defender = combat_group.to_territory.owner
    defense_group = DefenseGroup(defender, combat_group.to_territory)
    for unit in combat_group.to_territory.units:
        defense_group.ground_units.append(unit)

    combat_manager.resolve_battle(combat_group, defense_group)

combat_manager.clear_after_combat()

# 4. Non-Combat Movement Phase
print("\n=== Non-Combat Movement Phase ===")
movement_manager.non_combat_movement(player1)

# 5. Placement Phase
print("\n=== Placement Phase ===")
purchase_manager.place_units(player1, territories)

# 6. Collect Income Phase
print("\n=== Collect Income Phase ===")
collect_income(player1, territories)

# 7. End of Turn Cleanup
print("\n=== End of Turn ===")
reset_unit_flags(player1, territories)

# --- Final Board Status ---
print("\n=== Final Board Status ===")
for name, territory in territories.items():
    print(f"{name} (Owner: {territory.owner.name})")
    for unit in territory.units:
        print(f" - {unit.unit_type}")

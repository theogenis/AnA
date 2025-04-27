# turn_manager.py

from purchase_logic import PurchaseManager
from movement_logic import MovementManager
from combat_logic import CombatManager
from obj import Player, Territory, Unit, CombatGroup, DefenseGroup

class TurnManager:
    def __init__(self, players, territories, unit_prices):
        self.players = players  # list of Player objects
        self.territories = territories  # dictionary of territory name -> Territory object
        self.combat_manager = CombatManager()
        self.movement_manager = MovementManager(territories, self.combat_manager)
        self.purchase_manager = PurchaseManager(unit_prices)
        self.turn_counter = 1

    def check_victory(self):
        for player in self.players:
            opponent_capitals = [p.capital for p in self.players if p != player]

            player_territories = [
                territory.name for territory in self.territories.values()
                if territory.owner == player
            ]

            for capital in opponent_capitals:
                if capital in player_territories:
                    print(f"\n=== {player.name} has captured {capital}! ===")
                    print(f"=== {player.name} WINS THE GAME! ===")
                    return True  # Game ends
        return False  # Game continues


    def play_game(self):
        game_active = True
        while game_active:
            for player in self.players:
                print(f"\n--- Turn {self.turn_counter}: {player.name}'s Turn ---")
                self.play_turn(player)

                # Check for victory after each full player turn
                if self.check_victory():
                    game_active = False
                    break

            self.turn_counter += 1


    def play_turn(self, player):
        # 1. Purchase Units
        print("\n=== Purchase Phase ===")
        self.purchase_manager.purchase_units(player)

        # 2. Combat Movement
        print("\n=== Combat Movement Phase ===")
        self.movement_manager.combat_movement(player)

        # 3. Combat Phase
        print("\n=== Combat Phase ===")
        for combat_group in self.combat_manager.combat_groups:
            defender = combat_group.to_territory.owner
            defense_group = DefenseGroup(defender, combat_group.to_territory)
            for unit in combat_group.to_territory.units:
                defense_group.ground_units.append(unit)

            self.combat_manager.resolve_battle(combat_group, defense_group)

        self.combat_manager.clear_after_combat()

        # 4. Non-Combat Movement
        print("\n=== Non-Combat Movement Phase ===")
        self.movement_manager.non_combat_movement(player)

        # 5. Placement Phase
        print("\n=== Placement Phase ===")
        self.purchase_manager.place_units(player, self.territories)

        # 6. Collect Income Phase
        print("\n=== Collect Income Phase ===")
        self.collect_income(player)

        # 7. Reset Unit Movement Flags
        print("\n=== End of Turn Reset ===")
        self.reset_unit_flags(player)

    def collect_income(self, player):
        income = 0
        for territory in self.territories.values():
            if territory.owner == player:
                income += getattr(territory, 'ipc_value', 0)
        player.ipc += income
        print(f"{player.name} collected {income} IPCs. New IPC total: {player.ipc}")

    def reset_unit_flags(self, player):
        for territory in self.territories.values():
            if territory.owner == player:
                for unit in territory.units:
                    unit.has_moved_combat = False
                    unit.has_moved_noncombat = False
                    unit.has_attacked = False

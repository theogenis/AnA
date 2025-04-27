# movement_logic.py

from obj import Territory, Unit, Player, CombatGroup

class MovementManager:
    def __init__(self, board, combat_manager):
        self.board = board  # The territories dictionary
        self.combat_manager = combat_manager

    def combat_movement(self, player):
        print(f"\n{player.name}'s Combat Movement Phase")

        # Loop for multiple moves until player says done
        while True:
            from_name = input("Enter the territory you are moving units from (or 'done' to finish): ").strip()

            if from_name.lower() == 'done':
                break

            if from_name not in self.board:
                print("Invalid source territory.")
                continue

            from_territory = self.board[from_name]

            if from_territory.owner != player:
                print("You do not control that territory.")
                continue

            to_name = input("Enter the territory you are moving units to: ").strip()

            if to_name not in self.board:
                print("Invalid destination territory.")
                continue

            to_territory = self.board[to_name]

            # After player chooses from_territory and to_territory:
            if to_territory.name not in from_territory.adjacent:
                print("You cannot move there. It is not adjacent.")
                continue

            if to_territory.owner == player:
                print("You cannot move into a territory you already control during Combat Movement. Use Non-Combat Movement instead.")
                continue

            # Select which units to move
            units_to_move = []

            print(f"Units in {from_territory.name}:")
            for idx, unit in enumerate(from_territory.units):
                print(f"{idx}: {unit.unit_type}")

            while True:
                unit_choice = input("Enter unit index to move (or 'done' to finish selecting units): ").strip()

                if unit_choice.lower() == 'done':
                    break

                if not unit_choice.isdigit():
                    print("Invalid input.")
                    continue

                idx = int(unit_choice)
                if idx < 0 or idx >= len(from_territory.units):
                    print("Invalid index.")
                    continue

                selected_unit = from_territory.units[idx]
                units_to_move.append(selected_unit)

            if not units_to_move:
                print("No units selected.")
                continue

            # Remove units from source territory
            for unit in units_to_move:
                from_territory.units.remove(unit)

            # Decide what kind of move
            if to_territory.owner != player:
                # Enemy territory → create CombatGroup
                combat_group = CombatGroup(player, from_territory, to_territory)
                for unit in units_to_move:
                    combat_group.add_unit(unit)
                self.combat_manager.add_combat_group(combat_group)
            else:
                # Friendly territory → normal move (would be in Non-Combat phase normally)
                to_territory.units.extend(units_to_move)

            print(f"Moved {len(units_to_move)} units from {from_territory.name} to {to_territory.name}.")


    def non_combat_movement(self, player):
        print(f"\n{player.name}'s Non-Combat Movement Phase")

        while True:
            from_name = input("Enter the territory you are moving units from (or 'done' to finish): ").strip()

            if from_name.lower() == 'done':
                break

            if from_name not in self.board:
                print("Invalid source territory.")
                continue

            from_territory = self.board[from_name]

            if from_territory.owner != player:
                print("You do not control that territory.")
                continue

            to_name = input("Enter the territory you are moving units to: ").strip()

            if to_name not in self.board:
                print("Invalid destination territory.")
                continue

            to_territory = self.board[to_name]

            # After player chooses from_territory and to_territory:
            if to_territory.name not in from_territory.adjacent:
                print("You cannot move there. It is not adjacent.")
                continue

            # Validate destination is friendly (owned by player)
            if to_territory.owner != player:
                print("You can only non-combat move into friendly territories you control.")
                continue

            # Select which units to move
            eligible_units = [unit for unit in from_territory.units if not unit.has_moved_combat]

            if not eligible_units:
                print("No eligible units to move from this territory.")
                continue

            print(f"Eligible units in {from_territory.name}:")
            for idx, unit in enumerate(eligible_units):
                print(f"{idx}: {unit.unit_type}")

            units_to_move = []
            while True:
                unit_choice = input("Enter unit index to move (or 'done' to finish selecting units): ").strip()

                if unit_choice.lower() == 'done':
                    break

                if not unit_choice.isdigit():
                    print("Invalid input.")
                    continue

                idx = int(unit_choice)
                if idx < 0 or idx >= len(eligible_units):
                    print("Invalid index.")
                    continue

                selected_unit = eligible_units[idx]
                units_to_move.append(selected_unit)

            if not units_to_move:
                print("No units selected.")
                continue

            # Remove units from source and add to destination
            for unit in units_to_move:
                from_territory.units.remove(unit)
                to_territory.units.append(unit)
                unit.has_moved_noncombat = True  # Mark they moved non-combat

            print(f"Moved {len(units_to_move)} units from {from_territory.name} to {to_territory.name}.")


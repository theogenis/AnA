# purchase_logic.py

from obj import Player, Unit

class PurchaseManager:
    def __init__(self, unit_prices):
        self.unit_prices = unit_prices  # Dictionary of unit types to IPC cost

    def purchase_units(self, player):
        print(f"{player.name}, you have {player.ipc} IPCs to spend.")
        purchasing = True

        while purchasing:
            # For now, simple text input for purchases (later, could be scripted/AI)
            print("Available units to purchase:")
            for unit_type, cost in self.unit_prices.items():
                print(f"{unit_type}: {cost} IPCs")

            choice = input("Enter unit to purchase (or 'done' to finish): ").strip()

            if choice.lower() == 'done':
                purchasing = False
                break

            if choice in self.unit_prices and player.ipc >= self.unit_prices[choice]:
                player.purchased_units.append(Unit(choice, player))
                player.ipc -= self.unit_prices[choice]
                print(f"Purchased {choice}. Remaining IPCs: {player.ipc}")
            else:
                print("Invalid choice or insufficient IPCs.")

    def place_units(self, player, territories):
        print(f"{player.name}, place your purchased units.")

        for unit in player.purchased_units:
            placed = False
            while not placed:
                print(f"Placing {unit.unit_type}")
                territory_name = input("Enter territory name to place unit: ").strip()

                if territory_name in territories:
                    territory = territories[territory_name]
                    if territory.owner == player:
                        territory.units.append(unit)
                        placed = True
                        print(f"Placed {unit.unit_type} in {territory.name}.")
                    else:
                        print("You do not own that territory.")
                else:
                    print("Invalid territory.")

        # Clear purchased units after placement
        player.purchased_units = []

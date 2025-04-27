# combat_logic.py

from obj import CombatGroup, DefenseGroup, Unit

import random

class CombatManager:
    def __init__(self):
        self.combat_groups = []
    
    def add_combat_group(self, combat_group):
        self.combat_groups.append(combat_group)

    def roll_attacks(self, attack_group):
        hits = 0
        for unit in attack_group.ground_units + attack_group.air_units:
            roll = random.randint(1,6)
            if roll <= unit.attack:
                hits += 1
        return hits

    def roll_defenses(self, defense_group):
        hits = 0
        for unit in defense_group.ground_units + defense_group.air_units + defense_group.naval_units:
            roll = random.randint(1,6)
            if roll <= unit.defense:
                hits += 1
        return hits

    def apply_hits(self, group, hits):
        # Basic logic: remove cheapest units first
        all_units = group.ground_units + group.air_units
        all_units.sort(key=lambda unit: unit.attack + unit.defense)  # Weakest units die first
        for _ in range(hits):
            if all_units:
                unit = all_units.pop(0)
                if unit in group.ground_units:
                    group.ground_units.remove(unit)
                elif unit in group.air_units:
                    group.air_units.remove(unit)

    def resolve_battle(self, combat_group, defense_group):
        print(f"Battle for {defense_group.territory.name} begins!")
        territory = defense_group.territory

        while combat_group.ground_units or combat_group.air_units:
            attacker_hits = self.roll_attacks(combat_group)
            defender_hits = self.roll_defenses(defense_group)

            print(f"Attackers scored {attacker_hits} hits!")
            print(f"Defenders scored {defender_hits} hits!")

            self.apply_hits(defense_group, attacker_hits)
            self.apply_hits(combat_group, defender_hits)

            # Check for battle outcome
            attacker_alive = combat_group.ground_units or combat_group.air_units
            defender_alive = defense_group.ground_units or defense_group.air_units

            if not defender_alive and attacker_alive:
                print("Attackers win!")
                territory.owner = combat_group.attacker
                territory.units = combat_group.ground_units + combat_group.air_units
                return

            if not attacker_alive and defender_alive:
                print("Defenders win!")
                territory.units = defense_group.ground_units + defense_group.air_units
                return

            if not attacker_alive and not defender_alive:
                print("Both sides destroyed! Territory remains with defender.")
                territory.units = []
                return
            
    def clear_after_combat(self):
        self.combat_groups = []
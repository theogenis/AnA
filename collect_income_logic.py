def collect_income(player, territories):
    income = 0
    for territory in territories.values():
        if territory.owner == player:
            income += territory.ipc_value
    player.ipc += income
    print(f"{player.name} collected {income} IPCs.")

# board_setup.py

from obj import Player, Territory, Unit

def initialize_players():
    player1 = Player("Germany", "Germany", 30, 1, "Germany", is_human=True)
    player2 = Player("Russia", "Russia", 30, 2, "Russia", is_human=True)
    return [player1, player2]

def initialize_territories(players):
    germany = Territory("Germany", players[0], ipc_value=10)
    poland = Territory("Poland", players[0], ipc_value=6)
    france = Territory("France", players[0], ipc_value=6)
    
    russia = Territory("Russia", players[1], ipc_value=10)
    ukraine = Territory("Ukraine", players[1], ipc_value=6)
    karelia = Territory("Karelia", players[1], ipc_value=6)

    territories = {
        "Germany": germany,
        "Poland": poland,
        "France": france,
        "Russia": russia,
        "Ukraine": ukraine,
        "Karelia": karelia,
    }

    # Define adjacency
    germany.adjacent = ["Poland", "France"]
    poland.adjacent = ["Germany", "Ukraine"]
    france.adjacent = ["Germany"]

    russia.adjacent = ["Ukraine", "Karelia"]
    ukraine.adjacent = ["Russia", "Poland"]
    karelia.adjacent = ["Russia"]

    return territories

def initialize_units(players, territories):
    # Germany
    territories["Germany"].units.append(Unit("Infantry", players[0]))
    territories["Germany"].units.append(Unit("Tank", players[0]))
    territories["Poland"].units.append(Unit("Infantry", players[0]))

    # Russia
    territories["Russia"].units.append(Unit("Infantry", players[1]))
    territories["Russia"].units.append(Unit("Tank", players[1]))
    territories["Ukraine"].units.append(Unit("Infantry", players[1]))

def setup_board():
    players = initialize_players()
    territories = initialize_territories(players)
    initialize_units(players, territories)
    return players, territories

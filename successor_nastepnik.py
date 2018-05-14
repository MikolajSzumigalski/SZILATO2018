import game_logic
import A_star
import copy
def successor(LogicEngine):
    """
    this function prepars a list of pairs of [available target coordinates, LogicEngine outcome of target interaction]
    this is a successor function (nastepnik)
    :param LogicEngine:
    :return: list of pairs [[x,y], [LogicEngine]]
    """
    list_of_available_target_destinations = get_all_available_targets(LogicEngine)
    outcome = list()
    for target in list_of_available_target_destinations:
        try:
            entry = [target, LogicEngine.simulate_move_absolute_coordinate(save_simulated_state_JSON = False, x = target[0][0], y = target[0][1])]
            outcome.append(entry)
        except IndexError:
            pass;
    return outcome


def get_all_available_targets(LogicEngine):
    """
    this function checks for which monsters and mixtures there is available a direct path for the player
    :param LogicEngine:
    :return: list of [x,y] attributes of mixtures and monsters the player can get to
    """
    potential_targets = LogicEngine.get_mixtures_positions() + LogicEngine.get_monsters_positions()
    A_star_instance = A_star.A_star_path(LogicEngine)
    return [A_star_instance.get_path_to(target) for target in potential_targets if (A_star_instance.get_path_to(target) is not [[]] and ((A_star_instance.get_path_to(target) is not None))) ]




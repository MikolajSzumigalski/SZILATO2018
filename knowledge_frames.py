import game
import jsonpickle
import copy
import simplejson
#this is a helper file that manages saving the in-game data in JSON SI frame format

def save_data(LogicEngine):
    """this function saves game data in JSON form to the file"""

    monsters_list = LogicEngine.monsters
    final_monsters_dict = {"MONSTERS": monsters_list}

    player = LogicEngine.player
    final_player_dict = {"PLAYER": player}

    map_tiles = LogicEngine.map.tiles_data
    final_tiles_dict = {"TILES": map_tiles}

    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    final_JSON = jsonpickle.encode([final_player_dict, final_monsters_dict, final_tiles_dict], unpicklable=False)
    __save_to_file__(final_JSON)

def __save_to_file__(JSON):
    """this function rewrites the file with data in JSON form"""
    with open("frames.json", "w") as f:
        f.writelines(JSON)

#THIS template method will jonsify its class
    # def toJSON(self):
    #     """
    #     This function JSONifies the class
    #     :return JSON form of class:
    #     """
    #     jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    #     json_form = jsonpickle.encode(self, unpicklable=False)
    #     return json_form


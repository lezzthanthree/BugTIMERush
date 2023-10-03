from scripts import gamedata

class Game():
    def __init__(self):
        self.__level = 0
        self.__dead_reason = "FIRST_CALL_FUNCTION_ERROR"
        self.savedata = gamedata.get_save_data()

    def set_level(self, level):
        self.__level = level

    def set_reason(self, reason):
        self.__dead_reason = reason

    def get_level(self):
        return self.__level
    
    def get_reason(self):
        return self.__dead_reason
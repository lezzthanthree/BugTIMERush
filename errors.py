class InvalidLevelSave(Exception):
    def __init__(self):
        self.message = "currentlvl cannot be read properly"
        super().__init__(self.message)

class AntiCheatException(Exception):
    def __init__(self, reason):
        self.message = f"{reason}"
        super().__init__(self.message)

class SceneException(Exception):
    def __init__(self, scene):
        self.message = f"{scene} does not exist"
        super().__init__(self.message)
from Python.lift_manager import LiftManager

class Simulation:
    def __init__(self, width: int, height: int, floors: int = 6):
        self.width = width
        self.height = height
        self.floors = floors

        self.lift_manager = LiftManager()
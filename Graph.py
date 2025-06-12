class Point():
    def __init__(self, connections: list, name: str):
        self.positionX = None
        self.positionY = None
        self.name = name
        self.connections = connections
        

    def set_position(self, x, y):
        self.positionX = x
        self.positionY = y
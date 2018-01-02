# mediator between Control, Model and Viewer 
class EventManager:
    def __init__(self):
        self.listeners = []

    # add a listener
    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    # remove a listener
    def del_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)
    
    # send event to all listeners
    def notify(self, event):
        for listener in self.listeners:
            listener.notify(event)


# superclass for events
class Event:
    def __init__(self):
        self.name = "Generic Event"

# on game quit, Q-key
class Quit(Event):
    def __init__(self):
        pass

# player movement, arrow-keys
class PlayerThrust(Event):
    def __init__(self, direction):
        self.direction = direction

class PlayerBrake(Event):
    def __init__(self):
        pass

# when a player moves out of the current room
class RoomExit(Event):
    def __init__(self, direction):
        self.direction = direction

class ClearScreen(Event):
    def __init__(self):
        pass

# when an object dies
class ObjDeath(Event):
    def __init__(self, rect):
        self.rect = rect


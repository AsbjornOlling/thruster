# superclass for objects passed to and from eventManager
class Event:
    def __init__(self):
        self.name = "Generic Event"


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


# make the listener object
evm = EventManager()


class Quit(Event):
    def __init__(self):
        pass


class PlayerThrust(Event):
    def __init__(self, direction):
        self.direction = direction


class WallDeath(Event):
    def __init__(self, rect):
        self.rect = rect

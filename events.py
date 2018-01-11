"""Eventmanager for defining and sending events between modules.

Contains the EventManager class, which has a list of listeners,
as well as functions to send Event objects to all listeners.

Also contains Event classes to define different event types.
"""


class EventManager:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        """Add an event listener object.

        The listener object will be sent every event.
        The listener object must contain a notify function.
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def del_listener(self, listener):
        """Remove an event listener.

        Removes a listener object from list of listeners.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notify(self, event):
        """Pass event on to all listeners.

        When an event object is received, pass it on to all of
        the listener objects, by calling their notify() function.
        """
        for listener in self.listeners:
            listener.notify(event)


class Event:
    """Generit Event

    All other events should inherit from this class.
    """
    def __init__(self):
        self.name = "Generic Event"


class Quit(Event):
    """Game Quit Event

    Currently only triggered by Q key.
    """
    def __init__(self):
        pass


class PlayerThrust(Event):
    """Player moves in some direction.

    Currently only triggered by arrow keys.
    """
    def __init__(self, direction):
        self.direction = direction


class PlayerBrake(Event):
    """Player fires brakeshot.

    Currently only triggered by space button.
    """
    def __init__(self):
        pass


class RoomExit(Event):
    """Player exits room.

    Created when player leaves the game screen.
    """
    def __init__(self, direction):
        self.direction = direction


class ClearScreen(Event):
    """Instruct viewer to clear screen.

    This event is sent on game creation.
    """
    def __init__(self):
        pass


class ObjDeath(Event):
    """Instruct viewer to redraw area

    Happens when a programmatically drawn sprite disappears.
    """
    def __init__(self, rect):
        self.rect = rect

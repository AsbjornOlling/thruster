# Thruster game
# WIP

class App:
    def __init__(self):
        pygame.init()

        # display caption
        pygame.display.set_caption("THRUSTER")

        # make player obj
        self.p = player.Player()

    # receive events from evm
    def notify(self, event):
        if isinstance(event, events.Quit):
            self.cleanup()

    def cleanup(self):
        pygame.quit()
        quit()


if __name__ == "__main__":
    import pygame
    from pygame.locals import *
    import game
    import view
    import events
    import controls
    import player

    app = App()
    kb = controls.KeyboardController()
    
    # maybe do this in the constructor
    events.evm.add_listener(app)

    # main loop
    while True:
        # handle keyboard events
        kb.update()
        # update all sprites
        game.allsprites.update()
        # draw everything
        view.vw.update()

        # tick
        game.dt = game.clock.tick(view.vw.fps)

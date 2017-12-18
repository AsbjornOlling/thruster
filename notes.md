## Some architecture notes

### General Brainstorm

* App 
    * clock
    * title
    * screenres
    * handles pause, ui elements
    * main loop

* Game 
    * spritegroups
    * levels, maps
    * map generation

* Actor
    * move() - according to velocity vector
    * update()
    * health, die()
    * accelerate()
    * player
        * handle thrusters differently
        * unique event playerMove

* Drawer
		* keep list of rects to update
		* contains special effects funcitions (e.g. thruster flame)

* EVENTS
    * keyboard events
    * sprite events
        * colission
				* movement (e.g. sent to drawer)
		* app events
				- quit
				- pause


### Who talks to whom

**MVC Model:**

Model: Sprites, game.py

Viewer: on_render()

Controller: on_event()

*Model to viewer:* areas to update, special effects calls, pause state
*Model to controller:* n/a
*Model to model:* updating positions, behavior on colissions

*Viewer to model:* n/a
*Viewer to controller:* n/a
*Viewer to viewer:* n/a

*Controller to model:* all kb input, mouse input, exit signals
*Controller to viewer:* n/a


## Goals and milestones

### Dec. 18

**Goals:**

- rename files to make sense
* deprecate settings.py
* make Drawer object
- start adding Events classes



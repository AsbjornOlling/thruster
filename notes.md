# Some design notes

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

### Milestones

**Dec 25:**

	- scaling thruster animation
	- proper collision detection and bouncing off walls
	- some kind of placeholder enemy to blow up

**Jan 2:**

	- ability to leave starting room
	- basic tools to make rooms with enemies in them
	- velocity bomb

### Dec. 18

**Goals:**

- deprecate settings.py
- make event handler class
- moved towards mvc design
- start adding events classes

**Accomplished:**

- deprecate settings.py
- make event handler class
- moved towards mvc design
- start adding events classes

### Dec. 19

**Goals:**

	* thruster animation in view class

**Accomplished:**



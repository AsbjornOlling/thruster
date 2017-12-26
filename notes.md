# Some design notes

### Architecture overview

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


### Who talks to whom (mediator scratch notes)

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

### Scratchpad: Global variables

game.dt 
	- needed by everything in model

view.width, view.height
	- game class

eventmanager
	- passed to every object taht is listener or needs children listeners

**Arch. rewrite checklist:**

X Game class
X Pass view width, height to game class
* replace width and height refs
* organize main loop
* replace all major object refs

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

	* thruster animation in view class
	* fixed thruster position bug in player.py

### Dec. 20

**Goals:**

	* make growth / shrink rates of thruster better
	* new room walls
	* collision detection for bouncing off walls

**Accomplished:**
	* make growth / shrink rates of thruster better
	* debugged thruster sprite a bunch
	* new room walls
	* room class
	* wall drawer function
	* collision detection for bouncing off walls

### Dec. 21

**Goals:**

	* Placeholder enemy/crate to kill w/ thruster (maybe color change too)
	* Clean up code for readability

**Accomplished:**

	* WallDestructible class, w/ health and reacts to collision w/ thrust

### Dec. 23

**Accomplished:**

	* Completed new, more general collision method. 
	* Added color change for destructiblewall class

# Some design notes

## Broad notes

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


### Room generator scratch notes

**Criteria:**

	* Open gate on entrypoint
	* Makes walls in every room
	* Content based on progress
	* Coherent coordinates

**Required input:**

	* Previous room
		- previous coords
	* Game object
		- game progress

**Possible solutions:**

	* Everything in room constructor
		* **Pros:**
			- close to relevant object
			- smaller gamestate object
		- **Cons:**
			- pass more data to room (last room)
			- larger room class
			- further from progress params

	* Method in gamestate object
		* **Pros:**
			- closer to progress params
		* **Cons:**
			- complicates gamestate object purpose

	* Separate generator object
		* **Pros:**
			- common random generator, seed
			- evt. other utils
		* **Cons:**
			- spaghet

### Brake-shot collision scratch notes

**Core problem:**
- detect collisions
- sc

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

Jan 14:
	
	* Scaling velocity bomb sprite
	* Fuel consumption and death mechanic
	* Basic enemy


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

### Dec. 27

**Goals:**

	* Destructible gates
	* Detect leaving the room
	* Room coordinates
	* Rooms grid

**Accomplished:**

	* Walls now add themselves to room spritegroup
	* Added destructible gates to room walls
	* Detect leaving the room
	* Started notes about room generation


### Jan 6.

**Goals:**

	* Fuel comsumption bar
	* Max length for player truster
	* Width scaling for player thruster


**Accomplished:**

## Some architecture notes

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


## Goals and milestones

### Dec. 18

**Goals:**

- rename files to make sense
* deprecate settings.py
* make Drawer object
- start adding Events classes



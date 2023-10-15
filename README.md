# Raspberry Pi Sense Hat Progs
> Games and Tools for Raspberry Pi Sense Hat
> You need a Raspberry PI Single Board Computer
> equipped with a "Sense Hat" Board to run these programs.

---

###Starry Night 1
Emulates a starry night screen.
Background is a somewhat-flickering dark blue pattern.
Colorful shiny stars pop up randomly and later also extinct randomly.

###Starry Night 2
Similar to Starry Night 1, but the colorful stars poppig up are "Supernovas", so they appear bright and then slowly fade away during their existence until they completely disappear in the background.

###Air Data
Display Temperature, Humidity and Air Pressure as different color scrolling texts on the 8x8 dot matrix screen.

###Sense Hat Maze
Find Your way to the Exit of the Maze, collecting all 3 necessary keys to open the Exit door.

![Screenshot-Maze](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/scrot-Maze.png)

**Game Rules**:

Use the joystick to navigate inside the labyrinth.
Unvisited rooms appear with blue walls while visited ones appear in green.
The shortest route from the start to Your current position will show up brown to help You find Your way back from where You came from.

The 3 keys to collect will appear shiny bright green, yellow and red in the maze and the room's walls they are in are also enlighted by the same color light.
In the top row (which is the status row) You will see which keys You already have: Dark color keys mean You still need to find these. Bright color means You already have the respective key.
The exit cell will show up light magenta, enlightening the whole room with magenta around it.

The right edge of the screen is some kind of "Item Radar" showing which item is the closest and how far is it measured directly (not following the route) -- giving You a hint which direction the closest feature is.
The color of the bar is the color of the item that is closest, and the length and brightness of the bar hints the distance. (first the bar is dark, going from 0-8, then a bright bar is overlapping going 0-8)
Until You don't have all the keys the radar will only show You the closest key not taking care about the exit as You can not exit any way without all 3 keys. When You get all 3 keys the radar will only mind about the exit.


---

###TODO:

####Compass
Display a proper compass utilizing the magnetometer sensor of the Sense Hat.

####Reversi
Play a reversi game on the 8x8 LED matrix screen against the computer



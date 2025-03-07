# Raspberry Pi Sense Hat Progs

> Games and Tools for Raspberry Pi Sense Hat.  
> You need a Raspberry PI Single Board Computer equipped with a "Sense Hat" Board to run these programs.  
> Worst case You can also use the Sense Hat Emulator...  
> Some of the games are just a python re-written version of the famous sgt-puzzles collection _(find on GitHub)_, using the original C++ source code and applying some simplifications, some are completely own code development from scratch, and for some games I have taken inspiration from already existing codes publicly available on GitHub, although the Python realization and the coding for SenseHat is still own work.  

---

## GADGETS

### Starry Night 1

![Screenshot-Starry1](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Starry1.jpg)

Emulates a starry night screen.
Background is a somewhat-flickering dark blue pattern.
Colorful shiny stars pop up randomly and later also extinct randomly.

### Starry Night 2

![Screenshot-Starry2](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Starry2.jpg)

Similar to Starry Night 1, but the colorful stars poppig up are "Supernovas", so they appear bright and then slowly fade away during their existence until they completely disappear in the background.

### Fire

![Screenshot-Fire](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Fire.jpg)

Simulate a flaming fire.

### Paint Drips and Paint Drips 2

![Screenshot-PaintDrips](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-PaintDrips.jpg)

Colorful paint is dripping on Your screen, spreading, mixing with the other color drips and fading away.
- Paint Drips 1 uses a "traditional" linear programming, managing and handling all pixels separately by the code.
- Paint Drips 2 treats the 2x2 screen elements as objects that can interfere with their neighbouring objects: They can send paint splashes to the neighbours when receiving a drip, as well as receive paint splashes from the neighbours and get the adjacent LEDs tinted to a certain extent with the neighbouring color.

### Aquarium

![Screenshot-Aquarium](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Aquarium.jpg)

Simulate an aquarium with swimming fish, seaweed, and some bubbles. Inspiration taken from asciiaquarium terminal gadget.

### Air Data

![Screenshot-AirData](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-AirData.jpg)

Display Temperature, Humidity and Air Pressure as different color texts and bar charts on the 8x8 LED display.
1 column is 1 hour in the history. Values are normed to min-max. Pressure center line is latest value.


### Space Weather

![Screenshot-SpaceWeather](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-SpaceWeather.jpg)

Retrieve Space Weather Data from NOAA and display the status.
The **top row** of the 8x8 LED display will be the Particle Flux status and data readiness status:

* **High Energy Proton Flux** (>1MeV, >10MeV and >100MeV) displayed in the top-left corner: `p1`, `p2`, `p3`
* **High Energy Electron Flux** (>2MeV) displayed middle of the top row `e1`
* **Data Validity Status** is in the top-right corner as a blinker `ST`

On the main part of the screen there are the bar charts:

* **X-Ray Status** is in the rightmost column `xr`, separated: Column color represents: `B`-Green, `C`-Yellow, `M`-Orange, `X`-Red
* **Kp Status** is on the left side `kp`: the last 6 of the 3 hrs values displayed as columns

|p1|p2|p3|  |e1|  |  |ST|
|--|--|--|--|--|--|--|--|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|
|kp|kp|kp|kp|kp|kp|  |xr|

For a detailed description what the values mean please visit NOAA home page.



---

## GAMES

### Maze

> Find Your way to the Exit of the Maze, collecting all 3 necessary keys to open the Exit door.


![Screenshot-Maze](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Maze.jpg)

**Game Rules**:

Use the joystick (stick version) or the cursor keys (pygame version) to navigate inside the labyrinth.
Unvisited rooms appear with blue walls while visited ones appear in green.
The walls of corridors belonging to the shortest route from the start to Your current position will show up brown to help You find Your way back from where You came from. (Ariadne's thread)

The 3 keys to collect will appear shiny bright green, yellow and red in the maze and their rooms' walls are also enlighted by the same color light.
In the top row (which is the status row) You will see which keys You already have: Dark color keys mean You still need to find these. Bright color means You already have the respective key.
The exit cell will show up light magenta, enlightening the whole room with magenta around it.

The right edge of the screen is some kind of "Item Radar" showing which item is the closest and how far is it measured directly (not following the route) -- giving You a hint which direction the closest feature is.
The color of the bar is the color of the item that is closest, and the length and brightness of the bar hints the distance. (first the bar is dark, going from 0-8, then a bright bar is overlapping it going 0-8).  
Until You don't have all the keys, the radar will only show You the closest key, not taking care about the exit, as You can not exit any way without all 3 keys. When You get all 3 keys the radar will only mind about the exit as having all 3 keys enables You to exit.

In the pygame version pressing the 'A' key will dump the full maze on the terminal as ANSI art.


### Reversi

> Play a Reversi game on the 8x8 LED display against the Computer.


![Screenshot-Reversi](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Reversi.jpg)

For a better visibility on the 8x8 LED display the two players' colors are not black and white but blue and red. _(Black would mean an LED turned off, so the whole playfield should be colored to some neutral gray color, which might sound a generally good idea but imagine the situation if the top 3 rows of the board contain only black tiles then the top part of the screen is completely turned off, looking very stupid)_

Blue is the human player who begins the game, red is the computer player. Human and computer players put their tiles one by one in turns. You have to put a tile onto such a location where you can capture a whole and complete row of opponent's tiles between one of Your existing tiles and the currently put tile. This case the whole row turns into Your color. The row of tiles is considered in any of the 8 directions: up/down/left/right and in the 4 diagonal directions.

In case one player can not put a tile in a turn, the turn is skipped and the opponent player can put the next tile.
The game is over if none of the players can put any new tile _(i.e.: either a deadlock situation or the board is full)_
The winner is who has more tiles at the end of the game. The results are announced on the 8x8 LED display at the end of the game.

**Controls:**

Move the blinking cursor with the stick (stick version) or crsr keys (pygame version), and click (stick version) or press ENTER or SPACE (pygame version) where You would like to put Your tile. Newly put and newly conquered tiles are highlighted with brighter color for a short term, then the colors fade back to the default brightness.
Computer player is flashing the tile couple of times to make human player to see easier where the new tile is put, and similarly, newly conquered tiles are highlighted with bright colors for a short time to see the consequences.

Computer player's algorhythm is half own idea, but also taken lot of inspiration from other Reversi games downloaded from GitHub.


### Mastermind

> The classical Mastermind game on the 8x8 LED display.


![Screenshot-Mastermind](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Mastermind.jpg)

The computer will randomly pick a color out of 6 possible colors (red, yellow, green, cyan, blue, magenta) into each of 4 locations, creating a set of 4 colors (repetition possible). Your goal is to guess the 4 colors correctly, in correct sequence. Try to guess the correct color code with least possible turns.

The computer will give You a hint after each guessing: how many of the guessed colors are a perfect match (correct color on correct location), and how many colors are right (there is such a color within the set of 4, but You guessed it on an incorrect location).
Your guesses will appear on the left half of the screen, the computer's answers on the right half, side by side, for each guess. The guess list is scrollable up and down so that You can view all of Your previous guesses with their results.
Perfect Matches are displayed with bright green pixel, color-only matches with dark purple.

**Note:** The positions of the computer's feed back pixels are not corresponding to the positions of Your guess, so if You see a bright green pixel (perfect match) in the 2^nd^ position of the reply of the computer, it does not mean that the 2^nd^ position of Your guess is the one that matches. Please only consider **the number** of the perfect matches and color-only matches in the computer's reply. _Actually, results are displayed righ-to-left, to keep space between Your guess and computer's reply, number of perfect matches first, then number of color-only matches as second._

**Controls:**

There are two modes of the game: the `View Mode` and the `Enter Mode`
* In the `View Mode` You can scroll the entire Guess list up and down using the stick (stick version) or crsr keys (pygame version). If You are on the top or bottom of the list and want to move further, the top or bottom row of the screen will flash red momentarily to show You that it is the end of the list.
* In the `Enter Mode` You will see a blinking white cursor in the bottom row that You can only move sideways using the stick (stick version) or crsr keys (pygame version). In the first 4 columns You can also press the up/down keys to select between colors for Your guess. If all the 4 colors are picked, move the cursor to the bottom-right corner where You can see a light blue pixel, this is the "Process my guess" button and click on it (stick middle click in the stick version and ENTER/SPACE key in the pygame version). The computer evaluates Your guess in a slow animation, then appends Your guess and results to the guess list. Then You get back to the `View Mode`.

You can switch between `View Mode` and `Enter Mode` simply by middle clicking with the stick (stick version) or pressing ENTER/SPACE key (pygame version) on **anywhere else** than the bottom-right corner, as that is a special location to ask the computer to process Your guess.


### Flood

> Flood the screen with the same color in least possible steps.


![Screenshot-Flood](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Flood.jpg)

Initially You get a screen filled with mixed color pixels and areas. The cursor is blinking in the top-left corner.
You can move freely on the screen with the cursor, and whatever color You click on, it will be copied to the top-left corner pixel and flooded to all sideways-adjacent (4 directions) pixels on the screen with the same color as the top-left one. This means that You should check which color has the most pixels in adjacent contact with the already filled area of the top-left corner and click on this color, to fill the existing area with this new color, therefore causing the already filled area to grow with the most number of pixels.

Later on when the majority of the screen is already filled You should check which color to pick so that all remaining pixels of one color can be fully eliminated in one step rather than more steps, to reduce the number of steps consumed.
When You manage to completely fill the screen with the same color, the number of consumed steps will be displayed on the 8x8 LED display.

**Controls:**

Move the cursor with the stick (stick version) or crsr keys (pygame version) and click on the selected color with the middle button (stick version) or the ENTER/SPACE key (pygame version).


### Inertia

> A not so commonly known game from the sgt-puzzles set.


![Screenshot-Inertia](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Inertia.jpg)

There is a playfield filled with `Gems` to collect (bright green), `Mines` to make You die if You step on them (bright red), `Walls` that will block Your movement to that direction (dark grey), `Stoppers` or `Catchers` if You like, that will absorb Your inertia and halt Your actual motion (dark yellow), and the rest is `normal` playfield with no specific function (dark blue).

The goal is to navigate the player through the playfield and to collect all `Gems` without stepping on any of the `Mines`. Stepping on a Mine is instant death therefore losing the game.

It might sound very easy at first but there is a catch though: If You start moving in any of the 8 directions (sideways and diagonally), then You will keep Your initial inertia and continue moving until You either hit a `Wall`, or reach the `edge` of the screen or step on a `Stopper/Catcher` cell. Your movement will only stop at these locations.

During Your inertial movement You can step on cells with `Gems`, this case You collect the respective Gem but continue moving forward. The cell with the Gem will turn into a regular cell with no specific function. During inertial movement, stepping on a `Mine` will also stop You but not the way You would like to.

_Important:_ After collecting the last Gem the game does not immediately stop, but lets Your inertia to take effect and complete the movement until the first resting cell where You can stop, then the result is evaluated. So it is generally a bad last move to collect the last Gem such a way that there is a Mine behind the Gem, because the game is not interrupted immediately when You step on the cell with the Gem, but You will keep on moving and hit the Mine.

**Controls:**

There is a cursor blinking on the cell with the player, and You can move this cursor maximum 1 cell away from the player to indicate the direction (from 8 possible) You want to start moving.
Move the cursor with the stick (stick version) or crsr keys (pygame version) and click on the selected cell with the middle button (stick version) or the ENTER/SPACE key (pygame version) to start moving.


### Memory

> Classic 4x4 pcs Memory game for the SenseHat display.


![Screenshot-Memory](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Memory.jpg)

There are 2x8 pcs of colorful shapes shuffled around the playfield and Your goal is to find the pairs in least possible steps. A shape is a 2x2 square with light and dark pixels from the same color. All 8 shape pairs will have their unique colors. Revealing of any cell will count as 1 step.

**Controls:**

There is a 2x2 pixel cursor blinking on the screen. Move it around with the SenseHat stick (stick version) or CRSR Keys (pygame version). Click with the stick middle button (stick version) or hit ENTER/SPACE (pygame version) to reveal the cell under the cursor.

If the revealed cell matches the color/shape of the previously revealed cell, then the two cells remain discovered on the screen. If the last revealed cell does not match the previously revealed one, then the previous is concealed again.

_Note:_ Using 2x2 pixel shapes only leaves a 4x4 playfield (8 item pairs) that is quite easy to solve, but gives the opportunity using shapes and having nice distinct colors for the items to memorize.

While using 1x1 pixel items for the game would mean a 8x8 playfield (32 item pairs), although we would lose the shapes, and the only thing to memorize would be _the color_ of the pixel, although generating 32 different colors would also mean that the difference between the colors would be quite minor, creating some confusion when trying to find the matching pairs, so the game would turn unenjoyable.


### 2048

> SenseHat adaptation of the binary geek's 2048 matching game

![Screenshot-2048](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-2048.jpg)

The playfield consists of 4x4 cells (represented by 2x2 LEDs on the SenseHat). Each cell might be empty or contain a number that is a power of 2. In each turn the player has one move to make in any of the four cardinal directions, and all the numbers of the whole playfield get pushed towards that direction until they hit the wall or each other, so they pile up on that wall the player has selected. If two cells with the **same value** hit each other, they are merged into one cell with the value summed up, so `4` + `4` become merged into a single `8`. Therefore the numbers will always remain a certain power of 2. After each move of the player a single `2` number is dropped randomly on one of the empty cells of the playfield.  
The aim of the player is to merge so many cells that the value eventually reaches `2048` _(thus the name of the game)_. To reach this high number a lot of different powers of 2 are required to be present on the playfield simultaneously, turning the playfield quite crowded, blocking the way of further moves, therefore to reach 2048 might be quite challenging.

* If 2048 appears at any location of the playfield, the game is won with no further conditions.
* If the whole playfield gets populated, there are no more empty cells, OR the player pushes `x` or `q` in pygame version or the `stick middle` in stick version, the game is lost/quit, the number of performed turns and the total earned score is displayed on the SenseHat.
	* If the playfield gets full **after** the program drops the last `2`, the game is **not over**, as the player still has the chance to move and merge the numbers, freeing up some cells, where the program can drop further `2`'s.
	* The game **is over** if there are no free cells after the player's move, therefore there is **nowhere** to drop the next `2`.

These are the rules for the standard 2048 game that is being played on a PC display where the program is able to indicate the actual values of the cells. On the SenseHat there are 2x2 pixels available for each cell, so a different method had to be applied.  
The 2x2 pixels show a certain color for each value, although not randomly, but following the hue sequence of the H-S-V color space (the colors of the rainbow), to give a hint which value is higher than the other. Red - Orange - Yellow - Green - Cyan - etc... This seems complex but You can get used to it quite easily, and because of using vivid colors, the SenseHat turns into an eyecandy during gameplay.  
A further aid in determining the value of a cell a hint is given: the four LEDs of a cell represent four bits, the lighter ones mean `1`, the darker ones mean `0`, and these give You a number, that shows which power of 2 the cell represents. The top 2 pixels are 8 and 4 , the bottom 2 pixels are 2 and 1. So for example if the 4 pixels of a cell are: top row: dark - light ; bottom row: light - dark, then this means 0-1-1-0, that is the binary representation of 6, so the cell value is 2^6, that is 64. Although as I said, You'll never start calculating the numbers as the colors are so obvious that You'll focus on merging two oranges into a yellow...

**Hint for values:**

|Power of 2| Value | Color |Bit pattern|
|----------|-------|-------|-----------|
|          |_empty_|  black| _N/A_     |
|        1 |     2 |   gray|   0-0-0-1 |
|        2 |     4 |    red|   0-0-1-0 |
|        3 |     8 | orange|   0-0-1-1 |
|        4 |    16 | yellow|   0-1-0-0 |
|        5 |    32 |  green|   0-1-0-1 |
|        6 |    64 |   cyan|   0-1-1-0 |
|        7 |   128 |   blue|   0-1-1-1 |
|        8 |   256 | purple|   1-0-0-0 |
|        9 |   512 |   pink|   1-0-0-1 |
|       10 |  1024 | l.gray|   1-0-1-0 |
|       11 |  2048 |  white|   1-0-1-1 |


### Four in a Row

> Move colorful pixels to create complete rows of the same color to make all its members disappear.  
> A classic turn-based match-up game that has lots of different variants.

![Screenshot-Four_in_a_Row](https://github.com/oliverbacsi/Sense_Hat_Progs/blob/main/_screenshots/scrot-Four_in_a_Row.jpg)

There are random colored balls (represented by LED pixels in case of the SenseHat) displayed on the screen. In each turn the player has to grab exactly one ball and relocate it to somewhere else on the playfield so that consecutive rows of the same color are formed in any of the 8 directions (the cardinal four and four diagonal directions).  
In case the length of a consecutive row reaches a minimum value (four by default, as the name of the game suggests), the whole consecutive row disappears.  
The grabbed balls can be only moved to those empty locations that are not blocked/obscured by the other balls, so an area completely surrounded by balls is not accessible for other balls being outside, just for those on the inside.  
Preparing more semi-finished rows of balls and completing the rows with one single "intersection" ball will cause that rows in all directions will disappear simultaneously, this is called a "combo" move and will cause extra bonus points for each ball elimintated.  
For each player move when no balls are eliminated, extra random balls are dropped on the playfield as punishment.  
The goal is to keep the game alive for as long as possible. In case the playfield gets filled by the dropped balls and there is no more free space to drop the next set of balls, the game is over, and the total collected score is displayed on the SenseHat.

**Controls:**

Initially You are in `Cruise Mode`. A white blinking cursor can be moved with the crsr keys (pygame version) or the SenseHat Stick (stick version). Clicking on a ball will grab it, and the game is changing to `Grab Mode`. Move around the cursor with the usual keys, and the actual path of the ball's planned move will be always displayed with dark gray color.  
In `Grab Mode` You can either click (middle key in stick version or SPACE or ENTER in pygame version) on an empty location: The ball will move to that location, following the planned path, Your move is considered as done, and You get back to `Cruise Mode`. Clicking on an unaccessible place will not move the grabbed ball and You remain in `Grab Mode`.  
If You want to return to `Cruise Mode` without making a move, go back to the grabbed ball and click on it again. In pygame version You can press 'x' or 'q' to quit the game immediately. Your score will be shown.

**Complexity:**

The complexity of the game can be increased/decreased by adjusting internal variables of the game: The number of different colors used at the same time, the number of similar balls that need to be aligned in line, and the number of new balls dropped on the field in case the move was unsuccessful.  
There is no means of configuring these variables during gameplay, You have to edit them in the source code. Look for the beginning of the **`Game`** class:

```python
class Game :
    def __init__(self) :
        self.NumColor :int =6
        self.FullRow :int =4
        self.InjectBalls :int =3
```

|Variable   |Meaning                                            |Min|**Default**|Max|
|-----------|---------------------------------------------------|---|-----------|---|
|NumColor   |Number of different colors used in the game        | 3 |**6**      | 10|
|FullRow    |Number of consecutive balls to match to remove them| 3 |**4**      | 6 |
|InjectBalls|Number of new balls to be dropped on the playfield | 1 |**3**      | 5 |


---

# TODO:

## DEBUG:


### Reversi game

Experienced a bug: Close to the end of the game most of the game field was already blue (human player), so blue player didn't have a chance to put a tile (the blue question mark appeared correctly), while the red player (computer) had one single possibility to put the tile. But somehow the computer player didn't perform the move, but a red question mark appeared as if the computer player also didn't have the chance the move. Surprisingly the game was not over, so when the program was evaluating the "Game Over" condition, then it saw the possibility for the computer player to move, but when it was the computer player's turn, the algorhythm didn't find the correct move.... Strange...

### SpaceWeather

Time stamp of the last successful data should not be the timestamp of the download itself but of the (oldest?) report timestamp in the data files.

### _sense_hat_ANSI

This is a very lame library to subst the real sense_hat library,
when no Raspberry is around and developing only on PC.



## WRITE AS NEW:

### Compass (gadget)

Display a proper compass utilizing the magnetometer sensor of the Sense Hat.

### Galaga (game)

Sense Hat adaptation of the shoot-them-up arcade game Galaga

### Klotski (game)

Sense Hat adaptation of the Klotski logical board game

### Swell Foop (game)

Sense Hat adaptation of the Swell Foop logical board game

### Tents (game)

Conversion from C++ to Python of one of the sgt-puzzle games Tents.

### Towers (game)

Conversion from C++ to Python of one of the sgt-puzzle games Towers.

### Unruly (game)

Conversion from C++ to Python of one of the sgt-puzzle games Unruly.  
Most of the procedures are already inter-coded, but it needs to be finished yet.

### Zuma (game)

Sense Hat adaptation of the well known DOS/Win ball game Zuma.  
Develop game engine and finish the game.


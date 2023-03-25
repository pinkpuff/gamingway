# Gamingway
A python package for reading and modifying roms of Final Fantasy 4 (2 US) for SNES.
I figure if Namingway changes your name, then Gamingway changes your game :D

## Purpose
The objective of this project is twofold:
1. **Provide a tool for rom hacking whose power extends beyond that of a simple GUI editor.** As a python library, while it is still capable of all the more "simple" tasks like changing a weapon's graphic or a spell's name or something, it is capable of much more complex tasks, such as performing operations on an entire set of data, copying or modifying data between multiple roms, or even creating a full randomizer. It also has built in safeguards that allow it to read most expanded and hacked roms.
2. **Provide documentation for where and how data is stored in the rom.** There is a lot of known information about this already, but I figure by having the documentation all in one place and alongside the code, it may make it both easier to find and easier to understand. As a result, my plan is to include very thorough and detailed comments explaining every step of every procedure.

## Installation
It's not currently in a state where you can simply pip install it like a regular python library but I do plan to implement that down the road.
For now, simply download the files into the folder for whatever project you intend to use it in and import it.
I will work on improving/fixing this as demand arises. For now though, I think I'm the only one using it ^_^;

## Usage
Put this line at the top of your .py file that you want to use it in:
``from gamingway import FF4Rom``

Then to load a rom from within the code, use:
``rom = FF4Rom("example/path/to/rom/ff4.smc")``
Replace ``rom`` in the above with the name of the variable you would like to use to represent the abstract FF4Rom object. Also replace the path in quotation marks with the filesystem path to the rom file you wish to load the information from. You can have multiple roms stored in multiple FF4Rom variables and work with them as needed.

The above merely sets up an association between the variable and the rom file on the filesystem. To actually parse the data from the file into abstract objects that can be manipulated with the gamingway library's functions, use the following:
``rom.read()``
Again, replace ``rom`` with the variable name from the previous step. You can also tell it to read only one specific or general type of data. For example:
``rom.read("spells")``
That will only parse spell data. You can likewise say something like:
``rom.read("magic")``
This will read all data related to magic, which of course includes spells, but would also include things like the characters' spellbooks. If you want to read multiple types of data without reading all types, you can simply call ``read`` multiple times, each with the different types of data you want to read.

The full list of currently implemented data types is as follows:
* ``all`` Reads everything; this is the default if you leave out the parameter.
  * ``magic``
    * ``spells`` Player spells castable in battle. Currently only reads the 6-letter-name ones and does not include "monster abilities" like ColdMist and Reaction and so on.
    * ``spellbooks`` The starting spells and the spells put into each spellbook at each level.
  * ``gear``
    * ``equips`` The tables of which Jobs have which equipment permissions.
    * ``items`` The full list of items, including all weapons, armors, supplies (usable in battle), and tools (unusable in battle).
  * ``party``
    * ``characters`` The starting stats and levelups for each character.
  * ``combat``
    * ``monsters`` The stats for each individual enemy.
  * ``world``
    * ``mapnames`` The list of map names as stored in the rom. For example, when you enter a map and see a blue box at the top saying "B1" or "Cecil's Room" or what have you.
    * ``maps`` The information for each map, such as what tileset it uses, whether it's magnetic, warpable, exitable, etc. Does NOT include the arrangement of tiles except as an index referencing *which* tile arrangement it uses.
    * ``tilemaps`` The list of tile arrangements. 
    * ``overworld`` The tile arrangement for the overworld (upper world).

The reason everything is separated out like this is because I want to make as few assumptions about the input rom as possible in order to facilitate working with hacked and/or expanded roms which may have data in different locations or stored in different ways. If reading and/or writing a certain type of data causes issues, either in the program or in the actual playing of the game, you can omit reading or writing that type of data and it will leave it alone.

From here, you can make whatever changes you want to the rom by manipulating the variables and objects directly. Hopefully the source code is or will be well documented enough that it should be easy to figure out how to achieve whatever your goal is. Before trying to edit a certain type of data make sure you have read/parsed it as outlined above.

After making the desired changes, you can write them back to the rom using:
``rom.write()``
As with the ``read`` function, you can pass a parameter to ``write`` to only write a specific type of data (it uses the same names as listed above).
Note that this does not update the file on the disk; it only updates the bytecode stored in the rom variable.

When you are ready to commit the bytecode of the rom variable to a file on the filesystem, you can use:
``rom.save("example/path/to/new/rom/ff4.smc")``

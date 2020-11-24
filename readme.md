# StarBirght in the Dark

StarBright in the Dark, is the setting for a Traveller Campaign that will start running at some point in the near future. 

## stars.py

This is the backbone file currently for generating the star systems for the Campaign, using Traveller 5.1 system creation rules. 

## Functions

All functions are held within discrete modules in the travtools library

## module dice.py

### dice.sum(n)
roll n dice and return the sum of the values rolled.

### dice.flux()
roll flux dice. ie. 1d6 - 1d6

## module converters.py

### ext.hex(n)
takes a number and turns it into extended hex. 

### ext.dec(n)
takes and extended hex number and turns it back into its decimal equivalent.

## module system.py

### fun_uwp(n)
takes number n as a seed and generates a uwp for the planet. using the same value for n will generate the same uwp every time. 

### fun_trade(n)
taking a uwp as it's argument, this function for computing trade codes -- Not complete

### fun_ext(n)
takes a uwp and calculates the extended profile, to generate Ix, Ex & Cx

### fun_pbg(uwp)
takes a uwp and determines the population digit, the asteroid belts and gas giant number for the system.

## module stars.py

holds the code for generating the star locations, spherical generation.


## To Do

* Check Seed value generation for world placement
* update and finish writing various modules.
* Make plotly files available online.
* ...

# StarBirght in the Dark

StarBright in the Dark, is the setting for a Traveller Campaign that will start running at some point in the near future. 

## Functions

All functions are held within discrete modules in the travtools library

## module dice.py

### dice(n)
This fucntion rolls n dice and return the sum of the values rolled.

### flux()
This function rolls flux dice. ie. 1d6 - 1d6

### die_roll()
This function rolls 1d6.

## module converters.py

### ext_hex(n)
This function takes a number and turns it into extended hex. 

### ext_dec(n)
This function takes an extended hex number and turns it back into its decimal equivalent.

### neg_ehex(n, d)
This function takes a number (n) and turns it either: d=F - forward, or d=B - Backwards; into negative extended hex used by QREBS.

## module qrebs.py

### qrebs(n)
This function takes a variable n as the seed and generates a QREBS for an item, returning the full QREBS as well as it's description.

## module system.py

### fun_uwp(n)
takes number n as a seed and generates a uwp for the planet. using the same value for n will generate the same uwp every time. 

### fun_pbg(uwp)
takes a uwp and determines the population digit, the asteroid belts and gas giant number for the system.

### fun_trade(n)
taking a uwp as it's argument, this function for computing trade codes -- Not complete

### fun_ext(n)
takes a uwp and calculates the extended profile, to generate Ix, Ex & Cx

### fun_bases(uwp)
takes a uwp and sees whether there are naval or scout bases present.

## module stars.py

This code has 2 Classes Points & Points2D these are used to generate random points to act as placeholder for planetary systems. Each point is spread in 3d space or 2d space by providing the class with a number of points, a radius, a center point (x,y,z for Points and x,y for Points2D), a minimum distance between points, and a maximum number of itterations to find the points and make them fit. 


## To Do

* write more utility modules
* add more functionality
* other sutff...

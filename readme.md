# StarBirght in the Dark

StarBright in the Dark, is the setting for a Traveller Campaign that I am running. I created a whole pile of libraries and functions to help my life as GM be a little easier.

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

### qrebs(n, l)
This function takes a variable n as the seed and generates a QREBS for an item, if l = 1 it will return the full QREBS as well as it's description, otherwise if l = 0 (default) it will return the shorterned 5 digit code.

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

## module commerce.py

### spec_price(n,t)
Generate base cost of speculative cargo for a given set of trade codes n, with tech level t.

### trade_goods(n)
Generate a random Trade good type given a list of trade codes n.

### sell_price(n,d,b = 0, t = 0)

takes arguments of a Cargo Code (n) in the format: E - Hi In Na Va Cr3,400, Brokers Skill default is 0, no broker (b), Any Trader Roll default to 0, no trader (t) and Destination UWP (d) in the format A430311-B, it returns the sell price of the goods, taking brokering into account.

### trade_gds(n, skill = {'Steward':0, 'Admin':0, 'Streetwise':0, 'Liaison':0}, days = 7):

generate trade goods for a given UWP in the format A430311-B. Using skills, skill, where skill is {Steward, Admin, Streetwise, Liaison} defaults = 0, for a given number of days default = 7.

## module stars.py

This code has 2 Classes Points & Points2D these are used to generate random points to act as placeholder for planetary systems. Each point is spread in 3d space or 2d space by providing the class with a number of points, a radius, a center point (x,y,z for Points and x,y for Points2D), a minimum distance between points, and a maximum number of itterations to find the points and make them fit. 


## To Do

* write more utility modules
* add more functionality
* other sutff...

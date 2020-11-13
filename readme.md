# StarBirght in the Dark

StarBright in the Dark, is the setting for a Traveller Campaign that will start running at some point in the near future. 

##stars.R

This is the backbone file currently for generating the star systems for the Campaign. 

##Functions within the code

###dice.sum(n)
roll n dice and return the sum of the values rolled.

###dice.flux()
roll flux dice. ie. 1d6 - 1d6

###ext.hex(n)
takes a number and turns it into extended hex. 

###ext.dec(n)
takes and extended hex number and turns it back into its decimal equivalent.

###fun_uwp(n)
takes number n as a seed and generates a uwp for the planet. using the same value for n will generate the same uwp every time. 

###fun_trade(n)
taking a uwp as it's argument, this function for computing trade codes -- Not complete

###fun_ext(n)
takes a uwp and calculates the extended profile, to generate Ix, Ex & Cx

###rand.sep(n, x0, x1, y0, y1, z0, z1, d, test = 1000)
n - number of systems to generate
x0, x1 - extent of x co-ordinates
y0, y2 - extent of y co-ordinates
z0, z1 - extent of z co-ordinates
d - minimum distance between points
test - number of tests to run, default 1000. 
generate the planetary ssytems.
library(tidyverse)
library(plotly)

#Random number generator : sample(1:6, n, replace = TRUE)
#function allows for rolling of multiple dice
dice.sum <- function(n.dice){
  dice <- sample(1:6, size = n.dice, replace = TRUE)
  return(sum(dice))
}

dice.flux <- function() {
  return(dice.sum(1) - dice.sum(1))
}

ext.hex <- function(n) {
  if (n < 16) {
    return (sprintf("%X", n))
  } else if (n == 16) {
    return ("G")
  } else if (n == 17) {
    return ("H")
  } else if (n == 18) {
    return ("J")
  } else if (n == 19) {
    return ("K")
  } else if (n == 20) {
    return ("L")
  }
}

ext.dec <- function(n) {
  if(!is.na(strtoi(n))) {
    return (strtoi(n))
  } else {
    return (switch(n, A = 10, B = 11, C = 12, D = 13, E = 14, F = 15, G = 16, H = 17, J = 18, K = 19, L = 20))
  }
}

fun_uwp <- function(n) {
  set.seed(1000 + n)
  stprt <- dice.sum(2)
  sprt <- switch(stprt, "A", "A", "A", "A", "B", "B", "C", "C", "D", "E", "E", "X")
  sze <- dice.sum(2) - 2
  if (sze < 0) {
    sze <- 0
  } else if (sze == 10) {
    sze <- dice.sum(1) + 9
  } 
  atm <- dice.flux() + sze
  if (sze == 0) {
    atm <- 0
  } 
  if (atm < 0) {
    atm <- 0
  } else if (atm > 15) {
    atm <- 15
  }
  hyd <- dice.flux() + atm
  if (sze < 2) {
    hyd <- 0
  } else if (atm < 2 || atm > 9) {
    hyd <- hyd - 4
  }
  if (hyd < 0) {
    hyd <- 0
  } else if (hyd > 10) {
    hyd <- 10
  }
  pop <- dice.sum(2) - 2
  if(pop == 10) {
    pop <- dice.sum(2) + 3
  }
  gov <- dice.flux() + pop
  if(gov < 0) {
    gov <- 0
  } else  if (gov > 15) {
    gov <- 15
  }
  law <- dice.flux() + gov
  if (law < 0){
    law <- 0
  } else if (law > 18) {
    law <- 18
  }
  law <- ext.hex(law)
  #print(sprintf("%s%X%X%X%X%X%s", sprt, sze, atm, hyd, pop, gov, law))
  tech <- dice.sum(1)
  #starport factor
  tech <- tech + switch(sprt, A = 6, B = 4, C = 2, D = 0, E = 0, X = -4)
  #size factor
  tech <- tech + switch(sze, 1, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  #atmo factor
  tech <- tech + switch(atm, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1)
  #hydro factor
  tech <- tech + switch(hyd, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2)
  # if (hyd == 9) {
  #   tech <- tech + 1
  # } else if (hyd == 10) {
  #   tech <- tech + 2
  # }
  #pop factor
  tech <- tech + switch(pop, 1, 1, 1, 1, 1, 0, 0, 0, 2, 4, 4 ,4, 4, 4, 4)
  # if (pop > 9) {
  #   tech <- tech + 4
  # } else  if (pop == 9) {
  #   tech <- tech + 2
  # } else if (pop < 6) {
  #   tech <- tech + 1
  # }
  #gov factor
  if (gov == 0 || gov == 5) {
    tech <- tech + 1
  } else if (gov == 13) {
    tech <- tech + 2
  }
  #print(tech)
  if(identical(tech, numeric(0))) { 
    tech <- 1
  }
  if (tech < 0){
    tech <- 0
  }
  return (sprintf("%s%X%X%X%X%X%s-%s", sprt, sze, atm, hyd, pop, gov, law, ext.hex(tech)))
}

fun_trade <- function (n) {
  siz <- ext.dec(str_sub(n, 2, 2))
  atm <- ext.dec(str_sub(n, 3, 3))
  hyd <- ext.dec(str_sub(n, 4, 4))
  pop <- ext.dec(str_sub(n, 5, 5))
  gov <- ext.dec(str_sub(n, 6, 6))
  law <- ext.dec(str_sub(n, 7, 7))
  cat("UWP: ", n, "\nSize: ", siz, "| Atmo: ", atm, "| Hydro: ", hyd, "| Pop: ", pop, "| Gov: ", gov, "| Law: ", law, "\n")
  #Ag - Atm 5-9, Hyd 4-8, Pop 5-7
  #As - Siz 0, Atm 0, Hyd 0
  #Ba - Pop 0, Gov 0, Law 0
  #De - Atm 2-9, Hydro 0
  #Fl - Atm 10-12, Hydro 1-10
  #Hi - Pop 9-15
  #Ic - Atm 0,1, Hydro 1-10
  #In - Atm 0-4,7,9,10-12, Pop: 9-15
  #Lo - Pop 1-3
  #Na - Atm 0-3, Hydo 0-3, Pop: 6-15
  #Ni - Pop 4-6
  #Po - Atm 2-5, Hydro 0-3
  #Ri - Atm 6,8, Pop 6-8
  #Va - Atm 0
}
#Extended Profile {Ix} (Ex) [Cx]
#Importance (Ix)
#Starport Type A or B +1
#Starport D or worse -1
#Tech Level G or more +1
#Tech Level A or more +1
#Tech Level 8 or less -1
#Per Ag Hi In Ri +1
#If Pop 6 or less -1
#If Naval AND Scout Base +1
#If Way Station +1
#Important= +4 or greater.
#Unimportant= 0 or less.
#Economic (Ex)
#(RLI+E)
#R - Resources - 2D (if tech 8+, then +Gas Giants +Asteroid Belts)
#L - Labour - Pop - 1
#I - Infrastructure - Pop 0 = 0, Pop 1-3 = Ix, Pop 4-6 = 1D + Ix, Pop 7+ = 2D + Ix
#E - Efficiency - Flux
#Cultrual (Cx)
fun_ext <- function(n){
  sport <- str_sub(n, 1, 1)
  tech <- ext.dec(str_sub(n, 9, 9))
  sx <- switch(sport, A = 1, B = 1, C = 0, D = -1, E = -1, X = -1)
  tx <- 0
  if (tech > 15) {
    tx <- tx + 1
  } else if (tech > 10) {
    tx <- tx + 1
  } else  if (tech < 9) {
    tx <- tx - 1
  }
  ix <- sx + tx
  return (ix)
}

rand.sep <- function(n, x0, x1, y0, y1, z0, z1, d, seed = 256, test = 1000) {
  set.seed(seed)
  for (i in 1:test) {
    nums <- cbind(round(runif(n, x0, x1),2), round(runif(n, y0, y1),2), round(runif(n, z0, z1),2))
    #if (min(dist(nums)) >= d || max(dist(nums)) <= 6) {
    if (min(dist(nums)) < d) {
      return(nums)
    }
  }
  return(NA) #failed
}

# StarID: The database primary key from a larger "master database" of stars.
# HD: The star's ID in the Henry Draper catalog, if known.
# HR: The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.
# Gliese: The star's ID in the third edition of the Gliese Catalog of Nearby Stars.
# BayerFlamsteed: The Bayer / Flamsteed
# designation, from the Fifth Edition of the Yale Bright Star Catalog. This is a combination of the two designations. The Flamsteed number, if present, is given first; then a three-letter abbreviation for the Bayer Greek letter; the Bayer superscript number, if present; and finally, the three-letter constellation abbreviation. Thus Alpha Andromedae has the field value "21Alp And", and Kappa1 Sculptoris (no Flamsteed number) has "Kap1Scl".
# RA, Dec: The star's right ascension and declination, for epoch 2000.0. Stars present only in the Gliese Catalog, which uses 1950.0 coordinates, have had these coordinates precessed to 2000.
# ProperName: A common name for the star, such as "Barnard's Star" or "Sirius". I have taken these names primarily from the Hipparcos project's web site, which lists representative names for the 150 brightest stars and many of the 150 closest stars. I have added a few names to this list. Most of the additions are designations from catalogs mostly now forgotten (e.g., Lalande, Groombridge, and Gould ["G."]) except for certain nearby stars which are still best known by these designations.
# Distance: The star's distance in parsecs, the most common unit in astrometry. To convert parsecs to light years, multiply by 3.262. A value of 10000000 indicates missing or dubious (e.g., negative) parallax data in Hipparcos.
# Mag: The star's apparent visual magnitude.
# AbsMag: The star's absolute visual magnitude (its apparent magnitude from a distance of 10 parsecs).
# Spectrum: The star's spectral type, if known.
# ColorIndex: The star's color index (blue magnitude - visual magnitude), where known.
# * X,Y,Z: The Cartesian coordinates of the star, in a system based on the equatorial coordinates as seen from Earth. +X is in the direction of the vernal equinox (at epoch 2000), +Z towards the north celestial pole, and +Y in the direction of R.A. 6 hours, declination 0 degrees.
# * VX,VY,VZ: The Cartesian velocity components of the star, in the same coordinate system described immediately above. They are determined from the proper motion and the radial velocity (when known). The velocity unit is parsecs per year; these are small values (around 10-5 to 10-6), but they enormously simplify calculations using parsecs as base units for celestial mapping.

#stars <- read_csv('./code/hygdata_v3.csv')
#systems <- stars %>% 
#    select(id, proper, dist, spect, x, y, z)

# systems <- rand.sep(3000, -12, 12, -12, 12, -12, 12, 1)
# systems <- as.data.frame(systems)

#Generate quadrants
omega <- rand.sep(500, -5, 5, -5, 5, -5, 5, 1,500)
alpha <- rand.sep(350, 5, 15, -5, 5, -5, 5, 1,350)
beta <- rand.sep(350, -15, -5, -5, 5, -5, 5, 1,375)
gamma <- rand.sep(250, -5, 5, 5, 15, -5, 5, 1,250)
delta <- rand.sep(250, -5, 5, -15, -5, -5, 5, 1,275)
epsilon <- rand.sep(350, -5, 5, -5, 5, 5, 15, 1,365)
zeta <- rand.sep(350, -5, 5, -5, 5, -15, -5, 1,355)
#dist matrix for each
om_dist <- dist(omega)
al_dist <- dist(alpha)
be_dist <- dist(beta)
ga_dist <- dist(gamma)
de_dist <- dist(delta)
ep_dist <- dist(epsilon)
ze_dist <- dist(zeta)
# add id and convert to dataframes
omega <- as.data.frame(omega)
omega <- omega %>% rowid_to_column("id")
colnames(omega) <- c("id", "x", "y", "z")
alpha <- as.data.frame(alpha)
alpha <- alpha %>% rowid_to_column("id")
colnames(alpha) <- c("id", "x", "y", "z")

# this works (below)
omega$uwp <- sapply((omega$id+145), fun_uwp)
alpha$uwp <- sapply((alpha$id+541), fun_uwp)


omega <- omega %>% 
  mutate(uwp = as.character(uwp)) %>% 
  mutate(sport = str_sub(uwp, 1, 1))
alpha <- alpha %>%
  mutate(uwp = as.character(uwp)) %>% 
  mutate(sport = str_sub(uwp, 1, 1))

# sys50 <- systems %>%
#     filter(dist < 50) %>%
#     arrange(dist) 

# sys25 <- systems %>% # systems within 25 pcs
#     filter(dist < 25) %>%
#     arrange(dist) 

# all25 <- plot_ly(sys25, x = ~x, y = ~y, z = ~z, color = ~sport, size = I(5), text = ~uwp, hovertemplate = paste("UWP: %{text}", "<extra></extra>"))
# all50 <- plot_ly(sys50, x = ~x, y = ~y, z = ~z, size = I(5))
omega_3d_map <- plot_ly(omega, x = ~x, y = ~y, z = ~z, color = ~sport, size = I(5), text = ~uwp, hovertemplate = paste("UWP: %{text}", "<extra></extra>"))
omega_sport_dist <- ggplot(omega, aes(x = str_sub(uwp, 1, 1))) + geom_bar()
omega_size_dist <- ggplot(omega, aes(x = str_sub(uwp, 2, 2))) + geom_bar()
omega_atm_dist <- ggplot(omega, aes(x = str_sub(uwp, 3, 3))) + geom_bar()
omega_hydo_dist <- ggplot(omega, aes(x = str_sub(uwp, 4, 4))) + geom_bar()
omega_pop_dist <- ggplot(omega, aes(x = str_sub(uwp, 5, 5))) + geom_bar()
omega_gov_dist <- ggplot(omega, aes(x = str_sub(uwp, 6, 6))) + geom_bar()
omega_law_dist <- ggplot(omega, aes(x = str_sub(uwp, 7, 7))) + geom_bar()
omega_tech_dist <- ggplot(omega, aes(x = str_sub(uwp, 9, 9))) + geom_bar()
alpha_3d_map <- plot_ly(alpha, x = ~x, y = ~y, z = ~z, color = ~sport, size = I(8), text = ~uwp, hovertemplate = paste("UWP: %{text}", "<extra></extra>"))
alpha_sport_dist <- ggplot(alpha, aes(x = str_sub(uwp, 1, 1))) + geom_bar()
alpha_size_dist <- ggplot(alpha, aes(x = str_sub(uwp, 2, 2))) + geom_bar()
alpha_atm_dist <- ggplot(alpha, aes(x = str_sub(uwp, 3, 3))) + geom_bar()
alpha_hydo_dist <- ggplot(alpha, aes(x = str_sub(uwp, 4, 4))) + geom_bar()
alpha_pop_dist <- ggplot(alpha, aes(x = str_sub(uwp, 5, 5))) + geom_bar()
alpha_gov_dist <- ggplot(alpha, aes(x = str_sub(uwp, 6, 6))) + geom_bar()
alpha_law_dist <- ggplot(alpha, aes(x = str_sub(uwp, 7, 7))) + geom_bar()
alpha_tech_dist <- ggplot(alpha, aes(x = str_sub(uwp, 9, 9))) + geom_bar()

library(ggpubr)
fig_omega <- ggarrange( omega_sport_dist, omega_size_dist, omega_atm_dist, 
                omega_hydo_dist, omega_pop_dist, omega_gov_dist, omega_law_dist, omega_tech_dist,
                labels = c( "Starport", "Size", "Atmosphere", "Hydro", "Population", "Government", "Law", "Tech"),
                ncol = 3, nrow = 3)
fig_alpha <- ggarrange( alpha_sport_dist, alpha_size_dist, alpha_atm_dist, 
                alpha_hydo_dist, alpha_pop_dist, alpha_gov_dist, alpha_law_dist, alpha_tech_dist,
                labels = c( "Starport", "Size", "Atmosphere", "Hydro", "Population", "Government", "Law", "Tech"),
                ncol = 3, nrow = 3)
ggsave("omega_distribution.png", fig_omega, width = 10, height = 10, units = "cm", dpi = 300)
ggsave("alpha_distribution.png", fig_alpha, width = 10, height = 10, units = "cm", dpi = 300)


## simulation of 1,000,000 systems to check distsribution
sim <- c(1:1000000)
sim <- as.data.frame(sim)
colnames(sim) <- c("id")
sim$uwp <- sapply((sim$id+123456), fun_uwp)
sim <- sim %>% 
  mutate(uwp = as.character(uwp)) %>%
  mutate(sport = str_sub(uwp, 1, 1))
sim$sport <- as.factor(sim$sport)
summary(sim)
sim_sport_dist <- ggplot(sim, aes(x = str_sub(uwp, 1, 1))) + geom_bar()
sim_size_dist <- ggplot(sim, aes(x = str_sub(uwp, 2, 2))) + geom_bar()
sim_atm_dist <- ggplot(sim, aes(x = str_sub(uwp, 3, 3))) + geom_bar()
sim_hydo_dist <- ggplot(sim, aes(x = str_sub(uwp, 4, 4))) + geom_bar()
sim_pop_dist <- ggplot(sim, aes(x = str_sub(uwp, 5, 5))) + geom_bar()
sim_gov_dist <- ggplot(sim, aes(x = str_sub(uwp, 6, 6))) + geom_bar()
sim_law_dist <- ggplot(sim, aes(x = str_sub(uwp, 7, 7))) + geom_bar()
sim_tech_dist <- ggplot(sim, aes(x = str_sub(uwp, 9, 9))) + geom_bar()
fig_sim <- ggarrange( sim_sport_dist, sim_size_dist, sim_atm_dist, 
                sim_hydo_dist, sim_pop_dist, sim_gov_dist, sim_law_dist, sim_tech_dist,
                labels = c( "S'prt", "Sze", "Atm", "Hyd", "Pop", "Gov", "Law", "Tech"),
                ncol = 3, nrow = 3)
fig_sim
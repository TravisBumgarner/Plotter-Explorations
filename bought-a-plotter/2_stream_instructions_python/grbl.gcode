G21 ; Set units to MM
G90 ; Set absolute units
F10000 ; Set Feed rate, trial and error led to F10_000 being a good number
M3 S0 ; Move print head up
G4 P0.25 ; Wait 0.25s. This seems like a good thing to append to all move/up down commands as it seems the plotter starts doing the next instruction before the current one ends.
M3 S1000 ; Move print head down
G4 P0.25 ; Wait 0.25s. This seems like a good thing to append to all move/up down commands as it seems the plotter starts doing the next instruction before the current one ends.

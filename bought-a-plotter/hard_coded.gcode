G21 ; Set units to MM
G90 ; Set absolute units
F10000 ; Set Feed rate, trial and error led to F10_000 being a good number
M3 S0 ; Move print head up
G4 P0.25 ; Wait 0.25s. This seems like a good thing to append to all move/up down commands as it seems the plotter starts doing the next instruction before the current one ends.

G0 X0 Y0 ; Go to the origin. Still need to figure out how to set this.
G0 X100 Y100 ; Go roughly to the center. Plotter is maxed at X280 Y200

M3 S1000 ; Move print head down
G4 P0.25

G1 X120 Y100 ; Move absolutely to X120 Y100
G1 X120 Y120
G1 X100 Y120
G1 X100 Y100
G1 X120 Y120

M3 S0
G4 P0.25

G1 X100 Y120

M3 S1000
G4 P0.25

G1 X120 Y100

M3 S0
G4 P0.25

G0 X0 Y0


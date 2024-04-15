# Nbody-Simulation
![ Alt text](https://github.com/Andrewnolan13/Nbody-Simulation/blob/main/output_gif.gif)

# An Nbody simulator made possible thanks to taichi-lang.
### Option to export animations as mp4 and gif. 

This project was born out of boredom on a long car journey. I posted here because I thought the animations were cool and would like feedback. It's nothing special but shows the power of the taichi library. 

Nbody initialises particles in space. If the only arg given is num_planets, then initial conditions are randomized. If partial arguments are given, the complement are randomized.
The Cluster class can be used to make custom clusters of particles orbiting(maybe) a mass in space.

For a given particle, the only forces present are gravitaional forces exerted by other particles. If two particles collide, momentum is conserved(I think) and they merge to form a larger particle.
The radius of each particle is proportional to the cube of the mass.

Older versions were made using pygame but could only handle about 500 particles. Now, thanks to taichi-lang, it can comfortably handle 10,000 particles (provided the resolution is reasonable).
There is probably alot more room for improvement and I would be very grateful for any feedback.
read more about taichi here https://github.com/taichi-dev/taichi

** Doesn't work on python 3.12 yet. 

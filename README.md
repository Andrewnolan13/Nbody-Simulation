# Nbody-Simulation
![ Alt text]([galaxy collision. gif](https://github.com/Andrewnolan13/Nbody-Simulation/blob/main/output_gif.gif))

I'm partial to a bitta physics.

An Nbody simulator made possible thanks to taichi-lang. Option to export animations as mp4 and gif. 

Custom initialization of particles in space. Can be fully randomized or fully specified. 

For a given particle, the only forces present are gravitaional forces exerted by other particles. If two particles collide, momentum is conserved and they merge to form a bigger planet.

Older versions were made using pygame but could only handle about 500 particles. Now, thanks to taichi-lang, it can comfortably handle 10,000 particles (provided the resolution isn't huge).

There is probably alot more room for improvement and I welcome all suggestions.

read more about taichi here https://github.com/taichi-dev/taichi

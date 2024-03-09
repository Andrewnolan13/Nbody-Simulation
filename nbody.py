import numpy as np
import taichi as ti
import os
from moviepy.editor import ImageSequenceClip


class NBody:
    def __init__(self, num_planets = 2, width = 1600, height = 900,dt = 1,initial_conditions:dict = None):
        if initial_conditions is not None:
            positions = initial_conditions['Positions'] if 'Positions' in initial_conditions else np.random.rand(num_planets,2)*np.array([width,height])
            masses = initial_conditions['Masses'] if 'Masses' in initial_conditions else np.random.rand(num_planets)*1e10
            radii = initial_conditions['Radii'] if 'Radii' in initial_conditions else np.random.rand(num_planets)*5
            velocities = initial_conditions['Velocities'] if 'Velocities' in initial_conditions else np.zeros((num_planets,2))
        else:
            positions = np.random.rand(num_planets,2)*np.array([width,height])
            masses = np.random.rand(num_planets)*1e10
            radii = np.random.rand(num_planets)*5
            velocities = np.zeros_like(positions)

        positions = positions.astype(np.float32)
        masses = masses.astype(np.float32)
        radii = radii.astype(np.float32)
        velocities = velocities.astype(np.float32)

        self.num_planets = num_planets
        self.width = width
        self.height = height
        self.dt = dt
        self.initial_conditions = initial_conditions
        self.G = 6.67430e-11

        # Init environment
        ti.init(arch=ti.cpu)
        ## constants
        G = 6.67430e-11 # m^3 kg^-1 s^-2
        
        # Fields
        self.Positions = ti.Vector.field(2, dtype=ti.f32, shape=num_planets)
        self.Masses = ti.field(dtype=ti.f32, shape=num_planets)
        self.Radii = ti.field(dtype=ti.f32, shape=num_planets)
        self.Velocities = ti.Vector.field(2, dtype=ti.f32, shape=num_planets)
        self.Forces = ti.Vector.field(2, dtype=ti.f32, shape=num_planets)

        # Init Fields
        self.Positions.from_numpy(positions)
        self.Masses.from_numpy(masses)
        self.Radii.from_numpy(radii)
        self.Velocities.from_numpy(velocities)    
        self.Forces.fill([0,0])
        
        #Bells and whistles
        self.save_path = None
        self.passes = 0

    def forward(self,func = None):
        if self.passes == 0:
            @ti.kernel
            def forward_ti(num_planets:ti.i32):
                for i in range(num_planets):
                    self.Forces[i] = ti.Vector([0,0])
                    for j in range(num_planets):
                        if i != j and self.Masses[j] != 0 and self.Masses[i] != 0: # is there a way to sort the fields so that we don't have to check for 0 mass?
                            r = self.Positions[j] - self.Positions[i]
                            r_norm = r.norm(1e-5)
                            f = self.G * self.Masses[i] * self.Masses[j] / r_norm**2
                            
                            if self.Radii[i] + self.Radii[j] <= r_norm:
                                self.Forces[i] += f * r.normalized()
                            elif self.Masses[i] != 0:
                                self.Velocities[i] = (self.Masses[i]*self.Velocities[i] + self.Masses[j]*self.Velocities[j]) / (self.Masses[i]+self.Masses[j])
                                self.Positions[i] = (self.Masses[i]*self.Positions[i] + self.Masses[j]*self.Positions[j]) / (self.Masses[i]+self.Masses[j])
                                self.Masses[i] += self.Masses[j]
                                self.Radii[i] = (self.Radii[i]**3 + self.Radii[j]**3)**(1/3)

                                self.Masses[j] = 0
                                self.Radii[j] = 0
                            
                    self.Velocities[i] += self.Forces[i] * self.dt /self.Masses[i] if self.Masses[i] != 0 else [0,0]
                    self.Positions[i] += self.Velocities[i] * self.dt + 0.5 * (self.Forces[i] * self.dt /self.Masses[i] if self.Masses[i] != 0 else [0,0]) * self.dt**2
            self.passes += 1
            func = forward_ti
        func(self.num_planets)
        return func
    
    def render(self,gui):
        np_pos = self.Positions.to_numpy()
        np_pos[:,0] /= self.width
        np_pos[:,1] /= self.height
        gui.circles(pos = np_pos, radius=self.Radii.to_numpy())
        gui.show(self.save_path)
    
    def run(self,max_frames=np.inf,save_dir=None):
        if save_dir is not None:
            if not os.path.exists(save_dir):
                raise ValueError(f"{save_dir} doesn't exist. Please create the directory first.")
            elif os.listdir(save_dir) != []:
                ctu = True if input(f"{save_dir} is not empty. This will overwrite any existing pngs. Continue? (YES!/Other)") == 'YES!' else False
                if not ctu: raise ValueError(f"Animation escaped. Please choose another directory.")

        gui = ti.GUI("N-body simulation", (self.width, self.height))
        frame = 0
        func = None
        while gui.running and not gui.get_event(gui.ESCAPE) and frame < max_frames:
            func = self.forward(func)
            self.save_path = f'{save_dir}\\{frame:010d}.png' if save_dir is not None else None
            self.render(gui)
            print(frame,end = '\r')
            frame+=1
    
    def create_animation(self,fps = 30):
        if self.save_path is None:
            raise ValueError("No frames to animate. Please run the simulation first specifying a save_dir.\n >>> Nbody.run(save_dir = 'directory\\to\\save\\images' )")
        
        directory = '\\'.join(self.save_path.split('\\')[:-1])
        print(directory)
        image_files = sorted([f'{directory}\\{file}' for file in os.listdir(directory) if file.endswith('.png')])
        clip = ImageSequenceClip(image_files, fps=fps)

        # Write the video file
        output_file = f'{directory}\\output_gif.gif'
        clip.to_gif(output_file,fps = fps)
        clip.write_videofile(output_file.replace('gif','mp4'), codec='libx264', fps=fps)
    
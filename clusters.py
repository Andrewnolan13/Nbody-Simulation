import numpy as np

class Cluster:
    def __init__(self,centre,centre_mass,centre_velocity = np.array([0,0])):
        self.positions = []
        self.masses = []
        self.velocities = []

        self.centre = centre	
        self.centre_mass = centre_mass
        self.centre_velocity = centre_velocity
        self.num_planets = 1

    def add_belt(self, number, avg_mass,distance_from_centre, std_dev, avg_velocity,velocity_std_dev = 0.1):
        positions = np.array([self.centre+ (distance_from_centre + std_dev * np.random.randn()) * np.array([np.cos(t), np.sin(t)]) for t in np.linspace(0, 8 * np.pi, number)])
        masses = np.random.rand(number) * avg_mass
        velocities = self.centre_velocity+np.array([(avg_velocity + velocity_std_dev*np.random.rand()) * np.array([-np.sin(t), np.cos(t)]) for t in np.linspace(0, 8 * np.pi, number)])
        
        self.positions.append(positions)
        self.masses.append(masses)
        self.velocities.append(velocities)

        self.num_planets += number
        
    def generate_data(self):
        all_positions = np.vstack(self.positions)
        all_masses = np.hstack(self.masses)
        all_velocities = np.vstack(self.velocities)

        positions = np.vstack([self.centre, all_positions])
        masses = np.hstack([self.centre_mass, all_masses])
        radii = np.array([_ ** (1 / 3) / 1000 for _ in masses])
        velocities = np.vstack([self.centre_velocity, all_velocities])

        self.num_planets = len(positions)

        res = {
                                'Positions':positions,
                                'Masses':masses,
                                'Radii':radii,
                                'Velocities':velocities
                            }
        
        self.center_of_mass = np.sum(positions*masses[:,None],axis=0)/np.sum(masses)
        self.total_mass = np.sum(masses)

        return res

    def stack_dictionaries(self,dicts:list[dict])->dict:
        keys = dicts[0].keys()
        res = {}
        for key in keys:
            if key in ['Positions','Velocities']:res[key] = np.vstack([_dict[key] for _dict in dicts])
            else:res[key] = np.hstack([_dict[key] for _dict in dicts])
        return res
    
    def __add__(self,other):
        new = Cluster(self.centre,0)
        this_data = self.generate_data()
        other_data = other.generate_data()
        new_data = self.stack_dictionaries([this_data,other_data]) 
        
        new.positions = [new_data['Positions']]
        new.masses = [new_data['Masses']]
        new.velocities = [new_data['Velocities']]
        new.num_planets = len(new_data['Masses'])+1
        new.center_of_mass = np.sum(new_data['Positions']*new_data['Masses'][:,None],axis=0)/np.sum(new_data['Masses'])
        new.total_mass = np.sum(new_data['Masses'])

        return new
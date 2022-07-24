import random
import numpy as np
from re import L
from .lbforaging_sim import LBFSimulator
from .lbforaging_sim import Particle
from LBF.env.lbforaging.foraging.environment_adhoc import ForagingEnv, Player


config = {
    field_shape: (8,8),
    max_food : 4,
    player_types: ['H1', 'H2', 'H3', 'H4'], 
    max_player_level: 3, 
    player_num: 3
}

class PFilter:
    def __init__(self,simulator, config):
        self.sim = simulator
        self.particle_bank = None
        self.bank_max = 100 # number of particles at one time
        self.type_bank = []
        self.config = config
    
    """
    There are 4 main steps
        1) generate particles, 
        2) simulate particles with previous action
        3) compare outcomes with previous action
        4) filter beliefs
    """

    def generate_particles(self, obs):
        # if particles exist, generate new particles based on old ones
        # if not, generate new particles based on most recent observation
        if len(self.particle_bank == 0):
            self.__generate_all_from_observation(obs)
        else:
            while len(self.particle_bank) < self.bank_max:
                if random.uniform() > 0.5:
                    p = random.choice(self.particle_bank)
                    p_new = self.__perturb_particle(p)
                    self.particle_bank.append(p_new)
                else:
                    p = self.__generate_new_from_observation(obs)

            

    def simulate_and_prune_particles(self, action, observation, reward):
        # combined for efficiency --- single loop rather than double.
        
        pass
    
    def __generate_new_from_observation(self, obs):
        # make field
        p = Particle()
        p.from_observations(obs)
        return p
        # make players
        # copy over step_count and game_over

    def __generate_all_from_observation(self, obs):
        while len(self.particle_bank) < self.bank_max:
            self.particle_bank.append(self.__generate_new_from_observation(obs))
        if self.verbose:
            print('particles initialized based on first observation')
        

    def _evaluate_particle(self, action, observation, reward, particle):
        # compare single particle
        # config simulator
        # step simulator
        # if observations don't match, throw out. 
        pass

    def __compare_observation(ob_trial, ob_gt, r_trial, r_gt):
        # if return true if observations match sufficiently
        # false otherwise
        pass
import numpy
import pickle
from LBF.env.lbforaging.foraging.environment_adhoc import ForagingEnv

class Particle:
    def __init__(self, players, field, current_step, game_over):
        self.players = players # player object copy
        self.field = field # 2d numpy array --- greater than 0 means food parcel
        self.current_step = current_step # int
        self.game_over = game_over  # bool
    
    def from_observations(self, obs):
        # create a possible particle from an observation
        
        pass
 


class LBFSimulator:
    def __init__(self, action_space) -> None:
        self.env = ForagingEnv(
            players = 5,
            max_player_level = 3,
            field_size = (8,8),
            max_food = 4,
            sight = 8,
            max_episode_steps = 50,
            force_coop = True
            )
    
    def config_env(self, particle) -> None:
        # configure the environment given a particle
        # test as this it the most complex part.
        self.env.players = particle.players
        self.env.field = particle.field
        self.env.current_step = particle.current_step
        self.env._game_over = particle.game_over


    def get_action_space(self):
        # return the possible actions available in each state
        return self.env.get_valid_actions()

    def step_env(self, joint_action) -> None:
        #move the environment forwards
        nobs, nrewards, ndone, ninfo  = self.env.step(joint_action)
        return nobs, nrewards, ndone, ninfo

    def simulate_history(self, history) -> None:
        # step the environment through to equal a history
        ptr = 0
        while self.env.terminal == False and ptr < len(history):
            self.step_env(history[ptr])
            ptr += 1
            if self.env._game_over == True:
                print('terminal state found')
                break
            
    def distill_env_to_particle(self) -> Particle:
        # distill the current state of the environment to a particle
        env_copy = pickle.loads(pickle.dumps(self.env))
        p = Particle(env_copy.players, env_copy.field, env_copy.current_step, env_copy._game_over)
        return p
    
    def is_terminal(self) -> bool:
        # return boolean if simulated env is still live
        return self.env._game_over
    
    def current_val(self) -> int:
        return self.env.players[0].score
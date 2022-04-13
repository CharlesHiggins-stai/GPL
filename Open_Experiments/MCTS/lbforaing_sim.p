import numpy
import pickle


class Particle:
    def __init__(self, current_value, agent_reward):
        self.current_value = current_value
        self.agent_reward = agent_reward

 


class LBFSimulator():
    def __init__(self, action_space) -> None:
        self.env = TestEnv(total = 12, action_space = action_space)

    
    def config_env(self, particle) -> None:
        # configure the environment given a particle
        self.env.terminal = False
        self.env.current_value = particle.current_value
        self.env.agent_reward = particle.agent_reward

    def get_action_space(self):
        # return the possible actions available in each state
        return self.action_space

    def step_env(self, joint_action) -> None:
        #move the environment forwards
        ar, cv = self.env.step(joint_action)

    def simulate_history(self, history) -> None:
        # step the environment through to equal a history
        ptr = 0
        while self.env.terminal == False and ptr < len(history):
            self.step_env(history[ptr])
            ptr += 1
        
    def distill_env_to_particle(self) -> Particle:
        # distill the current state of the environment to a particle
        p = Particle(self.env.current_value, self.env.agent_reward)
        return p
    
    def is_terminal(self) -> bool:
        # return boolean if simulated env is still live
        return self.env.terminal
    
    def current_val(self) -> int:
        return self.env.agent_reward
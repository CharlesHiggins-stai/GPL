import numpy

class Particle:
    def __init__(self, current_value, agent_reward):
        self.current_value = current_value
        self.agent_reward = agent_reward
 


class TestSimulator():
    def __init__(self, action_space):
        self.env = TestEnv(total = 8, action_space = ['2','4','8'])

    
    def config_env(self, particle):
        # configure the environment given a particle
        self.env.terminal = False
        self.env.current_value = particle.current_value
        self.env.agent_reward = particle.agent_reward

    def get_action_space(self):
        # return the possible actions available in each state
        return self.action_space

    def step_env(self, joint_action):
        #move the environment forwards
        ar, cv = self.env.step(joint_action)

    def simulate_history(self, history):
        # step the environment through to equal a history
        ptr = 0
        while self.env.terminal == False and ptr < len(history):
            self.step_env(history[ptr])
            ptr += 1
        
    def distill_env_to_particle(self):
        # distill the current state of the environment to a particle
        p = Particle(self.env.current_value, self.env.agent_reward)
        return p
    
    def is_terminal(self):
        # return boolean if simulated env is still live
        return self.env.terminal
    
    def current_val(self):
        return self.env.agent_reward
    



class TestEnv:
    #  adding simulator. Options are to add by 2, by 4, or by 8, in order to reach 100. 
    #  actions cost 0.01...
    #  if you get 100, it's terminal, plus 100. If you get above 100, you get minus the number over... 

    def __init__(self, total = 8, action_space = ['2', '4', '8']): 
        self.current_value = 0
        self.total_value = total
        self.agent_reward = 0
        self.terminal = False
    
    def step(self, action):
        if action == '2':
            self.current_value += 2
            self.agent_reward -= 0.05
        elif action == '4':
            self.current_value += 4
            self.agent_reward -= 0.05
        elif action == '8':
            self.current_value += 8
            self.agent_reward -= 0.05
        #  process actions

        if self.current_value == self.total_value:
            self.agent_reward += 100
            print('gave a big ass reward')
            self.terminal = True
        if self.current_value > self.total_value:
            self.agent_reward -= self.current_value - self.total_value
            self.terminal = True

        
        return self.agent_reward, self.current_value


class GreedyAgent:
    def __init__(self):
        current_value = 0
        goal = 100
    
    def step(self, current_value, goal):
        if current_value <= (goal - 8):
            return '8'
        else:
            return '4'

if __name__ == "__main__":
    game = TestEnv()
    ga = GreedyAgent()
    current_value = 0
    goal = 10
    while game.terminal == False:
        action = ga.step(current_value, goal)
        new_reward, current_value = game.step(action)
        print(action, game.agent_reward)
    print('over')        
        
from simulator import *
import math
import random
import copy

class MCTS_agent:
    def __init__(self):
        print('agent initialised')
        action_set = ['2', '4', '8']
        simulator = TestSimulator(action_set)
        self.search_engine = MCTS(simulator, action_set)

    def step(self, current_value, current_reward):
        if current_reward > 5:
            print('winning at life bitches')
        # TODO when moving to proper parrticle filter, will need to update particle selection
        # print(f"this is the current value {current_value}")
        action = self.search_engine.build_tree()
        return action
        
        

        

class MCTS:
    def __init__(self, simulator, action_set, max_iterations = 50):
        # action_set must be an interable of some sort, with unique values
        self.sim = simulator
        self.max_iterations = max_iterations
        self.action_set = action_set
        self.particle = None
    
    def get_particle(self):
        return self.particle
    
    def build_tree(self):
        # TODO impliment particle
        root = Node(None, None)
        for i in range(self.max_iterations):
            p = self.sim.distill_env_to_particle()
            self.search(p, root)
        best_child = sorted(root.children, key = lambda x: x.value/x.visits, reverse = True)[0]
        kids = sorted(root.children, key = lambda x: x.value/x.visits, reverse = True)
        # print("-"* 25)
        # for kid in kids:
        #     print(kid.action, kid.value/kid.visits)
        # print("-" * 25)

        return best_child.action

    def search(self, particle, root):
        #configure environment
        self.sim.config_env(particle)
        assert(self.sim.env.current_value == particle.current_value)
        #traversal & selection
        selected = self.traverse_selection(root)
        #expansion
        expanded = self.expand(selected)
        #rollout
        rollout_end = self.rollout(expanded)
        #backprop
        self.backpropagation(rollout_end)

    
    def traverse_selection(self, node):
        # traverse the graph using ucb1 algorithm to find a node which has yet to be fully expanded
        if node.expanded == False:
            return node
        else:
            node = self.ucb1(node)
            return self.traverse_selection(node)
            
    
    def expand(self, selected):
        assert(len(selected.children)<3)
        tried_actions = [child.action for child in selected.children]
        untried_actions = [action for action in self.action_set if action not in tried_actions]
        action = random.choice(untried_actions)
        #create data for new node
        if selected.route_from_root != None:
            history = copy.deepcopy(selected.route_from_root)
        else:
            history = []
        history.append(action)
        n_node = Node(history, selected)
        #connect n_node to its parent, and update the status of node if fully expanded
        selected.children.append(n_node)
        if len(selected.children) >= len(self.action_set):
            selected.expanded = True
            # print('marked as expanded')
        #roll forward simulator to take account this action history
        self.sim.simulate_history(n_node.route_from_root)
        return n_node

    
    def rollout(self, expanded, max_rollout_depth = 5):
        if self.sim.is_terminal() == True:
            expanded.value += self.sim.current_val()
            return expanded
        else:
            steps = 0
            while steps < max_rollout_depth:
                if not self.sim.is_terminal():
                    action = random.choice(self.action_set)
                    history = copy.deepcopy(expanded.route_from_root)
                    history.append(action)
                    n_node = Node(history, expanded)
                    expanded.children.append(n_node)
                    self.sim.step_env(action)
                    expanded = n_node # set up basic pointer chase through
                steps += 1
            expanded.value += self.sim.current_val()
        return expanded
    
    def backpropagation(self, end_node):
        final_val = end_node.value
        end_node.visits += 1
        node = end_node
        while node.parent != None:
            node.parent.visits += 1
            node.parent.value += node.value
            node = node.parent

        
    def ucb1(self, node, expl = 0.5):
        #upper confidence trees --- first parameter ucb is an average return of child, second term is (weighted) value exploring the relative exploration of parent to child
        best = None
        best_value = None
        for child in node.children:
            ucb = child.value/child.visits
            val = ucb + expl * math.sqrt(math.log(node.visits)/child.visits)
            if best != None:
                # print(f"this is val {val}")
                # print(f"this is best_val {best_value}")
                if val>best_value:
                    best_value = val
                    best = child
            else:
                best = child
                best_value = val

        return best

    
class Node:
    def __init__(self, history, parent = None):
        self.route_from_root = history
        self.value = 0
        self.visits = 0
        self.parent = parent
        self.children = []
        self.expanded = False
        self.action = None
        if history is not None:
            # print(history)
            self.action = history[-1]



if __name__ == "__main__":
    game = TestEnv()
    ga = MCTS_agent()
    current_value = 0
    new_reward = 0
    goal = 8
    action_history = []
    while game.terminal == False:
        action = ga.step(current_value, new_reward)
        new_reward, current_value = game.step(action)
        action_history.append(action)

    print('over')
    print(f'total rewards = {game.agent_reward}')
    print(f"total reached = {game.current_value}")        
    print(f'action_history: {action_history}')
        
    



    
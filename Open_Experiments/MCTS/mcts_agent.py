from simulator import *
import math
import random

class MCTS_agent:
    def __init__(self):
        print('agent initialised')
        simulator = TestSimulator()
        action_set = ['2', '4', '8']
        self.search_engine = MCTS(simulator, action_set)

    def step(current_value, current_reward):
        action = 
        

        

class MCTS:
    def __init__(self, simulator, action_set, max_iterations = 500):
        # action_set must be an interable of some sort, with unique values
        self.sim = simulator
        self.max_iterations = max_iterations
        self.action_set = action_set
    
    def build_tree(self):
        # TODO impliment particle
        root = Node([], None)
        p = self.get_particle()
        for i in range(max_iterations):
            self.search(p, root)
        best_child = sorted(root.children, key = lambda x: x.value/x.visits, reverse = True)[0]
        return best_child.route_from_root[0]

    def search(self, particle, root):
        #configure environment
        self.sim.config_env(particle)
        #traversal & selection
        selected = self.traverse_selection(root)
        #expansion
        expanded = self.expand(selected)
        #rollout
        rollout_end = self.rollout(expanded)
        #backprop
        self.backpropagation(rollout_end)

    
    def traverse_selection(self, node):
        # traverse the graph using ucb1 algorihtm to find a node which has yet to be fully expanded
        if node.expanded == False:
            return node
        else:
            node = self.ucb1(node)
            return self.traverse_selection(node)
    
    def expand(self, selected):
        tried_actions = [child.action for child in selected.children]
        untried_actions = [action for action in self.action_set not in tried_actions]
        action = random.choice(untried_actions)
        #create data for new node
        history = copy.deepcopy(selected.history)
        history.append(action)
        n_node = Node(history, selected)
        #connect n_node to its parent, and update the status of node if fully expanded
        selected.children.append(n_node)
        if len(selected.children) >= len(self.action_set):
            selected.expanded = True
        #roll forward simulator to take account this action history
        self.sim.simulate_history(n_node.history)
        return n_node

    
    def rollout(self, expanded, max_rollout_depth = 10):
        if self.sim.is_terminal() == True:
            expanded.value += self.sim.current_val()
            return expanded
        else:
            steps = 0
            while steps < max_rollout_depth:
                if not self.sim.is_terminal():
                    action = random.choice(self.action_set)
                    n_node = (expanded.history.append(action), expanded)
                    expanded.children.append(n_node)
                    self.sim.step_env(action)
                    expanded = n_node # set up basic pointer chase through
                steps += 1
            expanded.value += self.sim.current_val()
        return expanded
    
    def backpropagation(self, end_node):
        final_val = end_node.value
        end_node.visits += 1
        node = env_node
        while node.parent != None:
            node.parent.visits += 1
            node.parent.value += node.value
            node = node.parent

        
    def ucb1(self, node, expl = 2):
        #upper confidence trees --- first parameter ucb is an average return of child, second term is (weighted) value exploring the relative exploration of parent to child
        best = None
        best_value = None
        for child in node.children:
            ucb = child.value/child.visits
            val = ucb + expl * math.sqrt(math.log(node.visits)/child.visits)
            if best is not None:
                if val>best_value:
                    best_value = val
                    best = child
            else:
                best = child
                best_val = val

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
            self.action = history[-1]





if __name__ == "__main__":
    



    
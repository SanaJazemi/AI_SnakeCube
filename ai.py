import numpy as np
from sim import Simulator, Interface
import json
from time import time
import queue

class Agent:

    def __init__(self):
        self.predicted_actions=[]

    def act(self, percept):
        sensor_data = json.loads(percept)

        alg = self.A_star

        if self.predicted_actions == []:
            t0 = time()
            initial_state = Simulator(sensor_data['coordinates'], sensor_data['stick_together'])
            self.predicted_actions = alg(initial_state)
            if self.predicted_actions is None : raise Exception("No solution found")
            print("run time:" , time()-t0)

        action = self.predicted_actions.pop()
        # action example: [1,2,2]
        # the first number is the joint number (1: the first joint)
        # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
        # the third number is the degree (1: 90 degree, 2: 180 degree, 3: -90 degree)
        return action

    def heuristic(self, state):
        axs = state.coordinates.T
        steps = (len(np.unique(axs[0]))+ len(np.unique(axs[1]))+ len(np.unique(axs[2])))/9-1
        return steps

    def A_star(self, root_game):
        interface = Interface()
        # append the first state as (state, action_history)
        node = [root_game, [[-1,-1,-1]]]
        q = queue.PriorityQueue()
        q.put((float('inf'),0))
        node_list = [node]
        while not q.empty():
            # pop first element from queue
            i = q.get()[1]
            node = node_list[i]
            node_list[i] = None
            # get the list of legal actions
            action_list = interface.valid_actions(node[0], np.transpose(node[1])[1])
            for action in action_list:
                # copy the current state
                child_state = interface.copy_state(node[0])
                # take action and change the copied node
                interface.evolve(child_state, action)
                # check if the child state is valid or not
                if not interface.valid_state(child_state): 
                    continue
                # add the child state to the nodes
                new_node = [child_state, [action] + node[1]]
                q.put((len(node[1]) + self.heuristic(child_state), len(node_list)))
                node_list.append(new_node)
                # return if goal test is true
                if interface.goal_test(child_state): 
                    return [action] + node[1][:-1]

    """def BFS(self, root_game):

        interface = Interface()

        q = []
        # append the first state as (state, action_history)
        q.append([root_game, [[-1,-1,-1]]])

        while q:
            # pop first element from queue
            node = q.pop(0)
            
            # get the list of legal actions
            actions_list = interface.valid_actions(node[0] , np.transpose(node[1])[1])
            
            # randomizing the order of child generation
            np.random.shuffle(actions_list)
            
            for action in actions_list:
                # copy the current state
                child_state = interface.copy_state(node[0])
                
                # take action and change the copied node
                interface.evolve(child_state, action)

                if not interface.valid_state(child_state): continue
                
                # add children to queue
                q.append([child_state, [action] + node[1]])
                
                # return if goal test is true
                if interface.goal_test(child_state): 
                    return [action] + node[1][:-1]"""

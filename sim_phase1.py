from copy import deepcopy
import json
import math
import numpy as np    

  
class Simulator:
    def __init__(self, state):
        self.coordinates = json.dumps({"coordinates":state.coordinates})
        self.sticky_cubes = json.dumps({"sticky_cubes":state.sticky_cubes})

    def rotate(self, degree, axis,start_index, end_index, i):
        
        sinTheta = math.sin(math.radian(degree))
        cosTheta = math.cos(math.radian(degree))
        
        #rotation matrix
        matrixX = [[1,0,0], [0, cosTheta, -sinTheta], [0,sinTheta, cosTheta]]
        matrixY = [[cosTheta, 0, sinTheta], [0,1,0], [-sinTheta, 0, cosTheta]]
        matrixZ = [[cosTheta, -sinTheta, 0], [sinTheta, cosTheta, 0], [0,0,1]]

        vector = [[self.coordinates[i][0]- self.coordinates[i+1][0]], [self.coordinates[i][1]- self.coordinates[i+1][1]], [self.coordinates[i][2]- self.coordinates[i+1][2]]]

        if axis == 'x': np.matmul(vector, matrixX)
        if axis == 'y': np.matmul(vector, matrixY)
        if axis == 'z': np.matmul(vector, matrixZ)
    
    def take_action(self, action, i, degree):
        #if the two blocks are on the same mehvar, then go to next state, if not then check if stick together, if true, no action, if false call rotate
        #if i<26-i+1 rotate(i) else rotate(i+1 to 26)
        if self.coordinates[i][0] == self.coordinates[i+1][0] or self.coordinates[i][1] == self.coordinates[i+1][1] or self.coordinates[i][2] == self.coordinates[i+1][2]: return
        #make coordinates into a list and find a way to get X Y Z value
    
        else:
            for j in self.sticky_cubes:
                if [i,i+1] == self.sticky_cubes[j]: return
                else:
                    if (self.coordinates[i][0] == self.coordinates[i+1][0] and self.coordinates[i][1] == self.coordinates[i+1][1]): axis = 'x'
                    if (self.coordinates[i][0] == self.coordinates[i+1][0] and self.coordinates[i][2] == self.coordinates[i+1][2]): axis= 'y'
                    if (self.coordinates[i][1] == self.coordinates[i+1][1] and self.coordinates[i][2] == self.coordinates[i+1][2]): axis= 'z'
                    if i < 27-i : Simulator.rotate(degree, axis, 0,i, i)
                    else: Simulator.rotate(degree, axis, i+1, 26, i)
     


class Interface:
    def __init__(self):
        pass

    def evolve(self, state, action):
        if type(action) is not str: raise("action is not a string")
        action=action.upper()
        if action not in self.valid_actions(state): raise("action is not valid")
        state.take_action(action)

    def copy_state(self, state):
        _copy = Simulator(None,None)
        _copy.map = deepcopy(state.map)
        _copy.agent_loc = deepcopy(state.agent_loc)
        return _copy

    def perceive(self, state):
        initial_state = json.dumps({"coordinates":state.coordinates, "sticky_cubes":state.sticky_cubes})
        #get max of X Y Z
        for i in range(26):
            for j in self.coordinates[i][0]: 
                max_x = json.dumps(max({"coordinates":state.coordinates}))
                min_x = json.dumps(min({"coordinates":state.coordinates}))
            for j in self.coordinates[i][1]:
                max_y = json.dumps(max({"coordinates":state.coordinates}))
                min_y = json.dumps(min({"coordinates":state.coordinates}))    
            for j in self.coordinates[i][2]:
                max_z = json.dumps(max({"coordinates":state.coordinates}))
                min_z = json.dumps(min({"coordinates":state.coordinates}))  
        Interface.goal_test(state, max_x, min_x, max_y, min_y, max_z, min_z)
        return initial_state

    def goal_test(self, state, max_x, min_x, max_y, min_y, max_z, min_z):
        #idea: get coordinates and if the max of X,Y,Z is 2 then it has reached it's goal
    
        if abs(max_x - min_x) == 2 and abs(max_y - min_y) == 2 and abs(max_z - min_z) == 2: return True
        

    def valid_actions(self, state):
        return ["rotate 90", "rotate -90", "rotate 180"]

    def valid_states(self, state):
        for i in range(26):
            for j in range(26):
                if self.coordinates[i] == self.coordinates[j]: return False
                else: return True


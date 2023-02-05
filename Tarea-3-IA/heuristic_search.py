from typing import final
import numpy as np
from numpy.core.fromnumeric import argmin

DEPTH_MAX=50 # Root node has 0 depth
np.random.seed(1)
#--------------------#
# Equality of arrays #
#--------------------#
def is_equal(A,B):
    if A.shape[0]!=B.shape[0] or A.shape[1]!=B.shape[1]:
        return False
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            if A[i][j]!=B[i][j]:
                return False
    return True
#--------------------#
# Printing dashboard #
#--------------------#
def print_dashboard(A):
    print("%d : %d : %d" %(A[0][0],A[0][1],A[0][2]))
    print("%d : %d : %d" %(A[1][0],A[1][1],A[1][2]))
    print("%d : %d : %d" %(A[2][0],A[2][1],A[2][2]))
#------------#
# Node class #
#------------#
class node:
    def __init__(self,value,cost,father_node=None):
        self.value = value
        self.cost=cost
        self.father_node = father_node
        # Depth
        depth_node=0
        father=father_node
        while father!=None:
            father=father.father_node
            depth_node=depth_node+1
        self.depth=depth_node
    # Equality in nodes
    def __eq__(self, other):
        if isinstance(other, node):
            aux1=self.value
            aux2=other.value
            return is_equal(aux1,aux2)
        return False
#-------------#
# Node Deepth #
#-------------#
def depth(current_state):
    depth_node=0
    father=current_state.father_node
    while father!=None:
        father=father.father_node
        depth_node=depth_node+1
    return depth_node
'''
Distances
'''      
#--------------------# 
# Manhattan distance #
#--------------------#
def Manhattan_dist(current_value,final_value):
    dist=0
    for i in range(3):
        for value in final_value[i]:
            if value!=0.0:
                dist+=abs(np.where(current_value==value)[0]-np.where(final_value==value)[0])[0]
                dist+=abs(np.where(current_value==value)[1]-np.where(final_value==value)[1])[0]
    return dist
#--------------------#
# Counting distance  #
#--------------------#  
def Counting_dist(current_value,final_value):
    misplaced=(current_value==final_value)
    dist=misplaced.size-np.sum(misplaced)
    if np.where(current_value==0)!=np.where(final_value==0):
        return dist-1
    return dist
#----------------------#
# Permutation distance #
#----------------------#
def Inversion_dist(current_value,final_value):
        # Inversions based in the order configuration 123456780
        inv_count_current = 0
        arr_current=[j for sub in current_value for j in sub]
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr_current[i] != empty_value and arr_current[j] != empty_value and arr_current[i] > arr_current[j]:
                    inv_count_current += 1
        # Number of inversions for the final value
        inv_count_final = 0
        arr_final=[j for sub in final_value for j in sub]
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr_final[i] != empty_value and arr_final[j] != empty_value and arr_final[i] > arr_final[j]:
                    inv_count_final += 1
        return abs(inv_count_current-inv_count_final) # In the goal is zero    
'''
Informed Search
'''
#--------------#
# A* Algorithm #
#--------------#
class A_star:
    # Initial variables 
    def __init__(self,init_value,final_value,dist_func):
        self.init_state=node(value=init_value,cost=dist_func(init_value,final_value))
        self.final_value=final_value
        self.open_states=[]
        self.closed_states=[]
    # Count inversions
    def getInvCount(self,arr):
        inv_count = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[i] != empty_value and arr[j] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count
    # if given 8 puzzle is solvable.
    def isSolvable(self,puzzle):
        # Count inversions in given 8 puzzle
        inv_count = self.getInvCount([j for sub in puzzle.value for j in sub])
        inv_count_final=self.getInvCount([j for sub in self.final_value for j in sub])
        # return true if inversion count is even.
        return (inv_count % 2 == inv_count_final % 2)
    # Obtain successors
    def get_successors(self,current_state,dist_func):
        # Current state value
        father_node=current_state
        current_state=current_state.value
        # Hole Position
        position_hole=np.where(current_state==0)
        position_hole=list(zip(position_hole[0],position_hole[1]))
        hole=position_hole[0]
        # Available Positions and movements
        available_pos=[0,1,2]
        movements=[hole[0]-1,hole[0]+1,hole[1]-1,hole[1]+1]
        # Build sons
        sons=[]
        # (i,j)->(i-1,j) (up) 
        if available_pos.count(movements[0])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[0]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[0]][hole[1]]=tmp1
            son=node(son_value,dist_func(son_value,self.final_value),father_node)
            sons.append(son)
        # (i,j)->(i+1,j) (down)   
        if available_pos.count(movements[1])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[1]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[1]][hole[1]]=tmp1
            son=node(son_value,dist_func(son_value,self.final_value),father_node)
            sons.append(son)
        # (i,j)->(i,j-1) (leff)
        if available_pos.count(movements[2])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[2]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[2]]=tmp1
            son=node(son_value,dist_func(son_value,self.final_value),father_node)
            sons.append(son)
        # (i,j)->(i,j+1) (right)
        if available_pos.count(movements[3])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[3]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[3]]=tmp1
            son=node(son_value,dist_func(son_value,self.final_value),father_node)
            sons.append(son)
        return sons
    # Deal with repetitions
    def deal_repetitions(self,sons):
        # Open states
        for open_node in self.open_states:
            for state in sons:
                if is_equal(open_node.value,state.value):
                    if open_node.cost+open_node.depth>state.cost+state.depth:
                        self.open_states.remove(open_node)
                    else:
                        sons.remove(state)
                    #sons.remove(state)
        # Closed states
        for closed_node in self.closed_states:
            for state in sons:
                if is_equal(closed_node.value,state.value):
                    
                    if closed_node.cost+closed_node.depth>state.cost+state.depth:
                        self.closed_states.remove(state)
                        #sons.remove(state)
                    else:
                        sons.remove(state)
                    #sons.remove(state)
        return sons
    # Append in list open
    def append_open(self,sons):
        for son in sons:
            self.open_states.append(son)
    # Getting better (from open_states)
    def get_better(self):
        cost=np.array([state.cost+state.depth for state in self.open_states])
        argmin_cost=np.argwhere(cost==np.amin(cost))
        argmin_cost=argmin_cost.reshape(argmin_cost.shape[0])
        if argmin_cost.size==1:
            value=self.open_states[argmin_cost[0]]
            #self.open_states.remove(value)
            return value
        else:
            # First criteria for repetitions is the heuristic distance
            states_argmin_cost=[self.open_states[i] for i in argmin_cost]
            heuristic_value=[state.cost for state in states_argmin_cost]
            argmin_heuristic=np.argwhere(heuristic_value==np.amin(heuristic_value))
            argmin_heuristic=argmin_heuristic.reshape(argmin_heuristic.shape[0])
            if argmin_heuristic.size==1:
                value=states_argmin_cost[argmin_heuristic[0]]
                #self.open_states.remove(value)
                return value
            else:
                # Second criteria for repetitions is the depth
                states_argmin_heuristic=[states_argmin_cost[i] for i in argmin_heuristic]
                depth_value=[state.depth for state in states_argmin_heuristic]
                argmin_depth=np.argwhere(depth_value==np.amin(depth_value))
                argmin_depth=argmin_depth.reshape(argmin_depth.shape[0])
                value=states_argmin_heuristic[argmin_depth[0]]
                #self.open_states.remove(value)
                return value
    # Main function
    def main(self,dist_func):
        if self.isSolvable(self.init_state):
            # Search Algorithm
            current_state=self.init_state
            self.open_states.append(current_state)
            while (not is_equal(current_state.value,self.final_value)) and len(self.open_states)>0:
                self.open_states.remove(current_state)
                self.closed_states.append(current_state)
                if current_state.depth<=DEPTH_MAX:
                    sons=self.get_successors(current_state,dist_func)
                    sons=self.deal_repetitions(sons)
                    if len(sons)>0:
                        self.append_open(sons)
                current_state=self.get_better()
            self.final_state=current_state
            self.closed_states.append(self.final_state)
            # Printing solution
            aux=[current_state.value]
            father=current_state.father_node
            while father!=None:
                aux.append(father.value)
                father=father.father_node
            aux.reverse()
            for i in range(len(aux)):
                print_dashboard(aux[i])
                print('\n')
            print('Numero de movimientos de la solución: %d' %(len(aux)-1))
            print('Numero de nodos visitados: %d' %(len(self.closed_states)))
            print('Numero de nodos por visitar: %d' %(len(list(self.open_states))))
            print('Numero de nodos expandidos: %d' %(len(self.closed_states)+len(list(self.open_states))))
        else:
            print('No se puede alcanzar el nodo final')

#-------#
# Proof #
#-------#
'''
init_value=np.array([[3,2,1],[6,5,4],[8,7,0]])
final_value=np.array([[1,2,3],[4,5,6],[8,7,0]])

A_star_1=A_star(init_value,final_value,Inversion_dist)
A_star_1.main(Inversion_dist)
'''


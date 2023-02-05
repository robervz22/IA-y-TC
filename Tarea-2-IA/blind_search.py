import numpy as np

DEPTH_MAX=10
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
# Clase nodo #
#------------#
class node:
    def __init__(self, value,father_node=None):
        self.value = value
        self.father_node = father_node
    # Equality in nodes
    def __eq__(self, other):
        if isinstance(other, node):
            aux1=self.value
            aux2=other.value
            return is_equal(aux1,aux2)
        return False
#--------------------#
# BFS (FIFO) (queue) #
#--------------------#
from collections import deque
class BFS:
    # Initial variables 
    def __init__(self,init_state,final_value):
        self.init_state=init_state
        self.open_states=deque([])
        self.closed_states=[]
        self.final_value=final_value
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
    def get_successors(self,current_state):
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
        # (i,j)->(i-1,j)  
        if available_pos.count(movements[0])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[0]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[0]][hole[1]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i+1,j)    
        if available_pos.count(movements[1])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[1]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[1]][hole[1]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i,j-1)
        if available_pos.count(movements[2])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[2]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[2]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i,j+1)
        if available_pos.count(movements[3])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[3]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[3]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        return sons
    # Deal with repetitions
    def deal_repetitions(self,sons):
        # Open states
        for open_node in self.open_states:
            for state in sons:
                if is_equal(open_node.value,state.value):
                    sons.remove(state)
        # Closed states
        for closed_node in self.closed_states:
            for state in sons:
                if is_equal(closed_node.value,state.value):
                    sons.remove(state)
        return sons
    # Node Deepth
    def depth(self,current_state):
        depth_node=1
        father=current_state.father_node
        while father!=None:
            father=father.father_node
            depth_node=depth_node+1
        return depth_node
    # Append in list open
    def append_open(self,sons):
        for son in sons:
            self.open_states.append(son)           
    # Main function
    def main(self):
        if self.isSolvable(self.init_state):
            # Search Algorithm
            current_state=self.init_state
            self.open_states.append(current_state)
            while (not is_equal(current_state.value,self.final_value)) and len(list(self.open_states))>0:
                current_state=self.open_states.popleft()
                self.closed_states.append(current_state)
                if self.depth(current_state)<=DEPTH_MAX-1:
                    sons=self.get_successors(current_state)
                    sons=self.deal_repetitions(sons)
                    if len(sons)>0:
                        self.append_open(sons)
                current_state=self.open_states.popleft()
                self.open_states.appendleft(current_state)
            self.final_state=self.open_states.popleft()
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
#--------------------#
# DFS (LIFO) (stack) #
#--------------------#
class DFS:
    # Initial variables 
    def __init__(self,init_state,final_value):
        self.init_state=init_state
        self.open_states=[]
        self.closed_states=[]
        self.final_value=final_value
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
        inv_count_init=self.getInvCount([j for sub in self.final_value for j in sub])
        # return true if inversion count is even.
        return (inv_count % 2 == inv_count_init % 2)
    # Obtain successors
    def get_successors(self,current_state):
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
        # (i,j)->(i-1,j)  
        if available_pos.count(movements[0])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[0]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[0]][hole[1]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i+1,j)    
        if available_pos.count(movements[1])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[movements[1]][hole[1]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[movements[1]][hole[1]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i,j-1)
        if available_pos.count(movements[2])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[2]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[2]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        # (i,j)->(i,j+1)
        if available_pos.count(movements[3])>0:
            tmp1=current_state[hole[0]][hole[1]]
            tmp2=current_state[hole[0]][movements[3]]
            son_value=np.copy(current_state)
            son_value[hole[0]][hole[1]]=tmp2
            son_value[hole[0]][movements[3]]=tmp1
            son=node(son_value,father_node)
            sons.append(son)
        return sons
    # Deal with repetitions
    def deal_repetitions(self,sons):
        # Open states
        for open_node in self.open_states:
            for state in sons:
                if is_equal(open_node.value,state.value):
                    sons.remove(state)
        # Closed states
        for closed_node in self.closed_states:
            for state in sons:
                if is_equal(closed_node.value,state.value):
                    sons.remove(state)
        return sons
    # Node Deepth
    def depth(self,current_state):
        depth_node=1
        father=current_state.father_node
        while father!=None:
            father=father.father_node
            depth_node=depth_node+1
        return depth_node
    # Append in list open
    def append_open(self,sons):
        for son in sons:
            self.open_states.append(son)           
    # Main function
    def main(self):
        if self.isSolvable(self.init_state):
            # Search Algorithm
            current_state=self.init_state
            self.open_states.append(current_state)
            while (not is_equal(current_state.value,self.final_value)) and len(self.open_states)>0:
                current_state=self.open_states.pop()
                self.closed_states.append(current_state)
                if self.depth(current_state)<=DEPTH_MAX-1:
                    sons=self.get_successors(current_state)
                    sons=self.deal_repetitions(sons)
                    if len(sons)>0:
                        self.append_open(sons)
                current_state=self.open_states.pop()
                self.open_states.append(current_state)
            self.final_state=self.open_states.pop()
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
            print('Numero de nodos por visitar: %d' %(len(self.open_states)))
            print('Numero de nodos expandidos: %d' %(len(self.closed_states)+len(self.open_states)))
        else: 
            print('No se puede alcanzar el nodo final')
#-------#
# Proof #
#-------#

# Solvable
# Case 1
init_value_1=np.array([[1,2,3],[4,0,5],[6,7,8]])
final_value_1=np.array([[0,1,3],[4,2,5],[6,7,8]])
init_state_1=node(init_value_1)
print('Busqueda BFS:')
first_case_BFS=BFS(init_state_1,final_value_1)
first_case_BFS.main()
print('\nBusqueda DFS:')
first_case_DFS=DFS(init_state_1,final_value_1)
first_case_DFS.main()



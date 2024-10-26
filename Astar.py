import heapq
from math import sqrt
import time
import sys

class Node:
    def __init__(self,state,parent,action,cost,heuristic,total_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic

    def __lt__(self, other):
        return self.total_cost < other.total_cost




def heuristic(state,goal,heuristic_type):
    if heuristic_type==1:
        return heuristic_manhattan_distance(state,goal)
    elif heuristic_type==2:
        return heuristic_euclidean_distance(state,goal)




def heuristic_manhattan_distance(state,goal):
    manhattan_distnace=0
    for i in range(9):
        if(state.index(i)!=goal.index(i) and state.index(i)!=0):
            manhattan_distnace+=abs((state.index(i)%3)-(goal.index(i)%3))+abs((state.index(i)//3)-(goal.index(i)//3))
    return manhattan_distnace





def heuristic_euclidean_distance(state,goal):
    euclidian_distance=0
    for i in range(9):
        if(state.index(i)!=goal.index(i) and state.index(i)!=0):
            euclidian_distance+=sqrt(pow((state.index(i)%3)-(goal.index(i)%3),2)+pow((state.index(i)//3)-(goal.index(i)//3),2))
    return euclidian_distance




def a_star_algorithm(initial_state,goal_state,heuristic_type):
    start_time=time.time()
    frontier=[]
    heapq.heapify(frontier)
    explored={}
    initial_cost=0
    initial_heuristic=heuristic(initial_state,goal_state,heuristic_type)
    initial_total_cost=initial_cost+initial_heuristic
    initial_node=Node(initial_state,None,None,initial_cost,initial_heuristic,initial_total_cost)
    heapq.heappush(frontier,(initial_total_cost,initial_node))
    while frontier:
        curr=heapq.heappop(frontier)[1]
        explored[tuple(curr.state)]=curr
        if(curr.state==goal_state):
            path=[]
            while curr.parent:
                path.append(curr.action)
                curr=curr.parent
            path.reverse()
            print("Path to Goal:", path)
            print("Cost of Path:",len(path))
            print("Nodes Expanded:",len(explored)-1)
            print("Search Depth:",len(path))
            print("Running Time:",time.time()-start_time)
            return
        moves={"Left":-1,"Right":1,"Down":3,"Up":-3}
        for move,step in moves.items():
            if (curr.state.index(0)%3!=0 and move=="Left") or (curr.state.index(0)%3!=2 and move=="Right") or (curr.state.index(0)//3!=2 and move=="Down") or (curr.state.index(0)//3!=0 and move=="Up"):
                new_state=curr.state.copy()
                new_state[curr.state.index(0)]=new_state[curr.state.index(0)+step]
                new_state[curr.state.index(0)+step]=0
                new_cost=curr.cost+1
                new_heuristic=heuristic(new_state,goal_state,heuristic_type)
                new_total_cost=new_cost+new_heuristic
                if tuple(new_state) not in explored or new_total_cost < explored[tuple(new_state)].total_cost:
                    new_node=Node(new_state,curr,move,new_cost,new_heuristic,new_total_cost)
                    heapq.heappush(frontier,(new_total_cost,new_node))
    return None

def count_inversions(state):
    inversions = 0
    tiles = [tile for tile in state if tile != 0]
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions

def is_solvable(initial_state, goal_state):
    initial_inversions = count_inversions(initial_state)
    goal_inversions = count_inversions(goal_state)
    return initial_inversions % 2 == goal_inversions % 2

initial_state=[1,0,2,7,5,4,8,6,3]
goal_state=[0,1,2,3,4,5,6,7,8]
heuristic_type=2
if is_solvable(initial_state, goal_state):
    a_star_algorithm(initial_state, goal_state, heuristic_type)
else:
    print("The puzzle is unsolvable.")











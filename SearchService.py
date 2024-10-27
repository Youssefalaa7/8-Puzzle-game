import time
f = open("States.txt" , "w")


def get_children(state: int):
    children = list()
    state_str = str(state)
    zero_p = int()
    try:
        zero_p = state_str.index('0')
    except:
        state_str = '0' + state_str
        zero_p = 0
    directions = [1, -1, 3, -3]
    for i in directions:
        place = zero_p + i
        if 0 <= place < len(state_str) and ((abs(i) == 3) or ((i==1) and (zero_p% 3 != 2)) or((i==-1) and(zero_p % 3 != 0))):
            new_state = swap(state_str, zero_p, place)
            children.append(new_state)
    return children
def swap(input: str, first, second):
    l = list(input)
    l[first],l[second] = l[second],l[first]
    swapped_state = ''.join(l)
    return int(swapped_state)
def get_path(parents:dict , goal : int):
    direction = list()
    x = goal
    while x !=  -1:
        y = parents[x]
        child_place = find_zero(str(x))
        parent_place = find_zero(str(y))
        if child_place == parent_place+1:
            direction.append("right")
        elif child_place == parent_place-1:
            direction.append("left")
        elif child_place == parent_place +3:
            direction.append("down")
        elif child_place == parent_place -3:
            direction.append("up")
        x = y

    direction.reverse()
    return direction
def find_zero(input:str):
    try:
        return input.index('0')
    except:
        return 0



def bfs(state: int, goal):
    frontier = list([state])
    level = dict()
    level[state] = 0
    parent = dict()
    parent[state] = -1
    explored = set()
    max_depth = int()
    flag = False
    while frontier:
        current_state = frontier.pop(0)
        f.write(str(current_state))
        f.write("\n")


        explored.add(current_state)


        children = get_children(current_state)
        for child in children:
         if (child not in explored) and (child not in frontier):
            frontier.append(child)
            parent[child] = current_state
            level[child] = level[current_state] + 1
         else:
             max_depth = max(max_depth, level[current_state])
        if current_state==goal:
            flag = True
            break
    if flag == True:
        print("Path Found")
        print("Max Depth:  ", max_depth)
        print("Path Cost:   ", level[goal])
        print("Nodes expanded", len(explored))
        print(get_path(parent , goal))
        return True , max_depth , level[goal] , len(explored) , get_path(parent , goal)
    else:
        print("Path Not found")
        return False,max_depth,None,len(explored),None




def dfs(state: int, goal:int ):
    frontier = [state]
    level = dict()
    level[state] = 0
    parent = dict()
    parent[state] = -1
    explored = set()
    max_depth = int()
    flag = False
    while frontier:
        current_state = frontier.pop()
        f.write(str(current_state))
        f.write("\n")


        explored.add(current_state)


        children = get_children(current_state)
        for child in children:
         if (child not in explored) and (child not in frontier):
            frontier.append(child)
            parent[child] = current_state
            level[child] = level[current_state] + 1
         else:
             max_depth = max(max_depth, level[current_state])
        if current_state==goal:
            flag = True
            break
    if flag == True:
        print("Path Found")
        print("Max Depth:  ", max_depth)
        print("Path Cost:   ", level[goal])
        print("Nodes expanded", len(explored))
        print(get_path(parent , goal))
        return True , max_depth , level[goal] , len(explored) , get_path(parent, goal)
    else:
         print("Path Not found")
         return False , max_depth , None , len(explored) , None






def dfs_with_limit(init_state:int  , goal:int, limit:int):
    frontier = [init_state]
    explored = set()
    parent = dict()
    parent[init_state] = -1
    level = dict()
    level[init_state] = 0
    flag = False
    current_state = int()
    while frontier:
        current_state = frontier.pop()
        explored.add(current_state)
        f.write(str(current_state))
        f.write("\n")
        if current_state == goal:
            flag =True
            continue
        children = get_children(current_state)
        for child in children:
            x = level[current_state] + 1
            if  x <= limit:
                 if ((child in frontier) or (child in explored)) and (level[current_state]+1 <level[child] ):
                    frontier.append(child)
                    parent[child] = current_state
                    level[child] = x
                 elif (child not in frontier) and (child not  in explored):
                    frontier.append(child)
                    parent[child] = current_state
                    level[child] = x
    f.write("\n#######################\n")
    return flag , level , len(explored) ,current_state , parent
def ids(state: int, goal: int):
    previous_explored_nodes = 0
    depth_limit = 0
    explored = 0


    while True:
        result, level, iterative_explored, solution, parents = dfs_with_limit(state, goal, depth_limit)
        explored+=iterative_explored
        if result:
            print("Goal Found")
            print("Path to Goal:", get_path(parents, goal))
            print("Depth Limit Reached:", depth_limit)
            print("Path Cost:", level[goal])
            print("Total Nodes Explored:", explored)
            return True,depth_limit,level[goal],explored,get_path(parents , goal)
        elif iterative_explored == previous_explored_nodes:
            print("Goal Not Found within current limits")
            return False, depth_limit,explored ,  None, None
        else:
            previous_explored_nodes = iterative_explored
            depth_limit += 1






# start_time = time.time()
#
# end_time = time.time()
# exec_time = end_time - start_time
# print("exec_time  " , exec_time , "Seconds")
# print("##############################")
# print(result)
# print(max_depth)
# print(cost)
# print(explored_nodes)
# print(path)
# print(tim)










# def dfs_with_limit(init_state:int  , goal:int, limit:int):
#     frontier = [init_state]
#     explored = set()
#     parent = dict()
#     parent[init_state] = -1
#     level = dict()
#     level[init_state] = 0
#     while frontier:
#         current_state = frontier.pop()
#         explored.add(current_state)
#         f.write(str(current_state))
#         f.write("\n")
#         if current_state == goal:
#             return True , level , len(explored) ,current_state , parent
#         children = get_children(current_state)
#         for child in children:
#             level[child] = level[current_state] + 1
#             if (child not in frontier) and (child not in explored) and (level[child] <= limit):
#                 frontier.append(child)
#                 parent[child] = current_state
#     f.write("\n#######################\n")
#     return False, level , len(explored) ,None , None


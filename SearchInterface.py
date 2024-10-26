import time
import SearchService as ss




def bfs(init_state: int):
    start = time.time()
    result, max_depth, cost, explored_nodes, path = ss.bfs(init_state, 12345678)
    end = time.time()
    exec = end - start
    return result, max_depth, cost, explored_nodes,path, exec

def dfs(state_init:int):
    start = time.time()
    result, max_depth, cost, explored_nodes, path = ss.dfs(state_init,12345678)
    end = time.time()
    exec = end-start
    return result,max_depth, cost, explored_nodes, path , exec

def ids(state_init:int):
    start = time.time()
    result,max_depth,cost,explored_nodes,path = ss.ids(state_init,12345678)
    end = time.time()
    exec = end-start
    return result,max_depth,cost,explored_nodes,path,exec



result,max_depth,cost,explored_nodes,path,exec = ids(213456780)
print(result)
print(max_depth)
print(cost)
print(explored_nodes)
print(path)
print(exec)






# result:boolean  if solvable or not
# cost :int depth of the goal
# explored_nodes : int number of explored nodes
# path : list of directions
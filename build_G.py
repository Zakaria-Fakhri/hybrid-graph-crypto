import random

def build_graph(nodes, prob, seed):
    random.seed(seed)
    adj = []
    for i in range(nodes):
        adj.append([])
    
    # ring structure
    for i in range(nodes):
        next_node = (i + 1) % nodes
        adj[i].append(next_node)
        adj[next_node].append(i)
    
    # random edges
    for i in range(nodes):
        for j in range(i + 2, nodes):
            if random.random() < prob:
                adj[i].append(j)
                adj[j].append(i)
    
    return adj

def get_neighbors(graph, node):
    return graph[node][:]

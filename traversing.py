from collections import deque

def bfs(graph, start):
    visited = [False] * len(graph)
    parent = [-1] * len(graph)
    q = deque([start])
    visited[start] = True
    
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = node
                q.append(neighbor)
    
    return parent

def build_tree(parent):
    children = []
    for _ in range(len(parent)):
        children.append([])

    for i, p in enumerate(parent):
        if p != -1:
            children[p].append(i)
    return children

def postorder(children, root):
    def walk(node):
        order = []
        for child in children[node]:
            order.extend(walk(child))
        order.append(node)
        return order
    return walk(root)

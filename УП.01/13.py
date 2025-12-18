# 13_graphs.py
from collections import deque

graph = [
    [1,2],      # 0
    [0,3,4],    # 1
    [0],        # 2
    [1],        # 3
    [1]         # 4
]

def bfs(start):
    q = deque([start]); visited = [False]*len(graph); visited[start] = True
    while q:
        v = q.popleft()
        print(v, end=' ')
        for to in graph[v]:
            if not visited[to]:
                visited[to] = True
                q.append(to)
bfs(0)  # 0 1 2 3 4
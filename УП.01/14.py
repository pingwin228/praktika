# 14_islands.py
grid = [
  [1,1,0,0,0],
  [1,1,0,0,0],
  [0,0,1,0,0],
  [0,0,0,1,1]
]

def num_islands(g):
    if not g: return 0
    rows, cols = len(g), len(g[0])
    vis = [[False]*cols for _ in range(rows)]
    def dfs(i,j):
        if i<0 or i>=rows or j<0 or j>=cols or g[i][j]==0 or vis[i][j]: return
        vis[i][j] = True
        for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(i+di, j+dj)
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1 and not vis[i][j]:
                dfs(i,j); cnt += 1
    return cnt

print("Островов:", num_islands(grid))  # 3
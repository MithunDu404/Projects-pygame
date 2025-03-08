import pygame
import math
from queue import PriorityQueue

Width = 700
Win = pygame.display.set_mode((Width,Width))
pygame.display.set_caption("A* Path Finding Algorithm")

Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 255, 0)
Yellow = (255, 255, 0)
White = (255, 255, 255)
Black = (0, 0, 0)
Purple = (128, 0, 128)
Orange = (255, 165 ,0)
Gray = (128, 128, 128)
Turquoise= (64, 224, 208)

class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = White
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row,self.col
    def is_open(self):
        return self.color == Turquoise
    def is_closed(self):
        return self.color == Green
    def is_barrier(self):
        return self.color == Black
    def is_start(self):
        return self.color == Blue
    def is_end(self):
        return self.color == Purple
    def is_path(self):
        return self.color == Red
    
    def reset(self):
        self.color = White
    def make_open(self):
        self.color = Turquoise
    def make_closed(self):
        self.color = Green
    def make_barrier(self):
        self.color = Black
    def make_start(self):
        self.color = Blue
    def make_end(self):
        self.color = Purple
    def make_path(self):
        self.color = Red

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        n = self.total_rows
        r = self.row
        c = self.col
        if r < n-1 and not grid[r+1][c].is_barrier():
            self.neighbors.append(grid[r+1][c])
        if r > 0 and not grid[r-1][c].is_barrier():
            self.neighbors.append(grid[r-1][c])
        if c < n-1 and not grid[r][c+1].is_barrier():
            self.neighbors.append(grid[r][c+1])
        if c > 0 and not grid[r][c-1].is_barrier():
            self.neighbors.append(grid[r][c-1])

    def __lt__(self,other):
        return False

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(parent,curr,draw):
    while curr in parent:
        curr = parent[curr]
        curr.make_path()
        draw()

def algorithm(draw,grid,start,end):
    que = PriorityQueue()
    que.put((0,start))
    parent = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    open_set = {start}

    while not que.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = que.get()[1]
        open_set.remove(curr)

        if curr == end:
            for row in grid:
                for spot in row:
                    if spot.is_open() or spot.is_closed():
                        spot.color = White
            reconstruct_path(parent,end,draw)
            end.make_end()
            return True
        
        for neighbor in curr.neighbors:
            temp_g = g_score[curr]+1
            if temp_g < g_score[neighbor]:
                parent[neighbor] = curr
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set:
                    que.put((f_score[neighbor],neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open()
        draw()

        if curr != start:
            curr.make_closed()

    return False
        


def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,Gray,(0,i*gap),(width,i*gap))
    for i in range(rows):
        pygame.draw.line(win,Gray,(i*gap,0),(i*gap,width))

def draw(win,grid,rows,width):
    win.fill(White)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    x,y = pos 
    row = x // gap
    col = y // gap
    return row,col

def main(win,width):
    Rows = 50
    grid = make_grid(Rows,width)
    start = None
    end = None
    run = True
    while run:
        draw(win,grid,Rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,Rows,width)
                if row >= 0 and row < Rows and col >= 0 and col < Rows:
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,Rows,width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                            if spot.is_path():
                                spot.color = White
                    algorithm(lambda: draw(win,grid,Rows,width),grid,start,end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(Rows,width)

    pygame.quit()

main(Win,Width)
                            

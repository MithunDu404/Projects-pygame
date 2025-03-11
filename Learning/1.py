import pygame
import sys
import random
import dictionary as mp

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 1: Interactive Grid System")

# Font for displaying text
font = pygame.font.SysFont('Arial', 15)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  
GRAY = (128, 128, 128)
PINK = (255, 192, 203)
PUPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

mp = {
    0: BLACK,
    1: ORANGE,
    2: PUPLE,
    3: PINK,
    4: BLUE,
    5: GREEN,
    6: RED,
    7: WHITE
}

GRID_SIZE = 40
Grid_Width = WIDTH // GRID_SIZE
Grid_Height = HEIGHT // GRID_SIZE

grid = [[0 for _ in range(Grid_Height)] for _ in range(Grid_Width)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0] // GRID_SIZE
            y = pos[1] // GRID_SIZE
            
            if 0 <= x < Grid_Width and 0 <= y < Grid_Height:
                grid[x][y] = 1 if grid[x][y] == 0 else 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for x in range(Grid_Width):
                    for y in range(Grid_Height):
                        grid[x][y] = random.randint(0, 7)
            elif event.key == pygame.K_r:
                for x in range(Grid_Width):
                    for y in range(Grid_Height):
                        grid[x][y] = 0
                

    screen.fill(BLACK)

    for x in range(Grid_Width):
        for y in range(Grid_Height):
            color = mp[grid[x][y]]
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Display instructions
    instructions = font.render("Click on cells to toggle their state", True, BLACK)
    screen.blit(instructions, (20, 20))

    # Display grid coordinates for educational purposes
    for x in range(Grid_Width):
        for y in range(Grid_Height):
            if grid[x][y] == 0:
                coords = font.render(f"{x},{y}", True, WHITE)
                screen.blit(coords, (x * GRID_SIZE + 5, y * GRID_SIZE + 10))

    pygame.display.update()

pygame.quit()
sys.exit()
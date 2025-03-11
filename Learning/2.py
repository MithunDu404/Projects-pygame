import pygame
import sys
import random
import dictionary as mp

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 2: Array Visualization")

# Font for displaying text
font = pygame.font.SysFont('Arial', 10)
font2 = pygame.font.SysFont('Arial', 15)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  
GRAY = (128, 128, 128)
PINK = (255, 192, 203)
PUPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

mp = {0: BLACK, 1: ORANGE, 2: PUPLE, 3: PINK, 4: BLUE, 5: GREEN, 6: RED, 7: WHITE}

def Genarate_Array(size,min = 5, max = 100):
    return [random.randint(min,max) for _ in range(size)] 

Array_size = 50
Array = Genarate_Array(Array_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Array = Genarate_Array(Array_size)
                
    screen.fill(BLACK)

    bar_width = (WIDTH-100)// Array_size
    for i,value in enumerate(Array):
        bar_height = 5*value
        x = 50 + i*bar_width
        y = HEIGHT - bar_height - 50
        pygame.draw.rect(screen, ORANGE, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, GRAY,(x,y,bar_width,bar_height),1)
        height = font.render(str(value), True, BLACK)
        screen.blit(height, (x+2, HEIGHT-65))

    # Draw instructions
    instructions = font2.render("Press R to generate a new array", True, WHITE)
    screen.blit(instructions, (20, 20))

    pygame.display.update()

pygame.quit()
sys.exit()
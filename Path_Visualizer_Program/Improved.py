import pygame
import math
import random
import time
from queue import PriorityQueue, Queue, LifoQueue

# Initialize pygame
pygame.init()

# Constants - INCREASED WINDOW WIDTH
WIDTH = 800  # Increased from 800 to 950
GRID_WIDTH = 750
UI_WIDTH = 250  # Now 250 instead of 100
WIN = pygame.display.set_mode((1000, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
PINK = (255, 192, 203)
LIGHT_GREY = (200, 200, 200)

# Fonts
FONT = pygame.font.SysFont('Arial', 16)
LARGE_FONT = pygame.font.SysFont('Arial', 20)

class Button:
    """Button class for UI elements"""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        """Initialize a button with position, size, text and colors"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_pressed = False
        
    def draw(self, win):
        """Draw the button on the window"""
        pygame.draw.rect(win, self.current_color, (self.x, self.y, self.width, self.height), 0, 5)
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 1, 5)  # Border
        text_surf = FONT.render(self.text, True, BLACK)
        win.blit(text_surf, (self.x + (self.width - text_surf.get_width()) // 2, 
                            self.y + (self.height - text_surf.get_height()) // 2))
        
    def is_over(self, pos):
        """Check if mouse position is over the button"""
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
    
    def update(self, pos):
        """Update button appearance based on mouse position"""
        if self.is_over(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
            
    def handle_event(self, event, pos):
        """Handle mouse events on the button"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(pos):
            self.is_pressed = True
            return True
        return False


class Spot:
    """Represents a cell in the grid"""
    
    def __init__(self, row, col, size, total_rows):
        """Initialize a spot with its position and properties"""
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows
        self.distance = float("inf")  # For Dijkstra
        self.parent = None  # For path reconstruction
        
    def get_pos(self):
        """Get the grid position (row, col) of the spot"""
        return self.row, self.col
    
    def is_open(self):
        """Check if spot is in the open set"""
        return self.color == TURQUOISE
    
    def is_closed(self):
        """Check if spot is in the closed set"""
        return self.color == GREEN
    
    def is_barrier(self):
        """Check if spot is a barrier"""
        return self.color == BLACK
    
    def is_start(self):
        """Check if spot is the start point"""
        return self.color == BLUE
    
    def is_end(self):
        """Check if spot is the end point"""
        return self.color == PURPLE
    
    def is_path(self):
        """Check if spot is part of the final path"""
        return self.color == RED
    
    def reset(self):
        """Reset the spot to its default state"""
        self.color = WHITE
        self.distance = float("inf")
        self.parent = None
        
    def make_open(self):
        """Mark spot as in the open set"""
        self.color = TURQUOISE
        
    def make_closed(self):
        """Mark spot as in the closed set"""
        self.color = GREEN
        
    def make_barrier(self):
        """Mark spot as a barrier"""
        self.color = BLACK
        
    def make_start(self):
        """Mark spot as the start point"""
        self.color = BLUE
        
    def make_end(self):
        """Mark spot as the end point"""
        self.color = PURPLE
        
    def make_path(self):
        """Mark spot as part of the final path"""
        self.color = RED
        
    def make_visited(self):
        """Mark spot as visited (for BFS/DFS)"""
        self.color = PINK
        
    def draw(self, win, offset=0):
        """Draw the spot on the window with an optional x-offset"""
        pygame.draw.rect(win, self.color, (self.x + offset, self.y, self.size, self.size))
        
    def update_neighbors(self, grid, allow_diagonal=False):
        """Update list of traversable neighboring spots"""
        self.neighbors = []
        # Check the four cardinal directions
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
            
        # If diagonal movement is allowed, add diagonal neighbors
        if allow_diagonal:
            # Down-Right
            if (self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and 
                not grid[self.row + 1][self.col + 1].is_barrier() and
                not grid[self.row + 1][self.col].is_barrier() and 
                not grid[self.row][self.col + 1].is_barrier()):
                self.neighbors.append(grid[self.row + 1][self.col + 1])
            # Down-Left
            if (self.row < self.total_rows - 1 and self.col > 0 and 
                not grid[self.row + 1][self.col - 1].is_barrier() and
                not grid[self.row + 1][self.col].is_barrier() and 
                not grid[self.row][self.col - 1].is_barrier()):
                self.neighbors.append(grid[self.row + 1][self.col - 1])
            # Up-Right
            if (self.row > 0 and self.col < self.total_rows - 1 and 
                not grid[self.row - 1][self.col + 1].is_barrier() and
                not grid[self.row - 1][self.col].is_barrier() and 
                not grid[self.row][self.col + 1].is_barrier()):
                self.neighbors.append(grid[self.row - 1][self.col + 1])
            # Up-Left
            if (self.row > 0 and self.col > 0 and 
                not grid[self.row - 1][self.col - 1].is_barrier() and
                not grid[self.row - 1][self.col].is_barrier() and 
                not grid[self.row][self.col - 1].is_barrier()):
                self.neighbors.append(grid[self.row - 1][self.col - 1])
                
    def __lt__(self, other):
        """Comparison method for priority queue ordering"""
        return False


class PathfindingVisualizer:
    """Main class for the pathfinding visualizer application"""
    
    def __init__(self, win, width):
        """Initialize the visualizer with window and dimensions"""
        self.win = win
        self.width = width
        self.grid_width = GRID_WIDTH
        self.ui_width = UI_WIDTH
        self.rows = 50
        self.grid = []
        self.start = None
        self.end = None
        self.allow_diagonal = False
        self.algorithm = "A*"
        self.running = False
        self.path_found = False
        self.nodes_visited = 0
        self.path_length = 0
        self.execution_time = 0
        self.visualization_speed = 25  # Milliseconds between frames
        self.maze_density = 0.65  # Controls how many walls are created (lower = fewer walls)
        
        # Create the buttons - increased width and adjusted spacing
        button_width = UI_WIDTH - 20  # Wider buttons
        button_height = 40  # Taller buttons for better text display
        button_spacing = 45  # Spacing between buttons
        self.buttons = [
            Button(GRID_WIDTH + 10, 50, button_width, button_height, "A* Algorithm", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + button_spacing, button_width, button_height, "Dijkstra Algorithm", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 2*button_spacing, button_width, button_height, "BFS Algorithm", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 3*button_spacing, button_width, button_height, "DFS Algorithm", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 4*button_spacing, button_width, button_height, "Toggle Diagonal", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 5*button_spacing, button_width, button_height, "Generate Maze", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 6*button_spacing, button_width, button_height, "Clear Grid", LIGHT_GREY, TURQUOISE),
            Button(GRID_WIDTH + 10, 50 + 7*button_spacing, button_width, button_height, "Start Algorithm", GREEN, TURQUOISE),
        ]
        
        self.make_grid()
        
    def make_grid(self):
        """Create a grid of Spot objects"""
        self.grid = []
        gap = self.grid_width // self.rows
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                spot = Spot(i, j, gap, self.rows)
                self.grid[i].append(spot)
                
    def draw_grid_lines(self):
        """Draw the grid lines"""
        gap = self.grid_width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.grid_width, i * gap))
            pygame.draw.line(self.win, GREY, (i * gap, 0), (i * gap, self.grid_width))
            
    def draw_ui(self):
        """Draw the user interface panel"""
        # Draw UI background
        pygame.draw.rect(self.win, WHITE, (self.grid_width, 0, self.ui_width, self.width))
        pygame.draw.line(self.win, GREY, (self.grid_width, 0), (self.grid_width, self.width), 2)
        
        # Draw title
        title = LARGE_FONT.render("Pathfinding Visualizer Controls", True, BLACK)
        self.win.blit(title, (self.grid_width + (self.ui_width - title.get_width()) // 2, 10))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.win)
            
        # Draw current algorithm and settings
        # Create a box for metrics - INCREASED HEIGHT FOR TEXT
        metrics_y = 50 + 8*45  # Position after all buttons
        metrics_height = 180  # Increased from 150 to 180
        pygame.draw.rect(self.win, LIGHT_GREY, 
                        (self.grid_width + 10, metrics_y, self.ui_width - 20, metrics_height), 0, 5)
        
        # Current algorithm info - INCREASED LINE SPACING
        padding = 15  # Increased left padding
        line_height = 30  # Increased from 25 to 30
        
        y_offset = metrics_y + 10
        curr_algo = FONT.render(f"Current Algorithm: {self.algorithm}", True, BLACK)
        self.win.blit(curr_algo, (self.grid_width + padding, y_offset))
        
        y_offset += line_height
        diag_text = "Enabled" if self.allow_diagonal else "Disabled"
        diagonal = FONT.render(f"Diagonal Movement: {diag_text}", True, BLACK)
        self.win.blit(diagonal, (self.grid_width + padding, y_offset))
        
        y_offset += line_height
        density = FONT.render(f"Maze Density: {int(self.maze_density * 100)}%", True, BLACK)
        self.win.blit(density, (self.grid_width + padding, y_offset))
        
        # Performance metrics
        if self.path_found:
            metrics = [
                f"Nodes Visited: {self.nodes_visited}",
                f"Path Length: {self.path_length}",
                f"Execution Time: {self.execution_time:.4f} s"
            ]
            for metric in metrics:
                y_offset += line_height
                text = FONT.render(metric, True, BLACK)
                self.win.blit(text, (self.grid_width + padding, y_offset))
                
        # Instructions
        instr_y = metrics_y + metrics_height + 10
        instr_height = 160  # Increased height for instructions
        pygame.draw.rect(self.win, LIGHT_GREY, 
                        (self.grid_width + 10, instr_y, self.ui_width - 20, instr_height), 0, 5)
                        
        instructions = [
            "Left Click: Place start/end/barriers",
            "Right Click: Remove spot",
            "Space: Run algorithm",
            "C: Clear the grid",
            "+/-: Adjust maze density"
        ]
        
        # Draw instruction title
        instr_title = FONT.render("Keyboard & Mouse Controls:", True, BLACK)
        self.win.blit(instr_title, (self.grid_width + padding, instr_y + 10))
        
        # Draw instructions with more spacing
        for i, instr in enumerate(instructions):
            text = FONT.render(instr, True, BLACK)
            self.win.blit(text, (self.grid_width + padding, instr_y + 35 + i * 25))
            
    def draw(self):
        """Draw the entire application window"""
        self.win.fill(WHITE)
        
        # Draw all spots
        for row in self.grid:
            for spot in row:
                spot.draw(self.win)
                
        self.draw_grid_lines()
        self.draw_ui()
        pygame.display.update()
        
    def get_clicked_pos(self, pos):
        """Convert mouse position to grid position"""
        if pos[0] >= self.grid_width:  # Click is in UI area
            return None, None
            
        gap = self.grid_width // self.rows
        x, y = pos
        row = x // gap
        col = y // gap
        return row, col
        
    def clear_grid(self, keep_barriers=False):
        """Clear the grid, optionally keeping barriers"""
        for row in self.grid:
            for spot in row:
                if keep_barriers and spot.is_barrier():
                    continue
                spot.reset()
                
        self.start = None
        self.end = None
        self.path_found = False
        self.nodes_visited = 0
        self.path_length = 0
        self.execution_time = 0
        
    def update_neighbors(self):
        """Update neighbors for all spots in the grid"""
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid, self.allow_diagonal)
                
    def reconstruct_path(self, current):
        """Reconstruct and visualize the path from start to end"""
        path_length = 0
        while current != self.start:
            current = current.parent
            if current != self.start:
                current.make_path()
                path_length += 1
                
        self.path_length = path_length
        return path_length
                
    def heuristic(self, p1, p2):
        """Calculate the Manhattan distance heuristic"""
        x1, y1 = p1
        x2, y2 = p2
        if self.allow_diagonal:
            # Chebyshev distance for diagonal movement
            return max(abs(x1 - x2), abs(y1 - y2))
        else:
            # Manhattan distance for 4-connectivity
            return abs(x1 - x2) + abs(y1 - y2)
            
    def astar(self):
        """Implement the A* algorithm"""
        self.nodes_visited = 0
        start_time = time.time()
        
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        open_set_hash = {self.start}
        
        # Initialize distances
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[self.start] = 0
        
        # Initialize estimated total cost
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[self.start] = self.heuristic(self.start.get_pos(), self.end.get_pos())
        
        while not open_set.empty():
            # Check for pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    
            # Get the node with lowest f_score
            current = open_set.get()[2]
            open_set_hash.remove(current)
            
            # If we reached the end
            if current == self.end:
                self.execution_time = time.time() - start_time
                path_length = self.reconstruct_path(current)
                self.end.make_end()
                self.start.make_start()
                self.path_found = True
                return True
                
            # Process neighbors
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1  # Assume uniform cost of 1
                
                # If we found a better path
                if temp_g_score < g_score[neighbor]:
                    neighbor.parent = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor.get_pos(), self.end.get_pos())
                    
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
                        self.nodes_visited += 1
                        
            # Update display
            self.draw()
            pygame.time.delay(self.visualization_speed)
            
            if current != self.start:
                current.make_closed()
                
        # No path found
        self.execution_time = time.time() - start_time
        self.path_found = False
        return False
        
    def dijkstra(self):
        """Implement Dijkstra's algorithm"""
        self.nodes_visited = 0
        start_time = time.time()
        
        # Initialize priority queue with start node
        pq = PriorityQueue()
        pq.put((0, 0, self.start))  # (distance, count, node)
        
        # Distance dictionary
        distances = {spot: float("inf") for row in self.grid for spot in row}
        distances[self.start] = 0
        
        # For tracking which nodes are in queue
        in_queue = {self.start}
        count = 0
        
        while not pq.empty():
            # Check for pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    
            # Get the node with lowest distance
            current_distance, _, current = pq.get()
            in_queue.remove(current)
            
            # If we reached the end
            if current == self.end:
                self.execution_time = time.time() - start_time
                self.reconstruct_path(current)
                self.end.make_end()
                self.start.make_start()
                self.path_found = True
                return True
                
            # Process neighbors
            for neighbor in current.neighbors:
                distance = current_distance + 1  # Uniform cost of 1
                
                # If we found a better path
                if distance < distances[neighbor]:
                    neighbor.parent = current
                    distances[neighbor] = distance
                    
                    if neighbor not in in_queue:
                        count += 1
                        pq.put((distance, count, neighbor))
                        in_queue.add(neighbor)
                        neighbor.make_open()
                        self.nodes_visited += 1
                        
            # Update display
            self.draw()
            pygame.time.delay(self.visualization_speed)
            
            if current != self.start:
                current.make_closed()
                
        # No path found
        self.execution_time = time.time() - start_time
        self.path_found = False
        return False
        
    def bfs(self):
        """Implement Breadth-First Search algorithm"""
        self.nodes_visited = 0
        start_time = time.time()
        
        # Initialize queue with start node
        queue = Queue()
        queue.put(self.start)
        visited = {self.start}
        
        while not queue.empty():
            # Check for pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    
            # Get the next node
            current = queue.get()
            
            # If we reached the end
            if current == self.end:
                self.execution_time = time.time() - start_time
                self.reconstruct_path(current)
                self.end.make_end()
                self.start.make_start()
                self.path_found = True
                return True
                
            # Process neighbors
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    neighbor.parent = current
                    visited.add(neighbor)
                    queue.put(neighbor)
                    neighbor.make_open()
                    self.nodes_visited += 1
                    
            # Update display
            self.draw()
            pygame.time.delay(self.visualization_speed)
            
            if current != self.start:
                current.make_closed()
                
        # No path found
        self.execution_time = time.time() - start_time
        self.path_found = False
        return False
        
    def dfs(self):
        """Implement Depth-First Search algorithm"""
        self.nodes_visited = 0
        start_time = time.time()
        
        # Initialize stack with start node
        stack = LifoQueue()
        stack.put(self.start)
        visited = {self.start}
        
        while not stack.empty():
            # Check for pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    
            # Get the next node
            current = stack.get()
            
            # If we reached the end
            if current == self.end:
                self.execution_time = time.time() - start_time
                self.reconstruct_path(current)
                self.end.make_end()
                self.start.make_start()
                self.path_found = True
                return True
                
            # Process neighbors
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    neighbor.parent = current
                    visited.add(neighbor)
                    stack.put(neighbor)
                    neighbor.make_open()
                    self.nodes_visited += 1
                    
            # Update display
            self.draw()
            pygame.time.delay(self.visualization_speed)
            
            if current != self.start:
                current.make_closed()
                
        # No path found
        self.execution_time = time.time() - start_time
        self.path_found = False
        return False
        
    def is_path_possible(self, start_pos, end_pos):
        """Check if a path is possible between start and end positions"""
        # Using BFS to check for path existence
        queue = Queue()
        visited = set()
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        if (start_row < 0 or start_row >= self.rows or 
            start_col < 0 or start_col >= self.rows or
            end_row < 0 or end_row >= self.rows or
            end_col < 0 or end_col >= self.rows):
            return False
            
        start_spot = self.grid[start_row][start_col]
        end_spot = self.grid[end_row][end_col]
        
        if start_spot.is_barrier() or end_spot.is_barrier():
            return False
            
        queue.put(start_spot)
        visited.add(start_spot)
        
        # Update neighbors first to ensure they're available
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid, False)  # No diagonal for pathfinding check
                
        while not queue.empty():
            current = queue.get()
            
            if current == end_spot:
                return True
                
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put(neighbor)
                    
        return False
        
    def generate_maze(self):
        """Generate a maze with improved navigability"""
        self.clear_grid()
        
        # Randomly place barriers based on density
        for row in range(1, self.rows - 1):
            for col in range(1, self.rows - 1):
                if random.random() < self.maze_density * 0.3:  # Use lower density for random barriers
                    self.grid[row][col].make_barrier()
                    
        # Create more structured maze sections
        # This approach creates fewer continuous walls with more paths available
        def create_maze_section(start_x, start_y, width, height):
            if width < 4 or height < 4:
                return
                
            # Choose orientation - vertical or horizontal wall
            if width > height:
                # Vertical wall
                wall_x = start_x + random.randint(1, width - 2)
                # Create a gap in the wall
                gap_y = start_y + random.randint(0, height - 1)
                
                # Probability of creating this wall segment
                if random.random() < self.maze_density:
                    # Place wall
                    for y in range(start_y, start_y + height):
                        if y != gap_y and not self.grid[wall_x][y].is_barrier():
                            self.grid[wall_x][y].make_barrier()
                            
                    # Draw and pause
                    self.draw()
                    pygame.time.delay(2)
                    
                # Recursive calls for sub-sections
                if width > 5:  # Only divide further if enough space
                    create_maze_section(start_x, start_y, wall_x - start_x, height)
                    create_maze_section(wall_x + 1, start_y, start_x + width - wall_x - 1, height)
            else:
                # Horizontal wall
                wall_y = start_y + random.randint(1, height - 2)
                # Create a gap in the wall
                gap_x = start_x + random.randint(0, width - 1)
                
                # Probability of creating this wall segment
                if random.random() < self.maze_density:
                    # Place wall
                    for x in range(start_x, start_x + width):
                        if x != gap_x and not self.grid[x][wall_y].is_barrier():
                            self.grid[x][wall_y].make_barrier()
                            
                    # Draw and pause
                    self.draw()
                    pygame.time.delay(2)
                    
                # Recursive calls for sub-sections
                if height > 5:  # Only divide further if enough space
                    create_maze_section(start_x, start_y, width, wall_y - start_y)
                    create_maze_section(start_x, wall_y + 1, width, start_y + height - wall_y - 1)
                    
        # Start creating the maze
        create_maze_section(1, 1, self.rows - 2, self.rows - 2)
        
        # Make sure there's a good area for start and end points
        # Clear some space in corners
        corners = [
            (1, 1, 3, 3),  # Top-left
            (1, self.rows-4, 3, 3),  # Bottom-left
            (self.rows-4, 1, 3, 3),  # Top-right
            (self.rows-4, self.rows-4, 3, 3)  # Bottom-right
        ]
        
        for x, y, w, h in corners:
            for i in range(x, x + w):
                for j in range(y, y + h):
                    if random.random() < 0.7:  # 70% chance to clear
                        self.grid[i][j].reset()
                        
        # Check and fix maze navigability
        self.ensure_navigable_maze()
        
    def ensure_navigable_maze(self):
        """Make sure the maze has possible paths by removing some barriers if needed"""
        # Attempt to clear paths if random start/end positions can't be connected
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            # Choose random start and end positions
            start_row, start_col = random.randint(1, self.rows-2), random.randint(1, self.rows-2)
            end_row, end_col = random.randint(1, self.rows-2), random.randint(1, self.rows-2)
            
            # Make sure start and end are not the same and not barriers
            if (abs(start_row - end_row) + abs(start_col - end_col) < self.rows // 3):
                continue  # Too close, try again
                
            if self.grid[start_row][start_col].is_barrier():
                self.grid[start_row][start_col].reset()
                
            if self.grid[end_row][end_col].is_barrier():
                self.grid[end_row][end_col].reset()
                
            # Check if a path exists
            if self.is_path_possible((start_row, start_col), (end_row, end_col)):
                # If a path exists, we have a good maze
                break
                
            # No path found, remove some barriers
            if attempts > max_attempts // 2:
                # Remove more barriers as attempts increase
                barrier_removal_count = int(self.rows * self.rows * 0.05)  # Remove 5% of barriers
                barriers_removed = 0
                
                while barriers_removed < barrier_removal_count:
                    r, c = random.randint(1, self.rows-2), random.randint(1, self.rows-2)
                    if self.grid[r][c].is_barrier():
                        self.grid[r][c].reset()
                        barriers_removed += 1
                        
            attempts += 1
            
        # If all attempts failed, remove a significant number of barriers
        if attempts >= max_attempts:
            barrier_removal_count = int(self.rows * self.rows * 0.2)  # Remove 20% of barriers
            barriers_removed = 0
            
            while barriers_removed < barrier_removal_count:
                r, c = random.randint(1, self.rows-2), random.randint(1, self.rows-2)
                if self.grid[r][c].is_barrier():
                    self.grid[r][c].reset()
                    barriers_removed += 1
        
    def run_algorithm(self):
        """Run the selected algorithm"""
        if not self.start or not self.end:
            return
            
        # Reset the path and visited nodes, but keep barriers
        for row in self.grid:
            for spot in row:
                if spot != self.start and spot != self.end and not spot.is_barrier():
                    spot.reset()
                    
        # Update neighbors
        self.update_neighbors()
        
        # Run the selected algorithm
        if self.algorithm == "A*":
            return self.astar()
        elif self.algorithm == "Dijkstra":
            return self.dijkstra()
        elif self.algorithm == "BFS":
            return self.bfs()
        elif self.algorithm == "DFS":
            return self.dfs()
        
    def run(self):
        """Main loop for the visualizer"""
        self.running = True
        
        while self.running:
            # Draw the current state
            self.draw()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # Mouse position
                pos = pygame.mouse.get_pos()
                
                # Update buttons
                for button in self.buttons:
                    button.update(pos)
                    
                # Handle mouse clicks
                if pygame.mouse.get_pressed()[0]:  # Left click
                    # Check if clicked on UI button
                    for i, button in enumerate(self.buttons):
                        if button.handle_event(event, pos):
                            # Handle button actions
                            if i == 0:  # A* Algorithm
                                self.algorithm = "A*"
                            elif i == 1:  # Dijkstra Algorithm
                                self.algorithm = "Dijkstra"
                            elif i == 2:  # BFS Algorithm
                                self.algorithm = "BFS"
                            elif i == 3:  # DFS Algorithm
                                self.algorithm = "DFS"
                            elif i == 4:  # Toggle Diagonal
                                self.allow_diagonal = not self.allow_diagonal
                            elif i == 5:  # Generate Maze
                                self.generate_maze()
                            elif i == 6:  # Clear Grid
                                self.clear_grid()
                            elif i == 7:  # Start Algorithm
                                self.run_algorithm()
                                
                    # Check if clicked on grid
                    row, col = self.get_clicked_pos(pos)
                    if row is not None and col is not None:
                        spot = self.grid[row][col]
                        # Place start, end or barrier
                        if not self.start and spot != self.end:
                            self.start = spot
                            self.start.make_start()
                        elif not self.end and spot != self.start:
                            self.end = spot
                            self.end.make_end()
                        elif spot != self.end and spot != self.start:
                            spot.make_barrier()
                            
                elif pygame.mouse.get_pressed()[2]:  # Right click
                    row, col = self.get_clicked_pos(pos)
                    if row is not None and col is not None:
                        spot = self.grid[row][col]
                        spot.reset()
                        if spot == self.start:
                            self.start = None
                        elif spot == self.end:
                            self.end = None
                            
                # Keyboard shortcuts
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        # Run the algorithm
                        self.run_algorithm()
                        
                    if event.key == pygame.K_c:
                        # Clear the grid
                        self.clear_grid()
                        
                    if event.key == pygame.K_m:
                        # Generate maze
                        self.generate_maze()
                        
                    if event.key == pygame.K_d:
                        # Toggle diagonal movement
                        self.allow_diagonal = not self.allow_diagonal
                        
                    # Adjust maze density
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                        self.maze_density = min(0.9, self.maze_density + 0.05)
                        
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.maze_density = max(0.1, self.maze_density - 0.05)
                        
        pygame.quit()


def main():
    """Main function to start the application"""
    visualizer = PathfindingVisualizer(WIN, WIDTH)
    visualizer.run()


if __name__ == "__main__":
    main()

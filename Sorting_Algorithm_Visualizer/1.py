import pygame
import random
import math
pygame.init()

class DrawInformation:
    # Basic colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    YELLOW = 255, 255, 0
    PURPLE = 128, 0, 128
    ORANGE = 255, 165, 0
    
    # Themes
    THEMES = {
        "Default": {
            "background": (255, 255, 255),
            "text": (0, 0, 0),
            "highlight1": (0, 255, 0),  # GREEN
            "highlight2": (255, 0, 0),  # RED
            "pivot": (0, 0, 255),       # BLUE
            "gradients": [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
        },
        "Dark": {
            "background": (40, 44, 52),
            "text": (171, 178, 191),
            "highlight1": (152, 195, 121),
            "highlight2": (224, 108, 117),
            "pivot": (97, 175, 239),
            "gradients": [(86, 92, 100), (92, 99, 112), (99, 109, 131)]
        },
        "Colorful": {
            "background": (245, 245, 245),
            "text": (50, 50, 50),
            "highlight1": (46, 204, 113),
            "highlight2": (231, 76, 60),
            "pivot": (52, 152, 219),
            "gradients": [(241, 148, 138), (162, 217, 206), (133, 193, 233)]
        }
    }
    
    FONT = pygame.font.SysFont('Georgia', 20)
    LARGE_FONT = pygame.font.SysFont('Verdana', 30)

    SIDE_PAD = 100
    TOP_PAD = 200  # Increased to give more space for UI elements
    BOTTOM_PAD = 60  # Space for metrics at the bottom

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.current_theme = "Default"
        
        # Set initial colors from theme
        self.set_theme(self.current_theme)
        
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_theme(self, theme_name):
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            theme = self.THEMES[theme_name]
            self.BACKGROUND_COLOR = theme["background"]
            self.TEXT_COLOR = theme["text"]
            self.HIGHLIGHT1 = theme["highlight1"]
            self.HIGHLIGHT2 = theme["highlight2"]
            self.PIVOT = theme["pivot"]
            self.GRADIENTS = theme["gradients"]
            return True
        return False
    
    def next_theme(self):
        themes = list(self.THEMES.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.set_theme(themes[next_index])
        return self.current_theme

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # Adjust the height calculation to leave room at the bottom
        available_height = self.height - self.TOP_PAD - self.BOTTOM_PAD
        self.block_height = math.floor(available_height / (self.max_val - self.min_val + 1))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending, speed, comparisons=0, swaps=0, distribution_name="Random"):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Title with sorting direction
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    # Controls information
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    # Algorithm selection controls
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | Q - Quick Sort | M - Merge Sort | S - Selection Sort", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    # Speed and size controls
    speed_txt = draw_info.FONT.render(f"Speed: {speed:.1f}x (+ / - to adjust)", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(speed_txt, (draw_info.width/2 - speed_txt.get_width()/2, 105))
    
    # Array size
    size_txt = draw_info.FONT.render(f"Array Size: {len(draw_info.lst)} ([ / ] to adjust)", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(size_txt, (draw_info.width/2 - size_txt.get_width()/2, 135))
    
    # Distribution info
    dist_txt = draw_info.FONT.render(f"Distribution: {distribution_name} (P to change)", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(dist_txt, (20, 20))
    
    # Theme info
    theme_txt = draw_info.FONT.render(f"Theme: {draw_info.current_theme} (T to change)", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(theme_txt, (draw_info.width - 280, 20))
    
    # Algorithm description - Moved to above the array visualization
    algorithm_descriptions = {
        "Bubble Sort": "O(n²) - Simple comparison-based algorithm that repeatedly steps through the list, comparing adjacent elements.",
        "Insertion Sort": "O(n²) - Builds the final sorted array one item at a time, efficient for small data sets.",
        "Quick Sort": "O(n log n) average - Divides array around pivot, recursively sorts the sub-arrays.",
        "Merge Sort": "O(n log n) - Divides array, sorts the parts recursively, then merges them.",
        "Selection Sort": "O(n²) - Repeatedly finds the minimum element and places it at the beginning."
    }
    
    if algo_name in algorithm_descriptions:
        algo_desc = draw_info.FONT.render(algorithm_descriptions[algo_name], 1, draw_info.TEXT_COLOR)
        draw_info.window.blit(algo_desc, (draw_info.width/2 - algo_desc.get_width()/2, 165))
    
    # Performance metrics - Position at the bottom of the window
    metrics = draw_info.FONT.render(f"Comparisons: {comparisons} | Swaps: {swaps}", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(metrics, (draw_info.width/2 - metrics.get_width()/2, draw_info.height - 30))

    # Draw the actual list visualization
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                     draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD - draw_info.BOTTOM_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - draw_info.BOTTOM_PAD - (val - draw_info.min_val + 1) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height - y - draw_info.BOTTOM_PAD))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def generate_nearly_sorted_list(n, min_val, max_val, swap_percent=10):
    lst = sorted(generate_starting_list(n, min_val, max_val))
    swaps = int((n * swap_percent) / 100)
    
    for _ in range(swaps):
        i = random.randint(0, n-2)
        lst[i], lst[i+1] = lst[i+1], lst[i]
        
    return lst


def generate_reversed_list(n, min_val, max_val):
    return sorted(generate_starting_list(n, min_val, max_val), reverse=True)


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    comparisons = 0
    swaps = 0

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            comparisons += 1

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swaps += 1
                draw_list(draw_info, {j: draw_info.HIGHLIGHT1, j + 1: draw_info.HIGHLIGHT2}, True)
                yield comparisons, swaps

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    comparisons = 0
    swaps = 0

    for i in range(1, len(lst)):
        current = lst[i]
        j = i
        comparisons += 1

        while j > 0 and ((lst[j - 1] > current and ascending) or (lst[j - 1] < current and not ascending)):
            lst[j] = lst[j - 1]
            j -= 1
            swaps += 1
            comparisons += 1
            draw_list(draw_info, {j: draw_info.HIGHLIGHT1, j - 1: draw_info.HIGHLIGHT2}, True)
            yield comparisons, swaps

        lst[j] = current
        draw_list(draw_info, {j: draw_info.HIGHLIGHT1}, True)
        yield comparisons, swaps

    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    comparisons = 0
    swaps = 0
    
    for i in range(len(lst)):
        min_idx = i
        
        for j in range(i + 1, len(lst)):
            comparisons += 1
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j
                # Add visualization for comparisons too
                draw_list(draw_info, {j: draw_info.HIGHLIGHT2, min_idx: draw_info.HIGHLIGHT1}, True)
                yield comparisons, swaps
                
        if i != min_idx:
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            swaps += 1
            draw_list(draw_info, {i: draw_info.HIGHLIGHT1, min_idx: draw_info.HIGHLIGHT2}, True)
            yield comparisons, swaps



def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    temp_arr = lst.copy()
    comparisons = 0
    swaps = 0
    
    def merge(arr, temp, left, mid, right):
        nonlocal comparisons, swaps
        i = left      # Starting index of left subarray
        j = mid + 1   # Starting index of right subarray
        k = left      # Starting index of merged subarray
        
        while i <= mid and j <= right:
            comparisons += 1
            if (arr[i] <= arr[j] and ascending) or (arr[i] >= arr[j] and not ascending):
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                swaps += (mid - i + 1)  # Count inversions
                j += 1
            k += 1
            
        # Copy remaining elements
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
            
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
            
        # Copy back to original array
        for i in range(left, right + 1):
            arr[i] = temp[i]
            draw_list(draw_info, {i: draw_info.HIGHLIGHT1}, True)
            yield
    
    def merge_sort_helper(arr, temp, left, right):
        if left < right:
            mid = (left + right) // 2
            
            # Sort first and second halves
            yield from merge_sort_helper(arr, temp, left, mid)
            yield from merge_sort_helper(arr, temp, mid + 1, right)
            yield from merge(arr, temp, left, mid, right)
    
    yield from merge_sort_helper(lst, temp_arr, 0, len(lst) - 1)
    
    # Final yield with updated metrics
    yield comparisons, swaps
    return lst


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    comparisons = 0
    swaps = 0
    
    def partition(arr, low, high):
        nonlocal comparisons, swaps
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            comparisons += 1
            if (arr[j] <= pivot and ascending) or (arr[j] >= pivot and not ascending):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                draw_list(draw_info, {i: draw_info.HIGHLIGHT1, j: draw_info.HIGHLIGHT2, high: draw_info.PIVOT}, True)
                yield comparisons, swaps
                
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        draw_list(draw_info, {i + 1: draw_info.HIGHLIGHT1, high: draw_info.HIGHLIGHT2}, True)
        yield comparisons, swaps
        return i + 1  # Return pivot index via generator's StopIteration
    
    def quick_sort_helper(arr, low, high):
        if low < high:
            # Create partition generator
            partition_gen = partition(arr, low, high)
            
            # Process partition steps and get pivot index
            try:
                while True:
                    comp_swaps = next(partition_gen)
                    yield comp_swaps  # Yield comparison/swap counts
            except StopIteration as e:
                pivot_index = e.value  # Get pivot index from generator return

            # Recursively sort left and right partitions
            yield from quick_sort_helper(arr, low, pivot_index - 1)
            yield from quick_sort_helper(arr, pivot_index + 1, high)
    
    # Start the sorting process
    yield from quick_sort_helper(lst, 0, len(lst) - 1)
    return lst



def main():
    # Initial setup
    run = True
    clock = pygame.time.Clock()

    # List parameters
    n = 50
    min_val = 0
    max_val = 100
    
    # Algorithm state
    sorting = False
    ascending = True
    speed = 1.0
    comparisons = 0
    swaps = 0

    # Distribution options
    distributions = ["Random", "Nearly Sorted", "Reversed"]
    current_distribution = 0
    
    # Generate initial list
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1200, 760, lst)  # Increased window size for better layout
    
    # Algorithm selection
    sorting_algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Selection Sort": selection_sort
    }
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm = sorting_algorithms[sorting_algo_name]
    sorting_algorithm_generator = None

    while run:
        # Adjust speed dynamically
        clock.tick(60 * speed)

        if sorting:
            try:
                result = next(sorting_algorithm_generator)
                if isinstance(result, tuple) and len(result) == 2:
                    comparisons, swaps = result
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, speed, comparisons, swaps, distributions[current_distribution])

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # Reset list
            if event.key == pygame.K_r:
                sorting = False
                if distributions[current_distribution] == "Random":
                    lst = generate_starting_list(n, min_val, max_val)
                elif distributions[current_distribution] == "Nearly Sorted":
                    lst = generate_nearly_sorted_list(n, min_val, max_val)
                else:  # Reversed
                    lst = generate_reversed_list(n, min_val, max_val)
                draw_info.set_list(lst)
                comparisons = 0
                swaps = 0
            
            # Start sorting
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            
            # Change sort direction
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            # Change algorithm
            elif event.key == pygame.K_i and not sorting:
                sorting_algo_name = "Insertion Sort"
                sorting_algorithm = sorting_algorithms[sorting_algo_name]
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_b and not sorting:
                sorting_algo_name = "Bubble Sort"
                sorting_algorithm = sorting_algorithms[sorting_algo_name]
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_q and not sorting:
                sorting_algo_name = "Quick Sort"
                sorting_algorithm = sorting_algorithms[sorting_algo_name]
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_m and not sorting:
                sorting_algo_name = "Merge Sort"
                sorting_algorithm = sorting_algorithms[sorting_algo_name]
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_s and not sorting:
                sorting_algo_name = "Selection Sort"
                sorting_algorithm = sorting_algorithms[sorting_algo_name]
                comparisons = 0
                swaps = 0
            
            # Adjust speed
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                speed = min(10.0, speed + 0.5)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                speed = max(0.1, speed - 0.5)
            
            # Adjust array size
            elif event.key == pygame.K_LEFTBRACKET and not sorting:
                n = max(10, n - 10)
                if distributions[current_distribution] == "Random":
                    lst = generate_starting_list(n, min_val, max_val)
                elif distributions[current_distribution] == "Nearly Sorted":
                    lst = generate_nearly_sorted_list(n, min_val, max_val)
                else:  # Reversed
                    lst = generate_reversed_list(n, min_val, max_val)
                draw_info.set_list(lst)
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_RIGHTBRACKET and not sorting:
                n = min(300, n + 10)
                if distributions[current_distribution] == "Random":
                    lst = generate_starting_list(n, min_val, max_val)
                elif distributions[current_distribution] == "Nearly Sorted":
                    lst = generate_nearly_sorted_list(n, min_val, max_val)
                else:  # Reversed
                    lst = generate_reversed_list(n, min_val, max_val)
                draw_info.set_list(lst)
                comparisons = 0
                swaps = 0
            
            # Change distribution
            elif event.key == pygame.K_p and not sorting:
                current_distribution = (current_distribution + 1) % len(distributions)
                if distributions[current_distribution] == "Random":
                    lst = generate_starting_list(n, min_val, max_val)
                elif distributions[current_distribution] == "Nearly Sorted":
                    lst = generate_nearly_sorted_list(n, min_val, max_val)
                else:  # Reversed
                    lst = generate_reversed_list(n, min_val, max_val)
                draw_info.set_list(lst)
                comparisons = 0
                swaps = 0
            
            # Change theme
            elif event.key == pygame.K_t and not sorting:
                draw_info.next_theme()

    pygame.quit()


if __name__ == "__main__":
    main()

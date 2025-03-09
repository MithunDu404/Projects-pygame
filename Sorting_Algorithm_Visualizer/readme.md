# Sorting Algorithm Visualizer

A Python-based visualization tool demonstrating the mechanics of different sorting algorithms. This interactive application allows users to observe how various sorting algorithms operate, compare their efficiency, and understand their behavior under different data distributions.

## Features

### Multiple Sorting Algorithms
- **Bubble Sort** (O(n²))
- **Insertion Sort** (O(n²))
- **Selection Sort** (O(n²))
- **Merge Sort** (O(n log n))
- **Quick Sort** (O(n log n) average case)

### Interactive Controls
- Adjust visualization speed
- Change array size
- Select different initial data distributions
- Switch between ascending and descending order

### Visual Elements
- Color-coded array elements
- Highlighted comparisons and swaps
- Multiple color themes (Default, Dark, Colorful)

### Performance Metrics
- Real-time tracking of comparisons and swaps
- Visual execution time measurement

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/sorting-algorithm-visualizer.git
   cd sorting-algorithm-visualizer
   ```
2. Install required dependencies:
   ```bash
   pip install pygame
   ```
3. Run the application:
   ```bash
   python visualizer.py
   ```

## Usage

When you launch the application, you'll see a visualization of randomly generated arrays. Use the keyboard controls to interact with the visualizer.

### Controls

#### Algorithm Selection:
- **B** - Bubble Sort
- **I** - Insertion Sort
- **S** - Selection Sort
- **M** - Merge Sort
- **Q** - Quick Sort

#### Visualization Controls:
- **SPACE** - Start/Pause sorting
- **R** - Reset with new values
- **A** - Switch to ascending order
- **D** - Switch to descending order
- **+** - Increase visualization speed
- **-** - Decrease visualization speed

#### Array Options:
- **[** - Decrease array size
- **]** - Increase array size
- **P** - Cycle through data distributions (Random, Nearly Sorted, Reversed)

#### Appearance:
- **T** - Change theme (Default, Dark, Colorful)

## Understanding the Visualization

### Colors:
- **Gray bars**: Unsorted elements
- **Green highlights**: Elements being compared/swapped
- **Red highlights**: Current element being placed
- **Blue highlights**: Pivot elements (in Quick Sort)

### Performance Metrics:
- **Comparisons**: Number of times elements are compared
- **Swaps**: Number of times elements are swapped

## Data Distributions
- **Random**: Completely random array values
- **Nearly Sorted**: Array that is mostly in order with a few elements out of place
- **Reversed**: Array sorted in reverse order

## Contributing

Contributions are welcome! Here are some ways you can contribute:
- Add new sorting algorithms
- Improve visualization effects
- Optimize existing code
- Add new features

Please feel free to submit a pull request.

## Acknowledgements

- Inspired by various sorting algorithm visualizations
- Built with Python and Pygame
- Created as an educational tool to help understand sorting algorithms and their efficiency.



# Maze Solver GUI

A maze-solver GUI program built using the **Python** programming language and the `customtkinter` library. The application implements both **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** algorithms to visualize pathfinding in a maze. It is executed using **Python** and managed with **Poetry** for dependency handling. This program is released under the **MIT License**.

## Features

- Interactive maze generation and solving interface  
- Visualization of BFS and DFS algorithms in real time  
- Adjustable maze size and algorithm selection  
- Simple and lightweight GUI using `customtkinter`
- Import maze data from .txt file

## Requirements

Make sure the following are installed on your system:
- Python 3.10 or newer  
- Poetry (for dependency management)  

## Installation & Run

1. **Clone this repository**
    ```shell
    git clone https://github.com/naufalhanif25/maze-solver-gui.git
    cd maze-solver-gui
    ```

2. **Install dependencies**
    Install the dependencies using Poetry
    ```shell
    poetry install
    ```
    or install `customtkinter` using pip
    ```
    pip install customtkinter
    ```

3. **Run the program**
    Run the program using `./run.sh`
    ```shell
    chmod +x run.sh
    ./run.sh
    ```
    or run the program using **Poetry**
    ```shell
    poetry run python main.py
    ```
    or run the program using **Python** if you are not using **Poetry**
    ```shell
    python main.py
    ```

**Note**
We also provide maze data at `public/maze.txt` as an example.

## Preview
Below is a preview of the Maze Solver GUI interface in action.
[![nKIgqJ.preview.png](https://i.im.ge/2025/10/24/nKIgqJ.preview.png)](https://im.ge/i/nKIgqJ)
🚀 AI Pathfinder – Uninformed Search Visualizer
GOOD PERFORMANCE TIME APP

An interactive desktop visualization of six fundamental Uninformed Search Algorithms implemented in Python using Matplotlib.

This project demonstrates how different blind search strategies explore a structured grid environment to reach a goal state from a start state.

🎯 Project Overview

The system simulates a grid-based search problem where:

🟢 A Start Node must reach

🔴 A Goal Node

⚫ While avoiding structured obstacle walls

The application visually animates:

Frontier expansion

Explored nodes

Final path construction

Execution time per algorithm

Each traversal dynamically displays the algorithm name in the window title:

GOOD PERFORMANCE TIME APP — BFS
🧠 Algorithms Implemented
Algorithm	Optimal	Complete	Memory Usage
Breadth-First Search (BFS)	✅ Yes	✅ Yes	High
Depth-First Search (DFS)	❌ No	❌ Not always	Low
Uniform Cost Search (UCS)	✅ Yes	✅ Yes	High
Depth-Limited Search (DLS)	❌ Depends	❌ Depends	Low
Iterative Deepening DFS (IDDFS)	✅ Yes	✅ Yes	Moderate
Bidirectional Search	✅ Yes	✅ Yes	Reduced
🎨 Visualization Legend
Color	Meaning
White	Empty Cell
Black	Wall
Lime	Start Node
Red	Goal Node
Cyan	Frontier Nodes
Blue	Explored Nodes
Yellow	Final Path
🏗 Grid Design

20×20 structured grid

Straight horizontal and vertical obstacle segments

Clockwise movement order including diagonals

Deterministic layout for meaningful comparison

📦 Requirements

Python 3.9+

matplotlib

numpy

🔧 Installation

Clone the repository:

git clone https://github.com/yourusername/ai-pathfinder.git
cd ai-pathfinder

Install dependencies:

pip install matplotlib numpy
▶️ How to Run
python search_visualizer.py

You will see:

1 - BFS
2 - DFS
3 - UCS
4 - DLS
5 - IDDFS
6 - Bidirectional
0 - Exit

Select an option to start visualization.

After completion, press ENTER to return to the menu.

⚙ Customization
Change Start and Goal Location

Modify these lines in the code:

START = (1, 1)
TARGET = (18, 18)
Adjust Animation Speed
DELAY = 0.05

Lower value → faster
Higher value → slower

📊 What This Project Demonstrates

Visual difference between BFS and DFS

How UCS guarantees optimal paths

How IDDFS balances memory and optimality

How Bidirectional Search reduces search space

The importance of structured environments for algorithm comparison

🛠 Technical Details

Python

Matplotlib (TkAgg backend)

Numpy grid representation

Deque for BFS

Heap-based priority queue for UCS

Stack-based DFS & DLS

Dynamic GUI title updates per algorithm

📁 Project Structure
search_visualizer.py
README.md
🎓 Academic Context

Developed as part of an Artificial Intelligence course assignment focused on:

Uninformed Search Strategies

Search Space Exploration

Algorithm Comparison

Visualization of AI Decision Processes

🔮 Possible Extensions

Dynamic obstacle re-planning

A* heuristic search

Performance comparison charts

Interactive GUI controls

Adjustable grid sizes

👨‍💻 Author
Huzaifa Hammad
Laiba Najeeb Khan


# Rod Maneuvering with Prioritized Sweeping
Python implementation of the example from the book Reinforcement Learning: An Introduction by Richard S. Sutton and Andrew G. Barto
<br><br>
There are 2 differences from the original example:
1. Instead of 20x20x36 states, there are 21x21x36 states
2. Instead of 4 actions, there are 6 actions. Each correspond to:
    1. Up: Center of the rod moves up 30 units
    2. Down: Center of the rod moves down 30 units
    3. Right: Center of the rod moves right 30 units
    4. Left: Center of the rod moves left 30 units
    5. +10 Degree: Rod rotates +10 degrees from the center
    6. -10 Degree: Rod rotates -10 degrees from the center
<br><br>

All the obstacles are hard-coded so that if you change the resolution of the screen, you should also change the obstacle positions.
<br><br>
Also if you want to change the positions of the initial and goal state, be sure to make their center locations multiple of 30, and angles to multiple of 10.

## Hyperparameters
Default values for environment:
* <img src="https://render.githubusercontent.com/render/math?math=\alpha = 0.1">
* <img src="https://render.githubusercontent.com/render/math?math=\gamma = 0.97">
* <img src="https://render.githubusercontent.com/render/math?math=\epsilon = 0.1">
* <img src="https://render.githubusercontent.com/render/math?math=\theta = 0.01">

## Usage

To train from scratch:
```python
python3 main.py train
```

To use pre-trained Q values:
```python
python3 main.py
```

![](sequ.gif)
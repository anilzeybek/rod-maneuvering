# Rod Maneuvering with Prioritized Sweeping
Python implementation of the example from the book Reinforcement Learning: An Introduction by Richard S. Sutton and Andrew G. Barto.
<br><br>
There are 2 differences from the original example:
1. Instead of 20x20x36 states, there are 21x21x36 states.
2. Instead of 4 actions, there are 6 actions. Each correspond to:
    1. Up: Center of the rod moves up 30 units
    2. Down: Center of the rod moves down 30 units
    3. Right: Center of the rod moves right 30 units
    4. Left: Center of the rod moves left 30 units
    5. +10 Degree: Rod rotates +10 degrees from the center
    6. -10 Degree: Rod rotates -10 degrees from the center
<br><br>

With this actions and states, shortest path from starting state to ending state has 47 steps. 
<br><br>
All the obstacles are hard-coded so that if you change the resolution of the screen, you should also change the obstacle positions.
<br><br>
Also if you want to change the positions of the initial and goal state, be sure to make their center locations multiple of 30, and angles to multiple of 10.

## Hyperparameters
Default values of hyperparameters:
* α = 0.1
* γ = 0.97
* ε = 0.1
* θ = 0.01
* n = 30

Rewards are 0 for each step except +1 for step to goal state. When agent reaches to goal state, episode ends and positions reset.
<br><br>
With this hyperparameters, learning completely happens after average of 130.000 steps.  
If you use q-learning instead of prioritized sweeping, average of 1.720.000 steps required to learn completely.

## Usage
To install requirements:
```console
pip install -r requirements.txt
```
<br>

To train from scratch:
```console
python3 main.py -t
```
If you use this flag, initial screen will give you warning. If you click it, the animation will start but this will slow down the process of learning. So wait until some convergence to see the results faster.

<br>

To use pre-trained Q values:
```console
python3 main.py
```

<br>

To slow down the animate while using pre-trained values to see the actions more clear:
```console
python3 main.py -s
```
Do not try to use both -t and -s flags at the same time because with -s flag agent will wait 0.05 secs after each step. So training with that much wait is impossible.

<br>

If you want to try learning with q-learning:
```console
python3 main.py -q -t
```
With that, use q-learning instead of prioritized sweeping and learn from scratch.

<br>


![](sequ.gif)

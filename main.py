from rod_maneuvering_env import RodManeuveringEnv
from priority_queue import PriorityQueue
import pygame
import numpy as np
import random


def initialize():
    _Q = np.zeros((21, 21, 36, 6))
    _model = {}
    _PQueue = PriorityQueue()

    return _Q, _model, _PQueue


def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return random.choice(indices)


def policy(env, state):
    if np.random.uniform() <= env.epsilon:
        return np.random.randint(env.action_space.n)
    else:
        return rargmax(Q[state])


def insert_queue(state, action, P):
    PQueue.push(P, (state, action))


def leading_state_action(state):
    leading = []
    for key in model:
        if model[key][1] == state:
            leading.append(key)

    return leading


def main():
    theta = 5
    env = RodManeuveringEnv()

    running = 1
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0

        state = env.get_obs()
        action = policy(env, state)
        new_state, reward, done, _ = env.step(action)
        Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[new_state]) - Q[state][action])

        # model[(state, action)] = (reward, new_state)
        #
        # P = abs(reward + env.gamma * np.max(Q[new_state]) - Q[state][action])
        # if P > theta:
        #     print(P)
        #     insert_queue(state, action, P)
        #
        # for _ in range(env.n):
        #     if not PQueue.is_empty():
        #         state, action = PQueue.pop()
        #         reward, s_prime = model[(state, action)]
        #         Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[s_prime]) - Q[state][action])
        #
        #         for state_action in leading_state_action(state):
        #             r_over = model[(state_action[0], state_action[1])][0]
        #             P = abs(r_over + env.gamma * np.max(Q[state]) - Q[state_action[0]][state_action[1]])
        #
        #             if P > theta:
        #                 print(P)
        #                 insert_queue(state_action[0], state_action[1], P)


if __name__ == '__main__':
    Q, model, PQueue = initialize()
    main()

from rod_maneuvering_env import RodManeuveringEnv
import pygame
import numpy as np
import sys
import pickle
import heapq
import random
import time


def initialize():
    _Q = np.zeros((21, 21, 36, 6))
    _model = {}
    _PQueue = []

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


def leading_state_action(state):
    # leading = []
    # for key in model:
    #     if model[key][1] == state:
    #         leading.append(key)
    #
    # return leading
    all_leadings = [((state[0], state[1] + 1, state[2]), 0), ((state[0], state[1] - 1, state[2]), 1),
                    ((state[0] - 1, state[1], state[2]), 2), ((state[0] + 1, state[1], state[2]), 3),
                    ((state[0], state[1], state[2] - 1), 4), ((state[0], state[1], state[2] + 1), 5)]

    return_list = []
    for i in all_leadings:
        if i in model:
            return_list.append(i)

    return return_list


def main():
    global Q

    theta = 0.01
    step_count = 0
    env = RodManeuveringEnv()
    pygame.init()

    if len(sys.argv) == 1:
        infile = open("pretrainedQ.pickle", 'rb')
        Q = pickle.load(infile)
        infile.close()

    running = 1
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0

            outfile = open("pretrainedQ.pickle", 'wb')
            pickle.dump(Q, outfile)
            outfile.close()

        state = env.get_obs()
        action = policy(env, state)
        new_state, reward, done, _ = env.step(action)

        print(step_count)
        if step_count > 50000:
            env.render()
            # time.sleep(0.05)
        step_count += 1

        # Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[new_state]) - Q[state][action])
        model[(state, action)] = (reward, new_state)
        P = abs(reward + env.gamma * np.max(Q[new_state]) - Q[state][action])
        if P > theta:
            heapq.heappush(PQueue, (-P, (state, action)))

        for _ in range(env.n):
            if PQueue:
                state, action = heapq.heappop(PQueue)[1]
                reward, s_prime = model[(state, action)]
                Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[s_prime]) - Q[state][action])

                for state_action in leading_state_action(state):
                    r_over = model[(state_action[0], state_action[1])][0]
                    P = abs(r_over + env.gamma * np.max(Q[state]) - Q[state_action[0]][state_action[1]])

                    if P > theta:
                        heapq.heappush(PQueue, (-P, (state_action[0], state_action[1])))


if __name__ == '__main__':
    Q, model, PQueue = initialize()
    main()

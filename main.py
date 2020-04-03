from rod_maneuvering_env import RodManeuveringEnv
import pygame
import numpy as np
import sys
import pickle
import heapq
import random
import time


def parse_arg():
    from_scratch = False
    render_each_step = True

    if len(sys.argv) == 2 and sys.argv[1] == "train":
        from_scratch = True
        render_each_step = False
    elif len(sys.argv) == 2:
        raise ValueError("Arguments must be 'train' or blank")

    return from_scratch, render_each_step


def initialize(from_scratch):
    Q = np.zeros((21, 21, 36, 6))
    model = {}
    PQueue = []

    if not from_scratch:
        infile = open("pretrainedQ.pickle", 'rb')
        Q = pickle.load(infile)
        infile.close()

    return Q, model, PQueue


def save_Q(Q):
    outfile = open("pretrainedQ.pickle", 'wb')
    pickle.dump(Q, outfile)
    outfile.close()


def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return random.choice(indices)


def policy(Q, env, state):
    if np.random.uniform() <= env.epsilon:
        return np.random.randint(env.action_space.n)
    else:
        return rargmax(Q[state])


def leading_state_action(state, model):
    all_leads = [((state[0], state[1] + 1, state[2]), 0), ((state[0], state[1] - 1, state[2]), 1),
                 ((state[0] - 1, state[1], state[2]), 2), ((state[0] + 1, state[1], state[2]), 3),
                 ((state[0], state[1], state[2] - 1), 4), ((state[0], state[1], state[2] + 1), 5)]

    return_list = []
    for i in all_leads:
        if i in model:
            return_list.append(i)

    return return_list


def main():
    pygame.init()

    from_scratch, render_each_step = parse_arg()

    Q, model, PQueue = initialize(from_scratch)
    env = RodManeuveringEnv()

    if not render_each_step:
        env.render_load_screen()

    running = 1
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            save_Q(Q)
            quit(0)

        elif from_scratch and event.type == pygame.MOUSEBUTTONDOWN:
            render_each_step = True

        state = env.get_obs()
        action = policy(Q, env, state)
        new_state, reward, done, _ = env.step(action)

        if render_each_step:
            env.render()
            # time.sleep(0.5)

        model[(state, action)] = (reward, new_state)
        P = abs(reward + env.gamma * np.max(Q[new_state]) - Q[state][action])
        if P > env.theta:
            heapq.heappush(PQueue, (-P, (state, action)))

        for _ in range(env.n):
            if PQueue:
                state, action = heapq.heappop(PQueue)[1]
                reward, s_prime = model[(state, action)]
                Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[s_prime]) - Q[state][action])

                for state_action in leading_state_action(state, model):
                    r_over = model[(state_action[0], state_action[1])][0]
                    P = abs(r_over + env.gamma * np.max(Q[state]) - Q[state_action[0]][state_action[1]])

                    if P > env.theta:
                        heapq.heappush(PQueue, (-P, (state_action[0], state_action[1])))


if __name__ == '__main__':
    main()

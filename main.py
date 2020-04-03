from rod_maneuvering_env import RodManeuveringEnv
import pygame
import numpy as np
import pickle
import heapq
import random
import argparse
import time


def parse_arg():
    parser = argparse.ArgumentParser(description="Rod Maneuvering with Prioritized Sweeping")
    parser.add_argument("-t", "--train", dest="from_scratch", action="store_true", help="train from scratch")
    parser.add_argument("-s", "--slow", dest="slow", action="store_true", help="slow down the animation")
    parser.add_argument("-q", "--q-learning", dest="q_learning",
                        action="store_true", help="use q-learning instead of prioritized sweeping")

    return parser.parse_args()


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


def prioritized_sweeping(args, env, render_each_step):
    Q, model, PQueue = initialize(args.from_scratch)

    running = 1
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            save_Q(Q)
            quit(0)

        elif args.from_scratch and event.type == pygame.MOUSEBUTTONDOWN:
            render_each_step = True

        state = env.get_obs()
        action = policy(Q, env, state)
        new_state, reward, done, _ = env.step(action)

        if render_each_step:
            env.render()
            if args.slow:
                time.sleep(0.05)

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


def q_learning(args, env, render_each_step):
    Q, _, _ = initialize(args.from_scratch)

    running = 1
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            save_Q(Q)
            quit(0)

        elif args.from_scratch and event.type == pygame.MOUSEBUTTONDOWN:
            render_each_step = True

        state = env.get_obs()
        action = policy(Q, env, state)
        new_state, reward, done, _ = env.step(action)
        Q[state][action] += env.alpha * (reward + env.gamma * np.max(Q[new_state]) - Q[state][action])

        if render_each_step:
            env.render()
            if args.slow:
                time.sleep(0.05)


def main():
    pygame.init()

    args = parse_arg()
    env = RodManeuveringEnv()

    render_each_step = True
    if args.from_scratch:
        render_each_step = False
        env.render_load_screen()

    if args.q_learning:
        q_learning(args, env, render_each_step)
    else:
        prioritized_sweeping(args, env, render_each_step)


if __name__ == '__main__':
    main()

from RodManeuveringEnv import RodManeuveringEnv
import pygame


def main():
    env = RodManeuveringEnv()
    running = 1

    env.step(0)
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0

        # env.step(0)
        # env.step(0)
        # env.step(0)
        # env.step(0)
        #
        # env.step(2)


if __name__ == '__main__':
    main()

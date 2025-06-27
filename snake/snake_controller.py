import cv2
import numpy as np
import random
import time


class SnakeController:
    SNAKE_LEN_GOAL = 30

    def __init__(self):
        self.reset()

    def reset(self):
        self.running = True
        # Initial Snake and Apple position
        self.snake_position = [[250, 250], [240, 250], [230, 250]]
        self.apple_position = _get_random_apple_position()
        self.score = 0
        self.snake_head = [250, 250]
        self.last_action = 1

    # Action : 0-Left, 1-Right, 3-Up, 2-Down
    def step(self, action: int):
        if not self.running:
            return

        # U-turn is prohibited
        if action == 0 and self.last_action == 1:
            action = 1
        elif action == 1 and self.last_action == 0:
            action = 0
        elif action == 3 and self.last_action == 2:
            action = 2
        elif action == 2 and self.last_action == 3:
            action = 3
        self.last_action = action

        # Change the head position based on the ai action
        if action == 1:
            self.snake_head[0] += 10
        elif action == 0:
            self.snake_head[0] -= 10
        elif action == 2:
            self.snake_head[1] += 10
        elif action == 3:
            self.snake_head[1] -= 10

        # Increase Snake length on eating apple
        if self.snake_head == self.apple_position:
            self.apple_position = _get_random_apple_position()
            self.score += 1
            self.snake_position.insert(0, list(self.snake_head))

        else:
            self.snake_position.insert(0, list(self.snake_head))
            self.snake_position.pop()

        # On collision kill the snake and print the score
        if _collision_with_boundaries(self.snake_head):
            print("BOUNDARYYYYY")
            self.running = False
            return

        # On collision kill the snake and print the score
        if _collision_with_self(self.snake_position):
            print("AUTO-CRASH", self.snake_head, self.snake_position)
            self.running = False
            return
        else:

            print("OK", self.snake_head, self.snake_position)


def _get_random_apple_position():
    return [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]


def _collision_with_boundaries(snake_head):
    return (
        snake_head[0] >= 500
        or snake_head[0] < 0
        or snake_head[1] >= 500
        or snake_head[1] < 0
    )


def _collision_with_self(snake_position):
    return snake_position[0] in snake_position[1:]

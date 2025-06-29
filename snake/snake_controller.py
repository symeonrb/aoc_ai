import random


BOARD_WIDTH = 50
BOARD_HEIGHT = 50


class SnakeController:

    def __init__(self):
        self.reset()

    def reset(self):
        self.running = True
        # Initial Snake and Apple position
        self.snake_position = [
            [25, 25],
            [24, 25],
            [23, 25],
            # [22, 25],
            # [21, 25],
            # [20, 25],
            # [19, 25],
            # [18, 25],
            # [17, 25],
            # [16, 25],
            # [15, 25],
            # [14, 25],
        ]
        self.apple_position = _get_random_apple_position()
        self.score = 0
        self.snake_head = [25, 25]
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
            self.snake_head[0] += 1
        elif action == 0:
            self.snake_head[0] -= 1
        elif action == 2:
            self.snake_head[1] += 1
        elif action == 3:
            self.snake_head[1] -= 1

        # Increase Snake length on eating apple
        if self.snake_head == self.apple_position:
            self.apple_position = _get_random_apple_position()
            self.score += 1
        #     self.snake_position.insert(0, list(self.snake_head))

        # else:
        self.snake_position.insert(0, list(self.snake_head))
        self.snake_position.pop()

        # On collision kill the snake and print the score
        if _collision_with_boundaries(self.snake_head):
            self.running = False
            return

        # On collision kill the snake and print the score
        if _collision_with_self(self.snake_position):
            self.running = False
            return

    @property
    def snake_apple_distance(self):
        return abs(self.snake_head[0] - self.apple_position[0]) + abs(
            self.snake_head[1] - self.apple_position[1]
        )

    # Direction : 0-Left, 1-Right, 2-Down, 3-Up
    def next_obstacle(self, direction: int):
        dx = 0
        dy = 0
        if direction == 0:
            dx = -1
        if direction == 1:
            dx = 1
        if direction == 2:
            dy = 1
        if direction == 3:
            dy = -1

        distance = 1
        while True:
            new_head = [
                self.snake_head[0] + dx * distance,
                self.snake_head[1] + dy * distance,
            ]
            if _collision_with_boundaries(new_head) or new_head in self.snake_position:
                return distance
            distance += 1


def _get_random_apple_position():
    return [random.randrange(1, 50), random.randrange(1, 50)]


def _collision_with_boundaries(snake_head):
    return (
        snake_head[0] >= BOARD_WIDTH
        or snake_head[0] < 0
        or snake_head[1] >= BOARD_HEIGHT
        or snake_head[1] < 0
    )


def _collision_with_self(snake_position):
    return snake_position[0] in snake_position[1:]

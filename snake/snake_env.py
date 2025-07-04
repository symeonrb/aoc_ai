import gymnasium as gym
import numpy as np
from gymnasium import spaces
from collections import deque

from snake_view import SnakeView
from snake_controller import BOARD_HEIGHT, BOARD_WIDTH, SnakeController


DEATH_PUNISHMENT = -1
APPLE_BOOST = 100

# MAX_STEPS = 15_000
OBS_LENGTH = 6


class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode: str | None = None):
        super().__init__()

        self.render_mode = render_mode

        # must be gym.spaces object
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=-1.0 if OBS_LENGTH == 6 else 0.0,
            high=1.0,
            shape=(OBS_LENGTH,),
            dtype=np.float32,
        )

        self.controller = SnakeController()
        self.view = SnakeView(self.controller)

    def _get_observation(self):

        next_obstacles = (
            [
                self.controller.next_obstacle(0) / BOARD_HEIGHT,
                self.controller.next_obstacle(1) / BOARD_HEIGHT,
                self.controller.next_obstacle(2) / BOARD_WIDTH,
                self.controller.next_obstacle(3) / BOARD_WIDTH,
            ]
            if OBS_LENGTH > 4
            else []
        )

        positions = (
            [
                (self.controller.snake_head[0] - self.controller.apple_position[0])
                / BOARD_WIDTH,
                (self.controller.snake_head[1] - self.controller.apple_position[1])
                / BOARD_HEIGHT,
            ]
            if OBS_LENGTH == 6
            else [
                self.controller.apple_position[0] / BOARD_WIDTH,
                self.controller.apple_position[1] / BOARD_HEIGHT,
                self.controller.snake_head[0] / BOARD_WIDTH,
                self.controller.snake_head[1] / BOARD_HEIGHT,
            ]
        )

        return np.array([*positions, *next_obstacles])

    def reset(self, seed=None, options=None):
        self.terminated = self.truncated = False
        self.reward = 0
        # self.step_count = 0

        self.controller.reset()
        self.last_apple_position = self.controller.apple_position
        # distance when the apple appeared
        self.apple_distance_ref = self.controller.snake_apple_distance

        self.observation = self._get_observation()
        info = {}
        return self.observation, info

    def step(self, action):
        try:
            self.controller.step(action)
        except:
            self.truncated = True

        if self.render_mode == "human":
            self.view.paint()

        self.observation = self._get_observation()
        # print(self.observation)
        info = {}

        if self.controller.running:
            self.reward = 0
        else:
            self.terminated = True
            self.reward = DEATH_PUNISHMENT

        if self.last_apple_position != self.controller.apple_position:
            self.reward += APPLE_BOOST
            self.apple_distance_ref = self.controller.snake_apple_distance
            info["event"] = "apple_eaten"

        self.last_apple_position = self.controller.apple_position

        # print(
        #     self.reward,
        #     self.apple_distance_ref,
        #     self.controller.snake_apple_distance,
        # )

        # self.step_count += 1
        # if self.step_count > MAX_STEPS:
        #     self.truncated = True

        return self.observation, self.reward, self.terminated, self.truncated, info

    def render(self):
        self.view.paint()

    def close(self):
        self.view.close()

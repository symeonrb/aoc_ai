import gymnasium as gym
import numpy as np
from gymnasium import spaces
from collections import deque

from snake_view import SnakeView
from snake_controller import BOARD_HEIGHT, BOARD_WIDTH, SnakeController


DEATH_PUNISHMENT = -1
APPLE_BOOST = 10
DISTANCE__REWARD_COEF = 0.01

MAX_STEPS = 1500
OBS_LENGTH = 8


class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode: str | None = None):
        super().__init__()

        self.render_mode = render_mode

        # must be gym.spaces object
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(OBS_LENGTH,),
            dtype=np.float32,
        )

        self.controller = SnakeController()
        self.view = SnakeView(self.controller)

    def reset(self, seed=None, options=None):
        self.terminated = self.truncated = False
        self.reward = 0
        self.step_count = 0

        self.controller.reset()
        self.last_apple_position = self.controller.apple_position
        # distance when the apple appeared
        self.apple_distance_ref = self.controller.snake_apple_distance

        next_obstacles = (
            [
                self.controller.next_obstacle(0),
                self.controller.next_obstacle(1),
                self.controller.next_obstacle(2),
                self.controller.next_obstacle(3),
            ]
            if OBS_LENGTH > 4
            else []
        )

        self.observation = np.array(
            [
                self.controller.apple_position[0] / BOARD_WIDTH,
                self.controller.apple_position[1] / BOARD_HEIGHT,
                self.controller.snake_head[0] / BOARD_WIDTH,
                self.controller.snake_head[1] / BOARD_HEIGHT,
                *next_obstacles,
            ]
        )

        info = {}
        return self.observation, info

    def step(self, action):
        try:
            self.controller.step(action)
        except:
            self.truncated = True

        if self.render_mode == "human":
            self.view.paint()

        next_obstacles = (
            [
                self.controller.next_obstacle(0),
                self.controller.next_obstacle(1),
                self.controller.next_obstacle(2),
                self.controller.next_obstacle(3),
            ]
            if OBS_LENGTH > 4
            else []
        )
        print(next_obstacles)

        self.observation = np.array(
            [
                self.controller.apple_position[0] / BOARD_WIDTH,
                self.controller.apple_position[1] / BOARD_HEIGHT,
                self.controller.snake_head[0] / BOARD_WIDTH,
                self.controller.snake_head[1] / BOARD_HEIGHT,
                *next_obstacles,
            ]
        )
        info = {}

        if self.controller.running:
            self.reward = 0
            # (
            #     self.apple_distance_ref - self.controller.snake_apple_distance
            # ) * DISTANCE__REWARD_COEF
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

        self.step_count += 1
        if self.step_count > MAX_STEPS:
            self.truncated = True

        return self.observation, self.reward, self.terminated, self.truncated, info

    def render(self):
        self.view.paint()

    def close(self):
        self.view.close()

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from collections import deque

from snake_view import SnakeView
from snake_controller import SnakeController


SCORE_BASE = 50
DEATH_PUNISHMENT = -1_000
SCORE_MULT = 10
APPLE_BOOST = 100_000
STEPS_BEFORE_SLOWNESS_PUNISHMENT = 50

OBS_SIZE = 5


class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode: str | None = None):
        super().__init__()

        self.render_mode = render_mode

        # must be gym.spaces object
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=-1,
            high=500,
            shape=(
                (OBS_SIZE,) if OBS_SIZE < 10 else (6 + SnakeController.SNAKE_LEN_GOAL,)
            ),
            dtype=np.int64,
        )

        self.controller = SnakeController()
        self.view = SnakeView(self.controller)

    def reset(self, seed=None, options=None):
        self.terminated = self.truncated = False
        self.reward = 0

        self.controller.reset()
        self.last_apple_position = self.controller.apple_position
        self.steps_since_last_eaten = 0
        self.apple_distance_ref = (
            self.controller.snake_apple_distance
        )  # distance when the apple appeared

        snake_length = len(self.controller.snake_position)
        self.prev_actions = deque(maxlen=SnakeController.SNAKE_LEN_GOAL)
        for _ in range(SnakeController.SNAKE_LEN_GOAL):
            self.prev_actions.append(1)

        self.observation = (
            np.array(self.controller.apple_position + self.controller.snake_head)
            if OBS_SIZE == 4
            else (
                np.array(
                    [self.controller.snake_apple_distance]
                    + self.controller.apple_position
                    + self.controller.snake_head
                )
                if OBS_SIZE == 5
                else np.array(
                    [self.controller.snake_apple_distance]
                    + self.controller.apple_position
                    + self.controller.snake_head
                    + [snake_length]
                    + list(self.prev_actions)
                )
            )
        )

        info = {}
        return self.observation, info

    def step(self, action):
        self.prev_actions.append(action)

        try:
            self.controller.step(action)
        except:
            self.truncated = True

        snake_length = len(self.controller.snake_position)
        self.observation = (
            np.array(self.controller.apple_position + self.controller.snake_head)
            if OBS_SIZE == 4
            else (
                np.array(
                    [self.controller.snake_apple_distance]
                    + self.controller.apple_position
                    + self.controller.snake_head
                )
                if OBS_SIZE == 5
                else np.array(
                    [self.controller.snake_apple_distance]
                    + self.controller.apple_position
                    + self.controller.snake_head
                    + [snake_length]
                    + list(self.prev_actions)
                )
            )
        )

        if self.controller.running:
            self.reward = (
                # self.controller.score
                # * SCORE_MULT
                # + SCORE_BASE
                self.apple_distance_ref
                - self.controller.snake_apple_distance
            )
        else:
            self.terminated = True
            self.reward = DEATH_PUNISHMENT

        self.steps_since_last_eaten += 1

        # Temp boosts based on eating apple
        if self.last_apple_position != self.controller.apple_position:
            # self.reward += APPLE_BOOST
            self.steps_since_last_eaten = 0
            self.apple_distance_ref = self.controller.snake_apple_distance
            print("EAT APPLE !!!!!")
        self.last_apple_position = self.controller.apple_position

        if self.steps_since_last_eaten > STEPS_BEFORE_SLOWNESS_PUNISHMENT:
            self.reward -= (
                self.steps_since_last_eaten / STEPS_BEFORE_SLOWNESS_PUNISHMENT - 1
            )

        # print(
        #     self.reward,
        #     self.apple_distance_ref,
        #     self.controller.snake_apple_distance,
        #     self.steps_since_last_eaten,
        # )

        info = {}
        return self.observation, self.reward, self.terminated, self.truncated, info

    def render(self):
        self.view.paint()

    def close(self):
        self.view.close()

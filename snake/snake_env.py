import gymnasium as gym
import numpy as np
from gymnasium import spaces
from collections import deque

from snake_controller import SnakeController


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
            shape=(5 + SnakeController.SNAKE_LEN_GOAL,),
            dtype=np.int64,
        )

        self.controller = SnakeController()

    def reset(self, seed=None, options=None):
        self.terminated = self.truncated = False
        self.reward = 0

        self.controller.reset()

        snake_length = len(self.controller.snake_position)
        self.prev_actions = deque(maxlen=SnakeController.SNAKE_LEN_GOAL)
        for _ in range(SnakeController.SNAKE_LEN_GOAL):
            self.prev_actions.append(-1)

        self.observation = np.array(
            self.controller.snake_head
            + self.controller.apple_position
            + [snake_length]
            + list(self.prev_actions)
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
        self.observation = np.array(
            self.controller.snake_head
            + self.controller.apple_position
            + [snake_length]
            + list(self.prev_actions)
        )

        if self.controller.running:
            self.reward = self.controller.score * 10
        else:
            self.terminated = True
            self.reward = -10

        info = {}
        return self.observation, self.reward, self.terminated, self.truncated, info

    def render(self):
        super().render()

    def close(self):
        super().close()

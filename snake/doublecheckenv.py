import time

import cv2
from snake_view import SnakeView
from snake_env import SnakeEnv


env = SnakeEnv()

# view = SnakeView(env.controller)
# view.paint()

episodes = 50
for episode in range(episodes):
    obs = env.reset()
    terminated = truncated = False
    old_reward = 0

    while not terminated and not truncated:
        # cv2.waitKey(125)

        random_action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(random_action)
        if old_reward != reward:
            print("episode", episode + 1, "reward", reward)
        old_reward = reward

        # view.paint()

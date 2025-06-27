import time

import cv2
from snake_view import SnakeView
from snake_env import SnakeEnv


env = SnakeEnv()

view = SnakeView(env.controller)
view.paint()

episodes = 50
for episode in range(episodes):
    obs = env.reset()
    while True:
        # cv2.waitKey(125)
        random_action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(random_action)
        print("action", random_action, "reward", reward)

        view.paint()

        if terminated or truncated:
            break

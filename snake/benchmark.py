import cv2
import warnings
from stable_baselines3 import PPO

from snake_env import SnakeEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

env = SnakeEnv(render_mode="human")

models_dir = "models/PPO-1751066034"
filename_end = "00000.zip"

for i in range(1, 11):
    model = PPO.load(f"{models_dir}/{i}{filename_end}", env=env)

    scores = []
    episodes = 1000
    for ep in range(episodes):
        obs, info = env.reset()
        terminated = truncated = False
        while not terminated and not truncated:
            action, _states = model.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            # env.render()
            # cv2.waitKey(10)
        scores.append(env.controller.score)

    env.close()

    print(f"{i}{filename_end} :", sum(scores) / len(scores))

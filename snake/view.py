import cv2
import warnings
from stable_baselines3 import PPO

from snake_env import SnakeEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

env = SnakeEnv(render_mode="human")

models_dir = "models/PPO-1751054836"
model_path = f"{models_dir}/800000.zip"
model = PPO.load(model_path, env=env)

episodes = 10
for ep in range(episodes):
    obs, info = env.reset()
    terminated = truncated = False
    while not terminated and not truncated:
        action, _states = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()
        cv2.waitKey(10)

env.close()

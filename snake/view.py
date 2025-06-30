import cv2
import warnings
from stable_baselines3 import PPO

from snake_env import SnakeEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

BENCHMARK = False

env = SnakeEnv(render_mode=None if BENCHMARK else "human")

# models_dir = "models/PPO-230262"
# model_path = f"{models_dir}/2200000.zip"
models_dir = "models/PPO-232559"
model_path = f"{models_dir}/9900000.zip"
model = PPO.load(model_path, env=env)

print(f"{"Benchmarking" if BENCHMARK else "Displaying"} {model_path}")

scores = []
episodes = 1000 if BENCHMARK else 10
for ep in range(episodes):
    obs, info = env.reset()
    terminated = truncated = False
    while not terminated and not truncated:
        action, _states = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        if not BENCHMARK:
            env.render()
            cv2.waitKey(10)
    scores.append(env.controller.score)

env.close()

print(sum(scores) / len(scores))

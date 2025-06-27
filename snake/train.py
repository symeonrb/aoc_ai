import warnings
from stable_baselines3 import PPO
import os
import time

from snake_env import SnakeEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

SAVES = 10  # Number of saves
TIMESTEPS = 10_000  # Number of steps between each save

now = int(time.time())
models_dir = f"models/PPO-{now}"
logdir = f"logs/PPO-{now}"

print("1")
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
if not os.path.exists(logdir):
    os.makedirs(logdir)
print("2")

env = SnakeEnv(render_mode="rgb_array")
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
for i in range(1, SAVES):
    print(i)
    model.learn(
        total_timesteps=TIMESTEPS,
        reset_num_timesteps=False,
        tb_log_name=f"PPO-{now}",
    )
    model.save(f"{models_dir}/{TIMESTEPS*i}")
env.close()

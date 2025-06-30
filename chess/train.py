import warnings
from stable_baselines3 import PPO
import os
import time

from chess_env import ChessEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

# Training parameters
model_class = PPO
SAVES = 10  # Number of saves
TIMESTEPS = 10_000  # Number of steps between each save
SAVE = True


now = int(time.time()) - 1751000000
models_dir = f"models/{model_class.__name__}-{now}"
logdir = "logs"

if SAVE:
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

env = ChessEnv()

# Model from scratch
model = model_class(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log=logdir if SAVE else None,
)

# Model from saved
# seed_model_dir = "models/PPO-1751056386"
# seed_model_path = f"{seed_model_dir}/2000000.zip"
# model = PPO.load(seed_model_path, env=env)

for i in range(1, SAVES + 1):
    model.learn(
        total_timesteps=TIMESTEPS,
        reset_num_timesteps=False,
        tb_log_name=f"{model_class.__name__}-{now}" if SAVE else "",
    )
    if SAVE:
        model.save(f"{models_dir}/{TIMESTEPS*i}")
env.close()

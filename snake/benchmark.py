import cv2
import warnings
from stable_baselines3 import PPO

from snake_env import SnakeEnv

# Remove deprecated warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

env = SnakeEnv(render_mode="human")

models_dir = "models/PPO-1751069820"
filename_end = "00000.zip"

print(f"Starting benchmark of {models_dir}/X{filename_end}")

for i in range(1, 30):
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

# PPO-1751056370 :
# 2000000_seed.zip : 6.016

# PPO-1751056386 :
# 1000000.zip : 4.905
# 2000000.zip : 6.437
# 3000000.zip : 6.211
# 4000000.zip : 2.082
# 5000000.zip : 6.161

# PPO-1751061714 :
# Queue 3
# 1000000.zip : 7.17
# 2000000.zip : 7.748
# 3000000.zip : 8.437
# 4000000.zip : 9.127
# 5000000.zip : 9.207
# 6000000.zip : 8.891
# 7000000.zip : 9.139
# 8000000.zip : 8.654
# 9000000.zip : 9.455
# 10000000.zip : 9.101

# PPO-1751066034 :
# Queue 3
# 100000.zip : 8.868
# 200000.zip : 8.469
# 300000.zip : 8.517
# 400000.zip : 8.477
# 500000.zip : 8.627
# 600000.zip : 9.307
# 700000.zip : 8.854
# 800000.zip : 8.859
# 900000.zip : 8.476
# 1000000.zip : 9.138
# Queue 12
# 100000.zip : 5.662
# 200000.zip : 5.746
# 300000.zip : 6.298
# 400000.zip : 5.857
# 500000.zip : 6.462
# 600000.zip : 6.14
# 700000.zip : 6.003
# 800000.zip : 6.232
# 900000.zip : 5.902
# 1000000.zip : 6.087

# PPO-1751067342 :
# Queue 3
# 100000.zip : 8.742
# 200000.zip : 8.871
# 300000.zip : 8.2
# 400000.zip : 8.598
# 500000.zip : 8.63
# 600000.zip : 8.585
# 700000.zip : 8.009
# 800000.zip : 8.499
# 900000.zip : 9.113
# 1000000.zip : 9.124
# Queue 12
# 100000.zip : 6.109
# 200000.zip : 5.909
# 300000.zip : 6.433
# 400000.zip : 5.705
# 500000.zip : 6.201
# 600000.zip : 5.873
# 700000.zip : 5.736
# 800000.zip : 6.034
# 900000.zip : 6.016
# 1000000.zip : 6.067

# PPO-1751069820 :
# Queue 3
# 100000.zip : 7.587
# 200000.zip : 6.994
# 300000.zip : 7.376
# 400000.zip : 8.234
# 500000.zip : 7.75
# 600000.zip : 9.045
# 700000.zip : 7.827
# 800000.zip : 7.969
# 900000.zip : 7.862
# 1000000.zip : 7.713
# 1100000.zip : 8.251
# 1200000.zip : 8.456
# 1300000.zip : 7.891
# 1400000.zip : 7.543
# 1500000.zip : 8.747
# 1600000.zip : 9.165
# 1700000.zip : 8.27
# 1800000.zip : 8.354
# 1900000.zip : 8.985
# 2000000.zip : 8.629
# 2100000.zip : 8.793
# 2200000.zip : 8.714
# 2300000.zip : 8.827
# 2400000.zip : 8.792
# 2500000.zip : 8.024
# 2600000.zip : 8.363
# 2700000.zip : 8.172
# 2800000.zip : 9.205
# 2900000.zip : 7.932

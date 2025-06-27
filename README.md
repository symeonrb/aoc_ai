### Create virtual env

python3 -m venv venv

### Generate requirements.txt

pip freeze > requirements.txt

### Activate virtual env

source venv/bin/activate && python -m pip install -r requirements.txt

### Start Tensorboard

tensorboard --logdir=logs

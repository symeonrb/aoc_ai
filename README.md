# Reinforcment learning exercices

## Project Description

A collection of reinforcement learning exercises and demos, including a Snake game environment and RL agent implementations. The goal is to provide hands-on examples for learning and experimenting with RL algorithms.

## Features

- Lunar landing environment and agent with ui
- Snake game environment and agent with ui

## Snake demo

![Snake Game Demo](assets/snake_demo.mov)

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd aoc_ai
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

- To run the Snake demo:
  ```bash
  python view.py
  ```
- To train an RL agent (example):
  ```bash
  python train.py
  ```
- To monitor training with TensorBoard:
  ```bash
  tensorboard --logdir=logs
  ```

## Project Structure

- `snake_controller.py` - Main Snake game logic
- `snake_view.py` - Snake game UI
- `snake_v2.py` - To play snake on your computer
- `train.py` - Training script for RL agents
- `view.py` - See what an agent is capable of
- `benchmark.py` - Get the apples per episode of an agent
- `models/` - RL agent implementations
- `logs/` - TensorBoard logs
- `assets/` - Images and media

## Useful commands when creating new game

### Create virtual env

python3 -m venv venv

### Generate requirements.txt

pip freeze > requirements.txt

### Activate virtual env

source venv/bin/activate && python -m pip install -r requirements.txt

### Start Tensorboard

tensorboard --logdir=logs

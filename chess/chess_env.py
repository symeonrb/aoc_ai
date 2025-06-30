import gym
from gym import spaces
import numpy as np
import chess
import chess.engine


class ChessEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.board = chess.Board()

        # Fixed action space: 4672 possible (from_square * to_square)
        self.action_space = spaces.Discrete(64 * 64)

        # Observation: 8x8x12 binary planes for each piece type and color
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(8, 8, 12), dtype=np.int8
        )

    def reset(self):
        self.board.reset()
        return self._get_obs()

    def step(self, action):
        move = self._decode_action(action)

        if move not in self.board.legal_moves:
            # Illegal move = lose immediately
            reward = -1.0
            done = True
            return self._get_obs(), reward, done, {"illegal_move": True}

        self.board.push(move)

        done = self.board.is_game_over()
        reward = self._get_reward(done)

        return self._get_obs(), reward, done, {}

    def render(self, mode="human"):
        print(self.board)

    def _get_obs(self):
        # 8x8x12 one-hot encoding
        obs = np.zeros((8, 8, 12), dtype=np.int8)

        piece_to_index = {
            "P": 0,
            "N": 1,
            "B": 2,
            "R": 3,
            "Q": 4,
            "K": 5,
            "p": 6,
            "n": 7,
            "b": 8,
            "r": 9,
            "q": 10,
            "k": 11,
        }

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                idx = piece_to_index[piece.symbol()]
                row = 7 - (square // 8)
                col = square % 8
                obs[row, col, idx] = 1

        return obs

    def _decode_action(self, action_index):
        from_square = action_index // 64
        to_square = action_index % 64
        return chess.Move(from_square, to_square)

    def _get_reward(self, done):
        if not done:
            return 0.0

        result = self.board.result()
        if result == "1-0":
            return 1.0  # White wins
        elif result == "0-1":
            return -1.0  # Black wins
        else:
            return 0.0  # Draw

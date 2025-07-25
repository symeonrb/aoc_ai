import cv2
import numpy as np
from snake_controller import BOARD_HEIGHT, BOARD_WIDTH, SnakeController


CANVAS_HEIGHT = BOARD_HEIGHT * 10
CANVAS_WIDTH = BOARD_WIDTH * 10


class SnakeView:
    def __init__(self, controller: SnakeController):
        self.controller = controller
        self.img = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), dtype="uint8")

    def paint(self):
        if self.controller.running:

            cv2.imshow("snake", self.img)
            self.img = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), dtype="uint8")
            # Display Apple
            cv2.rectangle(
                self.img,
                (
                    self.controller.apple_position[0] * 10,
                    self.controller.apple_position[1] * 10,
                ),
                (
                    self.controller.apple_position[0] * 10 + 10,
                    self.controller.apple_position[1] * 10 + 10,
                ),
                (0, 0, 255),
                3,
            )
            # Display Snake
            for position in self.controller.snake_position:
                cv2.rectangle(
                    self.img,
                    (position[0] * 10, position[1] * 10),
                    (position[0] * 10 + 10, position[1] * 10 + 10),
                    (0, 255, 0),
                    3,
                )

        else:

            font = cv2.FONT_HERSHEY_SIMPLEX
            self.img = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), dtype="uint8")
            cv2.putText(
                self.img,
                "Your Score is {}".format(self.controller.score),
                (140, 250),
                font,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow("snake", self.img)

        cv2.setWindowTitle("snake", str(self.controller.score))

    def close(self):
        cv2.destroyAllWindows()

import cv2
import time

from snake_view import SnakeView
from snake_controller import SnakeController


controller = SnakeController()
view = SnakeView(controller)

button_direction = 1

while controller.running:
    view.paint()

    # Takes step after fixed time
    t_end = time.time() + 0.2
    k = -1
    while time.time() < t_end:
        if k == -1:
            k = cv2.waitKey(125)
        else:
            continue

    # q-Left, d-Right, z-Up, s-Down, p-Quit
    if k == ord("q"):
        button_direction = 0
    elif k == ord("d"):
        button_direction = 1
    elif k == ord("z"):
        button_direction = 3
    elif k == ord("s"):
        button_direction = 2
    elif k == ord("p"):
        break
    else:
        button_direction = button_direction

    controller.step(button_direction)

    # next_obstacles = [
    #     controller.next_obstacle(0),
    #     controller.next_obstacle(1),
    #     controller.next_obstacle(2),
    #     controller.next_obstacle(3),
    # ]
    # print(next_obstacles)

view.paint()
cv2.waitKey(0)
cv2.destroyAllWindows()

import time
import cv2
import mss
import json
import numpy as np

from flappy_bird.flappy_bird import FlappyBird


IN_FILE_NAME = "screen.json"
TARGET_ACTIONS_PER_SEC = 10


with open(IN_FILE_NAME, 'r') as f:
    cut_area = json.load(f)

window_width = cut_area["width"]
window_height = cut_area["height"]

cv2.namedWindow("image")
cv2.moveWindow("image", 0, 0)

# frame counter
f_counter = 0
start = time.time()

game = FlappyBird((window_width, window_height))
current_fps = 0
min_sec_gap_between_actions = 1.0 / TARGET_ACTIONS_PER_SEC
prev_action = time.time()

with mss.mss() as sct:
    while True:
        f_counter += 1
        k = cv2.waitKey(1)
        screen_img = np.array(sct.grab(cut_area))

        fb_data = game.image_to_data(screen_img)
        fb_image = game.data_to_image(fb_data, screen_img)
        if time.time() - prev_action >= min_sec_gap_between_actions:
            game.take_acion(fb_data)
            prev_action = time.time()

        cv2.putText(fb_image, str(int(current_fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("image", fb_image)
        k = cv2.waitKey(1)
        if k == 27:
            break

        # fps
        if f_counter == 60:
            stop = time.time()
            current_fps = f_counter / (stop - start)
            start = time.time()
            f_counter = 0


cv2.destroyAllWindows()

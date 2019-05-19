import time
import cv2
import mss
import json
import numpy as np

from flappy_bird.flappy_bird import FlappyBird


IN_FILE_NAME = "screen.json"

with open(IN_FILE_NAME, 'r') as f:
    cut_area = json.load(f)

cv2.namedWindow("image")
cv2.moveWindow("image", 0, 0)

f_counter = 0
start = time.time()

game = FlappyBird()

with mss.mss() as sct:
    while True:
        f_counter += 1
        k = cv2.waitKey(1)
        screen_img = np.array(sct.grab(cut_area))
        fb_data = game.image_to_data(screen_img)
        fb_image = game.data_to_image(fb_data, screen_img)
        cv2.imshow("image", fb_image)
        k = cv2.waitKey(1)
        if k == 27:
            break
        # fps
        if f_counter == 60:
            stop = time.time()
            print(f"fps: {f_counter / (stop - start)}")
            start = time.time()
            f_counter = 0


cv2.destroyAllWindows()

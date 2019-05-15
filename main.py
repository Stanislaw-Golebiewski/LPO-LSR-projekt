import time
import cv2
import mss
import json
import numpy as np

from flappy_bird.flappy_bird import fb_TemplateMatching

IN_FILE_NAME = "screen.json"

with open(IN_FILE_NAME, 'r') as f:
    cut_area = json.load(f)

cv2.namedWindow("image")
cv2.moveWindow("image", 0, 0)

with mss.mss() as sct:
    while True:
        screen_img = np.array(sct.grab(cut_area))
        screen_img_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        img_out = fb_TemplateMatching(screen_img, screen_img_gray)
        cv2.imshow("image", img_out)
        # cv2.imshow("image", screen_img)
        k = cv2.waitKey(18)
        if k == 27:
            break


cv2.destroyAllWindows()

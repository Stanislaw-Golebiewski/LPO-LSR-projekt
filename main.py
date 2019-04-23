import time
import cv2
import mss
import json
import numpy as np

NO_WAIT_SEC = 5
IN_FILE_NAME = "screen.json"

with open(IN_FILE_NAME, 'r') as f:
    cut_area = json.load(f)

cv2.namedWindow("image")
cv2.moveWindow("image", 0, 0)

with mss.mss() as sct:
    while True:
        screen_img = np.array(sct.grab(cut_area))
        cv2.imshow("image", screen_img)
        k = cv2.waitKey(17)
        if k == 27:
            break

cv2.destroyAllWindows()

import time
import cv2
import mss
import json
import sys
import numpy as np

from flappy_bird.flappy_bird import FlappyBird
from dino_chrome.dino_chrome import DinoChrome

IN_FILE_NAME = "screen.json"
TARGET_ACTIONS_PER_SEC = 10

# pick game
games = [("Flappy Bird", FlappyBird), ("T-Rex Chrome", DinoChrome)]
for num, g in enumerate(games):
    print(f"  {num}. {g[0]}")

picked_game_num = int(input(f":> pick game [{0} - {len(games) - 1}]: "))
print(f"> {games[picked_game_num][0]} picked")
game = games[picked_game_num][1]()
game.setup()
cut_area = game.screen_cut_area

# is test mode flag on?
if len(sys.argv) > 1:
    if "--test" in sys.argv:
        print("> Tryb testowy")
        game.test()
        sys.exit(0)

# run game
cv2.namedWindow(game.name)
cv2.moveWindow(game.name, 0, 0)

# frame counter
f_counter = 0
start = time.time()
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
        cv2.imshow(game.name, fb_image)
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

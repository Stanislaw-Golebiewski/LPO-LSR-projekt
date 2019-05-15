import cv2
import numpy as np


def fb_TemplateMatching(img_in, gray_img_in):
    global bird, bird_w, bird_h, pipe_up_w, pipe_up_h
    img_out = img_in.copy()
    # bird
    results = cv2.matchTemplate(gray_img_in, bird, cv2.TM_CCOEFF_NORMED)
    threshold = 0.40
    loc = np.where(results >= threshold)
    for point in zip(*loc[::-1]):
        cv2.rectangle(img_out, point, (point[0] + bird_h, point[1] + bird_w), (0, 255, 255), 2)

    # # pipe up
    # results = cv2.matchTemplate(gray_img_in, pipe_up, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.60
    # loc = np.where(results >= threshold)
    # for point in zip(*loc[::-1]):
    #     cv2.rectangle(img_out, point, (point[0] + pipe_up_h, point[1] + pipe_up_w), (255, 0, 0), 2)

    return img_out


# przy uruchomieniu (> python flappy_bird.py)
if __name__ == "__main__":
    bird = cv2.imread('bird.png', 0)
    pipe_up = cv2.imread('pipe_up.png', 0)
    bird_w = bird.shape[0]
    bird_h = bird.shape[1]

    pipe_up_w = pipe_up.shape[0]
    pipe_up_h = pipe_up.shape[1]

    img_in = cv2.imread("game_screen_2.png")
    img_in_gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    img_out = fb_TemplateMatching(img_in, img_in_gray)
    cv2.imshow("image", img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# przy zaimportowaniu jako moduł (import flappy_bird)
else:
    bird = cv2.imread('./flappy_bird/bird.png', 0)
    pipe_up = cv2.imread('./flappy_bird/pipe_up.png', 0)

bird_w = bird.shape[0]
bird_h = bird.shape[1]

pipe_up_w = pipe_up.shape[0]
pipe_up_h = pipe_up.shape[1]

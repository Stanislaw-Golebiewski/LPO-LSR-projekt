import os
import cv2
import json

from flappy_bird.image_processing.color_matching import ColorMatching
from flappy_bird.controller.simple_controller import SimpleController
from flappy_bird.controller.fixed_fuzzy import FixedFuzzy
from utils.setup import run_setup


DEFAULT_SETTINGS_FILE_PATH = "./flappy_bird/screen.json"


class FlappyBird:
    def __init__(self):
        self.name = "Flappy Bird (V o)>"

    def setup(self):
        should_run_setup = False
        if not os.path.exists(DEFAULT_SETTINGS_FILE_PATH):
            print(f"> Nie znaleziono pliku screen.json w {os.path.abspath(DEFAULT_SETTINGS_FILE_PATH)}")
            should_run_setup = True
        else:
            print("> Znalaziono plik screen.json")
            dec = input(":> Czy wygenerować nowe ustawienia? [t/N]")
            if dec in ["t", "T", "1"]:
                should_run_setup = True
        if should_run_setup:
            print("> Generowanie nowych ustawień...(setup.py)")
            run_setup(os.path.abspath(DEFAULT_SETTINGS_FILE_PATH))

        print("> Wczytywanie ustawień (screen.json)")
        with open(DEFAULT_SETTINGS_FILE_PATH, 'r') as f:
            cut_area = json.load(f)

        self.window_size = (cut_area["width"], cut_area["height"])
        self.screen_cut_area = cut_area

        image_processor = ColorMatching
        controller = FixedFuzzy
        self.image_processor = image_processor(self.window_size)
        self.controller = controller(self.window_size)

    def image_to_data(self, img):
        return self.image_processor.image_to_data(img)

    def data_to_image(self, data, img):
        return self.image_processor.data_to_image(data, img)

    def take_acion(self, data):
        return self.controller.take_action(data)

    def test(self):
        img_in = cv2.imread("./flappy_bird/images/game_screen_2.png")
        data_out = self.image_to_data(img_in)
        img_out = self.data_to_image(data_out, img_in)
        print(data_out)
        # self.take_acion(data_out)
        cv2.imshow("image", img_out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# przy bezpośrednim uruchomieniu testujemy na screenie (> python flappy_bird.py)
# if __name__ == "__main__":
#     img_in = cv2.imread("./flappy_bird/images/game_screen_2.png")
#     w_width, w_height, _ = img_in.shape
#     fb = FlappyBird((w_width, w_height))
#     data_out = fb.image_to_data(img_in)
#     img_out = fb.data_to_image(data_out, img_in)
#     fb.take_acion(data_out)
#     cv2.imshow("image", img_out)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

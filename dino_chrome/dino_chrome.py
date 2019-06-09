import os
import cv2
import json

from utils.setup import run_setup
from dino_chrome.image_processing.color_matching import ColorMatching
from dino_chrome.controller.simple_controller import SimpleController


DEFAULT_SETTINGS_FILE_PATH = "./dino_chrome/screen.json"


class DinoChrome:
    def __init__(self):
        self.name = "Dino Chrome"

    def setup(self):
        should_run_setup = False
        if not os.path.exists(DEFAULT_SETTINGS_FILE_PATH):
            print(f"> Nie znaleziono pliku screen.json w {os.path.abspath(DEFAULT_SETTINGS_FILE_PATH)}")
            should_run_setup = True
        else:
            print("> Znalaziono plik screen.json")
            dec = input(":> Czy wygenerować nowe ustawienia? [t/N] ")
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

        self.image_processor = ColorMatching(self.window_size)
        self.controller = SimpleController(self.window_size)

    def image_to_data(self, img):
        return self.image_processor.image_to_data(img)

    def data_to_image(self, data, img):
        return self.image_processor.data_to_image(data, img)

    def take_acion(self, data):
        return self.controller.take_action(data)

    def test(self):
        img_in = cv2.imread("./dino_chrome/images/game_dino_3.png")
        data_out = self.image_to_data(img_in)
        img_out = self.data_to_image(data_out, img_in)
        # # self.take_acion(data_out)
        cv2.imshow("image", img_out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

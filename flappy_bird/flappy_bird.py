import cv2

from .image_processing.color_matching import ColorMatching

from .controller.simple_controller import SimpleController
from .controller.fixed_fuzzy import FixedFuzzy


class FlappyBird:
    def __init__(self, window_size, image_processor=ColorMatching, controller=FixedFuzzy):
        self.image_processor = image_processor(window_size)
        self.controller = controller(window_size)

    def image_to_data(self, img):
        return self.image_processor.image_to_data(img)

    def data_to_image(self, data, img):
        return self.image_processor.data_to_image(data, img)

    def take_acion(self, data):
        return self.controller.take_action(data)


# przy bezpośrednim uruchomieniu testujemy na screenie (> python flappy_bird.py)
if __name__ == "__main__":
    img_in = cv2.imread("./flappy_bird/images/game_screen_2.png")
    w_width, w_height, _ = img_in.shape
    fb = FlappyBird((w_width, w_height))
    data_out = fb.image_to_data(img_in)
    img_out = fb.data_to_image(data_out, img_in)
    fb.take_acion(data_out)
    cv2.imshow("image", img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

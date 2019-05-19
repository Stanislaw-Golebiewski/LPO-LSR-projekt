import cv2

from .image_processing.color_matching import ColorMatching


class FlappyBird:
    def __init__(self, image_processor=ColorMatching):
        self.image_processor = image_processor()

    def image_to_data(self, img):
        return self.image_processor.image_to_data(img)

    def data_to_image(self, data, img):
        return self.image_processor.data_to_image(data, img)


# przy bezpośrednim uruchomieniu testujemy na screenie uruchomieniu (> python flappy_bird.py)
if __name__ == "__main__":
    img_in = cv2.imread("./images/game_screen_2.png")
    fb = FlappyBird()
    data_out = fb.image_to_data(img_in)
    print(data_out)
    img_out = fb.data_to_image(data_out, img_in)
    cv2.imshow("image", img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

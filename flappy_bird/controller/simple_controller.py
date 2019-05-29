from pykeyboard import PyKeyboard
import time
from math import sqrt

k = PyKeyboard()


class SimpleController:
    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]

    def take_action(self, data):
        altitude, closest_pipe, bill_to_bird_y = self._prepeare_data(data)

        print(altitude, closest_pipe, bill_to_bird_y)

        if altitude < closest_pipe - 20:
            print("TAP!")
            k.press_key("space")
            k.release_key("space")
            # time.sleep(0.09)
        else:
            print("STAY!")

    def _prepeare_data(self, data):
        if not data["bird"]:
            altitude = -1
        else:
            altitude = self.window_height - data["bird"][1]

        closest_pipe = 200
        if data["pipe"]:
            print("got pipe")
            closest_pipe = self.window_height - data["pipe"][0][1]

        bill_to_bird_y = 0
        if data["bill"]:
            bill_to_bird_y = data["bird"][1] - data["bill"][1]

        return altitude, closest_pipe, bill_to_bird_y

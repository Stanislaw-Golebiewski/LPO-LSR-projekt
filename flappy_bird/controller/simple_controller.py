from pykeyboard import PyKeyboard
import time
from math import sqrt


class SimpleController:
    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]
        self.prev_closest_edge = (200, int(window_size[1] / 2))
        self.prev_bill_tilt = 0
        self.k = PyKeyboard()

    def take_action(self, data):
        bird_y, bill_tilt, closest_edge = self._prepeare_data(data)
        if bird_y == -1:
            pass
        print(f"bird: {bird_y} | bill tilt: {bill_tilt} | closest_edge: {closest_edge}")

        if bird_y > closest_edge[1] + 10 and bill_tilt < 0 and bill_tilt <= self.prev_bill_tilt:
            print("TAP")
            self.k.press_key("space")
            self.k.release_key("space")
            time.sleep(0.03)
        elif bird_y > closest_edge[1] + 40 and bill_tilt <= self.prev_bill_tilt:
            print("TAP")
            self.k.press_key("space")
            self.k.release_key("space")
            time.sleep(0.03)

        self.prev_bill_tilt = bill_tilt

    def _prepeare_data(self, data):
        altitude = bill_tilt = -1
        closest_edge = self.prev_closest_edge
        if not data["bird"]:
            return altitude, bill_tilt, closest_edge
        altitude = data["bird"][1]

        if data["bill"]:
            bill_tilt = data["bird"][1] - data["bill"][1]

        if data["closest_edge"]:
            self.prev_closest_edge = data["closest_edge"]
            closest_edge = data["closest_edge"]
        else:
            closest_edge = self.prev_closest_edge
            
        return altitude, bill_tilt, closest_edge

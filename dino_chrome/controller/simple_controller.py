import time
from pykeyboard import PyKeyboard


class SimpleController:
    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]
        self.k = PyKeyboard()
        self.ground_y = None
        self.flying = None

    def take_action(self, data):
        if data["dinosaur"] and not self.ground_y:
            self.ground_y = data["dinosaur"][1]

        if data["dinosaur"][1] < self.ground_y:
            self.flying = True
            print(f"FLYING! {data['dinosaur'][1]}")
        else:
            self.flying = False

        if data["obstacles"] and not self.flying:
            closest_target_dist = data["obstacles"][0][0] - data['dinosaur'][1]
            if closest_target_dist > 0 and closest_target_dist < 80:
                pass
                # print(closest_target_dist)
                # self.k.tap_key("space")
        # print(data)

        # if bird_y > closest_edge[1] + 10 and bill_tilt < 0 and bill_tilt <= self.prev_bill_tilt:
        #     print("TAP")
        #     self.k.press_key("space")
        #     self.k.release_key("space")
        #     time.sleep(0.03)
        # elif bird_y > closest_edge[1] + 40 and bill_tilt <= self.prev_bill_tilt:
        #     print("TAP")
        #     self.k.press_key("space")
        #     self.k.release_key("space")
        #     time.sleep(0.03)

    def low_jump(self):
        self.k.tap_key("space")
        # self.k.release_key("space")

    def high_jump(self):
        pass
        # self.k.press_key("space")
        # time.sleep(0.01)
        # self.k.release_key("space")

    def _prepeare_data(self, data):
        pass

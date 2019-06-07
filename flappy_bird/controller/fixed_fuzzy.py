import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from pykeyboard import PyKeyboard
import time
import matplotlib.pyplot as plt


def fuzzy_linear_fnc(arr, A, B):
    fnc_a = (A[1] - B[1]) / (A[0] - B[0])
    fnc_b = A[1] - fnc_a * A[0]
    temp_arr = arr * fnc_a + fnc_b
    for x in range(len(temp_arr)):
        if temp_arr[x] < 0:
            temp_arr[x] = 0.0
        elif temp_arr[x] > 1:
            temp_arr[x] = 1.0

    return temp_arr


class FixedFuzzy:
    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]
        self.k = PyKeyboard()
        self.prev_closest_edge = None
        self.prev_bird_pos = None
        self.prev_bill_y = 0
        self.prev_alt = 0

        height_x = np.arange(-self.window_height, self.window_height, 1)
        height = ctrl.Antecedent(height_x, 'height')
        height['too_high'] = fuzzy_linear_fnc(height_x, (20, 0), (200, 1))
        height['too_low'] = fuzzy_linear_fnc(height_x, (-100, 1), (-20, 0))
        height['perfect'] = fuzz.trimf(height_x, [-30, 0, 35])

        # height.view()
        # plt.show()

        bill_tilt_x = np.arange(-30, 10, 1)
        bill_tilt = ctrl.Antecedent(bill_tilt_x, 'bill_tilt')
        bill_tilt["pitched"] = fuzzy_linear_fnc(bill_tilt_x, (-15, 1), (0, 0))
        bill_tilt["raised"] = fuzzy_linear_fnc(bill_tilt_x, (0, 0), (5, 1))

        # bill_tilt_x = np.arange(-40, 40, 1)
        # bill_tilt = ctrl.Antecedent(bill_tilt_x, 'bill_tilt')
        # bill_tilt['pitched'] = fuzzy_linear_fnc(bill_tilt_x, (-20, 1), (1, 0))
        # bill_tilt['raised'] = fuzzy_linear_fnc(bill_tilt_x, (-1, 0), (1, 40))

        alt_change_x = np.arange(-self.window_height, self.window_height, 1)
        alt_change = ctrl.Antecedent(alt_change_x, 'alt_change')
        alt_change['positive'] = fuzzy_linear_fnc(alt_change_x, (1, 0), (20, 1))
        alt_change['negative'] = fuzzy_linear_fnc(alt_change_x, (-40, 1), (-1, 0))
        alt_change['unchanged'] = fuzz.trimf(height_x, [-2, 0, 2])

        tap_x = np.arange(0, 10, 1)
        tap = ctrl.Consequent(tap_x, 'tap')
        tap['should_tap'] = fuzzy_linear_fnc(tap_x, (5, 0), (10, 1))
        tap['should_not_tap'] = fuzzy_linear_fnc(tap_x, (0, 1), (6, 0))

        # rules
        rule1 = ctrl.Rule(height['too_low'], tap['should_tap'])
        rule2 = ctrl.Rule(height['too_high'], tap['should_not_tap'])
        rule3 = ctrl.Rule(height['perfect'] & alt_change['negative'], tap['should_tap'])
        rule4 = ctrl.Rule(height['perfect'] & alt_change['positive'], tap['should_not_tap'])
        rule5 = ctrl.Rule(height['perfect'] & alt_change['unchanged'], tap['should_not_tap'])


        # rule2 = ctrl.Rule(height['too_low'] & bill_tilt['raised'], tap['should_not_tap'])
        # rule3 = ctrl.Rule(height['too_high'], tap['should_not_tap'])
        # rule4 = ctrl.Rule(height['perfect'] & bill_tilt['raised'], tap['should_not_tap'])
        # rule5 = ctrl.Rule(height['perfect'] & bill_tilt['pitched'], tap['should_tap'])
        # rule6 = ctrl.Rule(bill_tilt['raised'], tap['should_not_tap'])

        fb_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.controller = ctrl.ControlSystemSimulation(fb_ctrl)

    def take_action(self, data):
        dst, alt, bld, pbl = self._prepeare_data(data)
        self.controller.input['height'] = alt
        self.controller.input['alt_change'] = alt - self.prev_alt
        # self.controller.input['bill_tilt'] = bld - pbl
        print(f"dst: {dst} | alt: {alt} | h_change: {alt - self.prev_alt}  | b_change: {bld - pbl}")
        self.controller.compute()
        # print(f"dst: {dst} | alt: {alt} | h_change: {alt - self.prev_alt}  | b_change: {bld - pbl} | cnt: {int(self.controller.output['tap'])}")
        self.prev_alt = alt
        if self.controller.output['tap'] > 5.0:
            self.k.press_key("space")
            print("TAP!")
            self.k.release_key("space")

    def _prepeare_data(self, data):
        if data["bird"]:
            bird = data["bird"]
            self.prev_bird_pos = data["bird"]
        else:
            bird = self.prev_bird_pos

        if data["closest_edge"]:
            cle = data["closest_edge"]
            self.prev_closest_edge = data["closest_edge"]
        elif self.prev_closest_edge:
            cle = self.prev_closest_edge
        else:
            cle = (self.window_width, int(self.window_height / 2))

        prev_bill = self.prev_bill_y
        dist_to_edge = cle[0] - bird[0]
        dist_to_optimal_height = cle[1] - bird[1] + 40
        fill_delta_y = bird[1] - data["bill"][1]
        # bill_change = self.prev_bill_delta_y - fill_delta_y

        self.prev_bill_y = fill_delta_y

        return dist_to_edge, dist_to_optimal_height, fill_delta_y, prev_bill

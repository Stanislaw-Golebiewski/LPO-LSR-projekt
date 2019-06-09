import cv2


class ColorMatching:

    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]
        self.masks = {
                 "obstacles": {
                     "lower": (30, 22, 72),
                     "upper": (45, 255, 255),
                     },
                 "dinosaur": {
                     "lower": (70, 85, 72),
                     "upper": (200, 255, 255),
                     }
                 }

    def image_to_data(self, img) -> dict:
        '''
        process an image and extract bird and closest pipes positions
        '''
        out = {}
        # img_out = img.copy()

        for object_name in ["obstacles", "dinosaur"]:
            # dolna i górna wartość filtra HSV
            lower_filter = self.masks[object_name]["lower"]
            upper_filter = self.masks[object_name]["upper"]

            # filtrowanie i dylacja (erozja jest niepotrzebna)
            blurred = cv2.GaussianBlur(img, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_filter, upper_filter)
            # mask = cv2.erode(mask, None, iterations=2)
            # mask = cv2.dilate(mask, None, iterations=4)
            # wyznaczenie konturów
            cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(img_out, cnts, -1, (0, 0, 255), 2)
            if cnts:
                if object_name == "obstacles":
                    out[object_name] = sorted([cv2.boundingRect(c) for c in cnts], key=lambda x: x[0])
                elif object_name == "dinosaur":
                    c = max(cnts, key=cv2.contourArea)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    out[object_name] = center
            else:
                out[object_name] = None

        return out

    def data_to_image(self, data, img):
        img_out = img.copy()
        for object_name in data:
            if not data[object_name]:
                continue
            if object_name == "dinosaur":
                center = data[object_name]
                cv2.circle(img_out, center, 5, (0, 255, 0), -1)
            elif object_name == "obstacles":
                for obs in data["obstacles"]:
                    p1 = (obs[0], obs[1])
                    p2 = (obs[0] + obs[2], obs[1] + obs[3])
                    cv2.rectangle(img_out, obs, (255, 0, 0), 2, -1)

        return img_out

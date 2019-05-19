import cv2


class ColorMatching:

    def __init__(self):
        self.masks = {"bird": {
                     "lower": (11, 64, 193),
                     "upper": (33, 216, 222),
                     },
                 "bill": {
                     "lower": (0, 160, 230),
                     "upper": (255, 255, 255),
                     },
                 "pipe": {
                     "lower": (36, 119, 0),
                     "upper": (155, 203, 255),
                     }
                 }

    def image_to_data(self, img) -> dict:
        '''
        process an image and extract bird and closest pipes positions
        returns:
        {
           "bird": (bird_x, bird_y), # or None
           "pipe": [(pipe_x, pipe_y, pipe_w, pipe_h), ...] # or None
        }
        '''
        out = {}

        for object_name in ["bird", "pipe"]:
            # dolna i górna wartość filtra HSV
            lower_filter = self.masks[object_name]["lower"]
            upper_filter = self.masks[object_name]["upper"]

            # filtrowanie i dylacja (erozja jest niepotrzebna)
            blurred = cv2.GaussianBlur(img, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_filter, upper_filter)
            # mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # wyznaczenie konturów
            cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(img_out, cnts, -1, (0, 255, 0), 3)

            if cnts:
                if object_name == "pipe":
                    out[object_name] = [cv2.boundingRect(c) for c in cnts]
                else:
                    c = max(cnts, key=cv2.contourArea)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    out[object_name] = center
            else:
                out[object_name] = None

        return out

    def data_to_image(self, data, img):
        img_out = img.copy()
        for object in data:
            if not data[object]:
                continue
            if object == "bird":
                center = data[object]
                cv2.circle(img_out, center, 5, (0, 0, 255), -1)
            elif object == "pipe":
                for p in data[object]:
                    x, y, w, h = p
                    cv2.rectangle(img_out, (x, y), (x + w, y + h), (0, 255, 255), 2)
        return img_out

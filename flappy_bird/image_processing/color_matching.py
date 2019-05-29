import cv2


class ColorMatching:

    def __init__(self):
        self.masks = {"bird": {
                     "lower": (11, 64, 193),
                     "upper": (33, 216, 222),
                     },
                 "bill": {
                     "lower": (0, 118, 65),
                     "upper": (5, 205, 255),
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
        # img_out = img.copy()

        for object_name in ["bird", "pipe", "bill"]:
            # dolna i górna wartość filtra HSV
            lower_filter = self.masks[object_name]["lower"]
            upper_filter = self.masks[object_name]["upper"]

            # filtrowanie i dylacja (erozja jest niepotrzebna)
            blurred = cv2.GaussianBlur(img, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_filter, upper_filter)
            # mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=4)

            # wyznaczenie konturów
            cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # if object_name == "bird":
            #     cv2.drawContours(img_out, cnts, -1, (0, 0, 255), 2)

            if cnts:
                if object_name == "pipe":
                    # out[object_name] = [cv2.boundingRect(c) for c in cnts]
                    out[object_name] = []
                    pipes = [cv2.boundingRect(c) for c in cnts]
                    temp_dict = {}
                    for box in pipes:
                        x = box[0]
                        if x not in temp_dict:
                            temp_dict[x] = [box]
                        else:
                            temp_dict[x].append(box)

                    for x in temp_dict:
                        pair = temp_dict[x]
                        if len(pair) == 1:
                            continue
                        if pair[0][1] < pair[1][1]:
                            up = pair[0]
                            down = pair[1]
                        else:
                            up = pair[1]
                            down = pair[0]
                        # pipe_center = (up[1] + up[3] + int((down[1] - up[1])/2), up[0] + int(up[2]/2))
                        pipe_center = (up[0] + int(up[2]/2), up[1] + up[3] + int((down[1] - up[3])/2))
                        # pipe_center = (down[0], down[1])
                        out[object_name].append(pipe_center)

                else:
                    c = max(cnts, key=cv2.contourArea)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    # if object_name == "bird":
                    #     cv2.circle(img_out, center, 5, (0, 0, 255), -1)
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
                for center in data[object]:
                    cv2.circle(img_out, center, 5, (0, 255, 255), -1)
            elif object == "bill":
                center = data[object]
                cv2.circle(img_out, center, 5, (255, 0, 0), -1)
                # for p in data[object]:
                #     x, y, w, h = p
                #     cv2.rectangle(img_out, (x, y), (x + w, y + h), (0, 255, 255), 2)
        return img_out

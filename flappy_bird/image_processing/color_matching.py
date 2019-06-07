import cv2


class ColorMatching:

    def __init__(self, window_size):
        self.window_width = window_size[0]
        self.window_height = window_size[1]
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
                    out[object_name] = []
                    pipes = [cv2.boundingRect(c) for c in cnts]
                    pipes_dict = {}
                    # posegreguj wykryte rury w pary
                    for box in pipes:
                        x = box[0]
                        if x not in pipes_dict:
                            pipes_dict[x] = [box]
                        else:
                            pipes_dict[x].append(box)
            
                    all_pipes = []
                    for x in pipes_dict:
                        pair = pipes_dict[x]
                        # odrzuć jeśli to nie jest para
                        if len(pair) != 2:
                            continue
                        # zdecyduj która jest górna a która dolna
                        if pair[0][1] < pair[1][1]:
                            up = pair[0]
                            down = pair[1]
                        else:
                            up = pair[1]
                            down = pair[0]
                        
                        # pipe_center = (up[0] + int(up[2]/2), up[1] + up[3] + int((down[1] - up[3])/2))

                        # obliczamy prostokąt z wolnym miejscem między rurami
                        pipe_x = up[0]
                        pipe_y = up[1] + up[3]
                        pipe_w = up[2]
                        pipe_h = int(down[1] - up[3])
                        out[object_name].append((pipe_x, pipe_y, pipe_w, pipe_h))
                else:
                    # oblicz środek największego znalezionego konturu (ptak lub dziób)
                    c = max(cnts, key=cv2.contourArea)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    out[object_name] = center
            else:
                out[object_name] = None

        # oblicz najbliższą krawędź (dodajemy 20 px zapasu)
        if out["pipe"] and out["bird"]:
            closest_edge_y = int(self.window_height / 2)
            closest_edge_x = 10000
            temp_bird_x = out["bird"][0]

            for p in out["pipe"]:
                # jeśli ptak jest za krawędzią
                if p[0] + p[2] + 10 < temp_bird_x:
                    continue
                # jeśli ptka jest między krawędziemi danej rury
                elif p[0] - 10 < temp_bird_x < p[0] + p[2] + 10:
                    closest_edge_x = p[0] + p[2] + 60
                    closest_edge_y = p[1] + int(p[3] / 2)
                    break
                elif p[0] - 10 > temp_bird_x and p[0] - temp_bird_x < closest_edge_x:
                    closest_edge_x = p[0] - 60
                    closest_edge_y = p[1] + int(p[3] / 2)
            out["closest_edge"] = (closest_edge_x, closest_edge_y)
        else:
            out["closest_edge"] = None

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
                    # left upper - x, y
                    lu_p = (p[0], p[1])
                    # right upper - x + width, y
                    ru_p = (p[0] + p[2], p[1])
                    # left lower - x, y + height
                    ll_p = (p[0], p[1] + p[3])
                    # right lower - x + width, y + height
                    rl_p = (p[0] + p[2], p[1] + p[3])
                    for point in [lu_p, ru_p, ll_p, rl_p]:
                        cv2.circle(img_out, point, 5, (0, 255, 255), -1)

            elif object == "bill":
                center = data[object]
                cv2.circle(img_out, center, 5, (255, 0, 0), -1)
            elif object == "closest_edge":
                center = data["closest_edge"]
                line_1 = [(center[0], center[1] + 30), (center[0], center[1] - 30)]
                line_2 = [(center[0] - 30, center[1]), (center[0] + 30, center[1])]
                cv2.circle(img_out, data["closest_edge"], 5, (45, 125, 64), -1)
                cv2.line(img_out, line_1[0], line_1[1], (45, 125, 65), 2, cv2.LINE_4, 0)
                cv2.line(img_out, line_2[0], line_2[1], (45, 125, 65), 2, cv2.LINE_4, 0)
        return img_out

import cv2
import mss
import numpy as np


drawing = False
rectStart = (0, 0)
rectStop = (1, 1)


def mouse_callback(event, x, y, flags, param):
    """
    obsługa zdarzeń myszki
    """
    global drawing, rectStart, rectStop, screen_img

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            print(f"Start in: {x} {y}")
            rectStart = (x, y)
            drawing = True
        else:
            print(f"Stop in: {x} {y}")
            rectStop = (x, y)
            drawing = False
            cv2.rectangle(screen_img, rectStart, rectStop, (0, 255, 0), 2)


# przejęcie jednej klatki
with mss.mss() as sct:
    # tutaj można zmienić w przypadku pobierania obrazu z innego monitora
    monitor = sct.monitors[0]
    print(monitor)
    screen_img = np.array(sct.grab(monitor))

# screen_img_copy = screen_img.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_callback)

while True:
    cv2.imshow("image", screen_img)
    k = cv2.waitKey(33)
    # 27 - Esc
    if k == 27:
        break


cv2.destroyAllWindows()

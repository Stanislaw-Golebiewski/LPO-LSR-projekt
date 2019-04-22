import time
import cv2
import mss
import numpy as np


drawing = False
rectanglePicked = False
rectStart = (-1, -1)
rectStop = (-1, -1)

instructions = """
"-------------------
Zaznacz obszar klikając w jego lewy-górny i prawy-górny róg.

[S] - podgląd zaznaczonego miejsca
[D] - wyjście z podglądu
[Esc] - zakończ prace
-----------------"
"""


def crop_window_mouse_callback(event, x, y, flags, param):
    global drawing, rectStart, rectStop, screen_img, screen_img_clear

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            print(f"Start in: {x} {y}")
            rectStart = (x, y)
            drawing = True
        else:
            print(f"Stop in: {x} {y}")
            rectStop = (x, y)
            drawing = False
            rectanglePicked = True
            cv2.rectangle(screen_img, rectStart, rectStop, (255, 0, 0), 2)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            screen_img = screen_img_clear.copy()
            cv2.rectangle(screen_img, rectStart, (x, y), (255, 0, 0), 2)


SEC = 5
print(f"Zrzut zostanie wykonany za {SEC} sekund")
for i in range(SEC, 0, -1):
    print(i)
    time.sleep(1)

# weź jedną klatkę
with mss.mss() as sct:
    # tutaj można zmienić w przypadku pobierania obrazu z innego monitora
    monitor = sct.monitors[0]
    print("monitor:", monitor)
    screen_img = np.array(sct.grab(monitor))

print(instructions)

screen_img_clear = screen_img.copy()
screen_img_cropped = screen_img.copy()

cv2.namedWindow("image")
cv2.moveWindow("image", 0, 0)
cv2.setMouseCallback("image", crop_window_mouse_callback)

showCropWindow = False


while True:
    cv2.imshow("image", screen_img)
    k = cv2.waitKey(17)
    """
    Esc --> 27
    S   --> 100
    D   --> 115
    """
    if k == 27:
        break
    elif k == 115:
        if not showCropWindow:
            screen_img_cropped = screen_img_clear[rectStart[1]:rectStop[1], rectStart[0]:rectStop[0]]
            screen_img = screen_img_cropped.copy()
            showCropWindow = True
    elif k == 100:
        if showCropWindow:
            screen_img = screen_img_clear.copy()
            showCropWindow = False


cv2.destroyAllWindows()

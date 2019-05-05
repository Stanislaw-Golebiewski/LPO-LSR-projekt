import time
import cv2
import mss
import json
import numpy as np

NO_WAIT_SEC = 5
OUT_FILE_NAME = "screen.json"

drawing = False
rectanglePicked = False
rectStart = (-1, -1)
rectStop = (-1, -1)

instructions = """
-------------------
Zaznacz obszar klikając w jego lewy-górny i prawy-górny róg.

[Z] - podgląd/wyjście z podglądu zaznaczonego miejsca
[X] - zapisz współrzędne obrazu do pliku screen.json
[C] - zapisz obraz do pliku
[Esc] - zakończ prace
-------------------
"""


def crop_window_mouse_callback(event, x, y, flags, param):
    global drawing, rectStart, rectStop, screen_img, screen_img_clear, rectanglePicked

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


def get_mss_object(t1, t2):
    """
    Z dwóch par koordynatów stworzy słownik gotowy do przekazania do funkcji mss.grab()
    t1, t2: (x, y)
    """
    return {'left': t1[0], 'top': t1[1], 'width': t2[0] - t1[0], 'height': t2[1] - t1[1]}


print(f"Zrzut zostanie wykonany za {NO_WAIT_SEC} sekund")
for i in range(NO_WAIT_SEC, 0, -1):
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
    # ~ 1000 / 17 =~ 60 fps
    k = cv2.waitKey(17)
    """
    Esc --> 27
    C   --> 99
    D   --> 100
    S   --> 115
    X   --> 120
    Z   --> 122
    """
    if k == 27:
        break
    elif k == 122:
        if not showCropWindow:
            screen_img_cropped = screen_img_clear[rectStart[1]:rectStop[1], rectStart[0]:rectStop[0]]
            screen_img = screen_img_cropped.copy()
            showCropWindow = True
        else:
            screen_img = screen_img_clear.copy()
            showCropWindow = False
    elif k == 120:
        data = get_mss_object(rectStart, rectStop)
        print(data)
        with open(OUT_FILE_NAME, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"zapisano do pliku {OUT_FILE_NAME}")
    elif k == 99:
        filename = input("nazwa pliku: ")
        cv2.imwrite(f"{filename}.png", screen_img)

cv2.destroyAllWindows()

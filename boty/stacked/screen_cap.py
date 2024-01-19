import mss
import cv2 as cv
import numpy as np
from win32gui import FindWindow, GetWindowRect, SetForegroundWindow
import time

class ScreenCapture:
    def __init__(self, window_title):
        self.window_title = window_title
        self.stc = mss.mss()

    def capture_screen(self):
        # Fetch the window handle and its rectangle each time
        window_handle = FindWindow(None, self.window_title)
        if window_handle == 0:
            raise Exception("Window not found: {}".format(self.window_title))

        window_rect = GetWindowRect(window_handle)
        x0, y0, x1, y1 = window_rect
        width = x1 - x0
        height = y1 - y0

        # Capture the screen
        scr = self.stc.grab({
            'left': x0,
            'top': y0,
            'width': width,
            'height': height
        })

        img = np.array(scr)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        return img

    def start_capture(self):
        while True:
            screenshot = self.capture_screen()
            cv.imshow("Screenshot", screenshot)

            loop_time = time.time()
            key = cv.waitKey(3000)

            if key == ord("q"):
                cv.destroyAllWindows()
                break
            elif key == ord('f'):
                print("[INFO] Screenshot taken...")
                cv.imwrite('screenshots/{}.jpg'.format(loop_time), screenshot)

        print("[INFO] Done.")

if __name__ == "__main__":
    capture = ScreenCapture("Path of Exile")
    capture.start_capture()
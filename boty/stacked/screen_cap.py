from time import time
import mss
import cv2 as cv
import numpy as np
from win32gui import FindWindow, GetWindowRect, SetForegroundWindow

class ScreenCapture:
    def __init__(self, window_title):
        self.window_title = window_title
        self.window_handle = FindWindow(None, self.window_title)
        if self.window_handle == 0:
            raise Exception("Window not found: {}".format(self.window_title))
        
        # Get the entire window rectangle
        self.window_rect = GetWindowRect(self.window_handle)
        self.x0, self.y0, x1, y1 = self.window_rect
        self.w, self.h = x1 - self.x0, y1 - self.y0  # Width and height of the window

        # Adjust these if there's a border or title bar that shouldn't be captured
        self.x_corr = 8
        self.y_corr = 31

        self.stc = mss.mss()

    def capture_screen(self):
        # Adjust these if the window is not positioned at the top-left corner of your screen
        left = self.x0 + self.x_corr
        top = self.y0 + self.y_corr

        scr = self.stc.grab({
            'left': left,
            'top': top,
            'width': self.w,
            'height': self.h
        })

        img = np.array(scr)
        img = cv.cvtColor(img, cv.IMREAD_COLOR)

        return img

    def start_capture(self):
        SetForegroundWindow(self.window_handle)

        while True:
            screenshot = self.capture_screen()
            cv.imshow("Screenshot", screenshot)

            loop_time = time()
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


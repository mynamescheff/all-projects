import cv2 as cv
import numpy as np
import pyautogui
import time
from screen_cap import ScreenCapture

class ItemAutomation(ScreenCapture):
    def __init__(self, window_title, item_template_path):
        super().__init__(window_title)
        self.item_template = cv.imread(item_template_path, cv.IMREAD_UNCHANGED)

    def find_item_position(self, screenshot):
        # Convert screenshot to grayscale
        screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        template_gray = cv.cvtColor(self.item_template, cv.COLOR_BGR2GRAY)

        # Template matching to find the item
        result = cv.matchTemplate(screenshot_gray, template_gray, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        # Threshold for matching
        threshold = 0.8
        if max_val >= threshold:
            return max_loc
        return None

    def click_item(self, position, click_type="right"):
        x, y = position
        pyautogui.moveTo(x, y)
        if click_type == "right":
            pyautogui.rightClick()
        else:
            pyautogui.leftClick()

    def start_automation(self):
        while True:
            screenshot = self.capture_screen()
            item_position = self.find_item_position(screenshot)
            
            if item_position:
                # Adjust the position to the center of the found item
                item_center = (item_position[0] + self.item_template.shape[1] // 2,
                               item_position[1] + self.item_template.shape[0] // 2)

                # Click the item
                self.click_item(item_center, click_type="right")

                # Assuming a fixed position for the empty space (you can modify this as needed)
                empty_space_position = (item_center[0] + 50, item_center[1] + 50)
                self.click_item(empty_space_position, click_type="left")

                print("[INFO] Item transformed and moved.")
                time.sleep(2)  # Wait for a while before next action
            
            key = cv.waitKey(1000)  # Wait for 1 second to press key
            if key == ord("q"):
                cv.destroyAllWindows()
                break

        print("[INFO] Automation done.")

if __name__ == "__main__":
    window_title = "Path of Exile"
    item_template_path = "boty/stacked/stacked.jpg"  # Path to the image template of the item stack
    automation = ItemAutomation(window_title, item_template_path)
    automation.start_automation()

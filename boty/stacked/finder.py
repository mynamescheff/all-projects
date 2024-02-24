import cv2 as cv
import numpy as np
import time
from screen_cap import ScreenCapture
import pyautogui
import random
import time

# Load the template image (the item to be identified)
template_path = 'boty/stacked/stacked.jpg'
template = cv.imread(template_path)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)  # Convert template to grayscale

# Define a function to find and box the item in a given screenshot
def find_and_box_item(screenshot, template):
    screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    # Perform template matching
    res = cv.matchTemplate(screenshot_gray, template, cv.TM_CCOEFF_NORMED)

    # Define a threshold for detection
    threshold = 0.8
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region
    item_boxes = []
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (pt[0] + w, pt[1] + h)
        item_boxes.append((top_left, bottom_right))
        cv.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 2)
    return screenshot, item_boxes

# Load the template image for equipment slots (the empty slots to be highlighted)
slots_template_path = 'boty/stacked/eq_slot.jpg'  # Replace with your actual template path
slots_template = cv.imread(slots_template_path)
slots_template_gray = cv.cvtColor(slots_template, cv.COLOR_BGR2GRAY)  # Convert template to grayscale

# Define a function to find and box the empty slots in a given screenshot
def find_and_box_slots(screenshot, slots_template):
    screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    w, h = slots_template.shape[::-1]

    # Perform template matching for slots
    res = cv.matchTemplate(screenshot_gray, slots_template, cv.TM_CCOEFF_NORMED)

    # Define a threshold for detection
    threshold = 0.8
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region
    slot_boxes = []
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (pt[0] + w, pt[1] + h)
        slot_boxes.append((top_left, bottom_right))
        cv.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
    return screenshot, slot_boxes



# Initialize screen capture for the game window
capture = ScreenCapture("Path of Exile")

# Start a loop that captures the screen every 3 seconds
try:
    while True:
        screenshot = capture.capture_screen()
        result_image, item_boxes = find_and_box_item(screenshot, template_gray)
        result_image_with_slots, slot_boxes = find_and_box_slots(result_image, slots_template_gray)

        # Now you have item_boxes and slot_boxes variables that contain the coordinates
        # You can use these variables for further processing

        cv.imshow("Detected Items and Slots", result_image_with_slots)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(3)  # Wait for 3 seconds before capturing the screen again

finally:
    cv.destroyAllWindows()

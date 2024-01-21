import cv2 as cv
import numpy as np
import time
from screen_cap import ScreenCapture

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
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        cv.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    return screenshot

# Initialize screen capture for the game window
capture = ScreenCapture("Path of Exile")

# Start a loop that captures the screen every 3 seconds
try:
    while True:
        screenshot = capture.capture_screen()
        result_image = find_and_box_item(screenshot, template_gray)
        cv.imshow("Detected Items", result_image)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(3)  # Wait for 3 seconds before capturing the screen again

finally:
    cv.destroyAllWindows()

import cv2 as cv
import numpy as np
from screen_cap import ScreenCapture
import os

# Load the template image (the item to be identified)
template_path = 'boty/stacked/stacked.jpg'
template = cv.imread(template_path)


# Convert template to grayscale (if needed for template matching)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

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

# Placeholder for screenshot capturing code
# This is where you would integrate with your ScreenCapture class
# For now, let's just assume screenshot is the template for demonstration purposes
result_image = find_and_box_item(template, template_gray)

# Display the result
cv.imshow("Detected Items", result_image)
cv.waitKey(0)
cv.destroyAllWindows()
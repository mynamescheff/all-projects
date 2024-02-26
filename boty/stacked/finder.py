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
    red_boxes = []
    for pt in zip(*loc[::-1]):
        cv.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        red_boxes.append((pt[0], pt[1], pt[0] + w, pt[1] + h))
    return screenshot, red_boxes

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
    green_boxes = []
    for pt in zip(*loc[::-1]):
        cv.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        green_boxes.append((pt[0], pt[1], pt[0] + w, pt[1] + h))
    return screenshot, green_boxes

# Function to move the mouse to a point with random human-like movements
def human_like_mouse_move(x, y, duration=1):
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)

# Function to perform a right-click within a random area of the red box
def random_right_click_within_box(box_coords):
    # box_coords is a tuple: (x_start, y_start, x_end, y_end)
    x_start, y_start, x_end, y_end = box_coords
    x = random.randint(x_start, x_end)
    y = random.randint(y_start, y_end)
    human_like_mouse_move(x, y)
    pyautogui.click(button='right')

# Function to perform a left-click within a random area of one of the green boxes
def random_left_click_within_boxes(boxes_coords):
    box_coords = random.choice(boxes_coords)
    x_start, y_start, x_end, y_end = box_coords
    x = random.randint(x_start, x_end)
    y = random.randint(y_start, y_end)
    human_like_mouse_move(x, y)
    pyautogui.click(button='left')

red_box_coords = []  # List to store the coordinates of the red boxes
green_boxes_coords = []  # List to store the coordinates of the green boxes

# Initialize screen capture for the game window
capture = ScreenCapture("Path of Exile")

# Start a loop that captures the screen every 3 seconds
try:
    while True:
        screenshot = capture.capture_screen()
        result_image, red_box_coords = find_and_box_item(screenshot, template_gray)
        result_image_with_slots, green_boxes_coords = find_and_box_slots(result_image, slots_template_gray)
        
        cv.imshow("Detected Items and Slots", result_image_with_slots)
        
        # Perform the clicks if red and green boxes are found
        if red_box_coords and green_boxes_coords:
            red_box = random.choice(red_box_coords)
            random_right_click_within_box(red_box)
            random_left_click_within_boxes(green_boxes_coords)
        
        # Break the loop and exit the program if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(3)  # Wait for 3 seconds before capturing the screen again

finally:
    cv.destroyAllWindows()
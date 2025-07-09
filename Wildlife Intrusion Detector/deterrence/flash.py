import cv2
import numpy as np
import time

def trigger_flash(duration=1):
    # Create a white image (fullscreen white flash)
    screen_width = 1920
    screen_height = 1080
    flash = np.ones((screen_height, screen_width, 3), dtype=np.uint8) * 255

    cv2.namedWindow("FLASH", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("FLASH", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("FLASH", flash)

    # Wait for given duration in seconds
    cv2.waitKey(int(duration * 1000))

    # Close flash window
    cv2.destroyWindow("FLASH")

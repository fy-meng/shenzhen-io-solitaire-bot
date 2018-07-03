import cv2
import numpy as np
import os


def _get_locations_by_name(screen, name):
    template = cv2.imread('assets/cards/' + name + '.png')
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.99
    loc = np.where(result >= threshold)
    print(name, loc)

    return []


def get_current_layout():
    # os.system('screencapture screen.png')
    screen = cv2.imread('screen.png')

    cards = []

    # flower card
    cards += _get_locations_by_name(screen, 'FF')

    for suit in ('R', 'G', 'B'):
        # dragon cards
        cards += _get_locations_by_name(screen, suit + 'D')
        # regular cards
        for number in range(1, 10):
            name = suit + str(number)
            cards += _get_locations_by_name(screen, name)

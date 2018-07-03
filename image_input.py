import cv2
import numpy as np
import os


def _get_one_location_by_name(screen, name):
    """
    Returns the tuple (NAME, LOC) given by the current SCREEN and the NAME of
    the desired card. LOC is the best fit location for the given card.
    """
    template = cv2.imread('assets/cards/' + name + '.png')
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, _, _, loc = cv2.minMaxLoc(result)
    return name, loc


def _get_locations_by_name(screen, name):
    """
    Returns a list of tuples in the format of (NAME, LOC) given by the current
    SCREEN and the NAME of the desired card. LOC is the best fit location for
    the given card.
    """
    template = cv2.imread('assets/cards/' + name + '.png')
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.99
    locations = np.where(result >= threshold)
    locations = np.array(locations).T.tolist()
    return [(name, tuple(loc)[::-1]) for loc in locations]


def get_current_layout():
    """
    Take a screenshot and returns the Solitaire piles on screen.
    """
    os.system('screencapture screen.png')
    screen = cv2.imread('screen.png')
    os.remove('screen.png')

    cards = []

    # flower card
    cards.append(_get_one_location_by_name(screen, 'FF'))

    for suit in ('R', 'G', 'B'):
        # dragon cards
        cards += _get_locations_by_name(screen, suit + 'D')
        # regular cards
        for number in range(1, 10):
            name = suit + str(number)
            cards.append(_get_one_location_by_name(screen, name))

    cards.sort(key=lambda item: item[1])
    piles = [cards[i:i + 5] for i in range(0, len(cards), 5)]
    piles = [[item[0] for item in pile] for pile in piles]

    return piles

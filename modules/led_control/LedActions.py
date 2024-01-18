from enum import Enum


class LedAction(Enum):
    OFF = 0
    ON = 1

    MODE_TEMP = 2
    MODE_COLOR = 3
    MODE_DYNAMIC_COLOR = 4
    MODE_EFFECTS = 5

    CHANGE_BRIGHTNESS = 6
    SET_BRIGHTNESS = 7

    CHANGE_VALUE = 6
    SET_VALUE = 7




from enum import Enum


class ButtonStatus(Enum):
    EB_NONE = 0
    EB_PRESS = 1
    EB_HOLD = 2
    EB_STEP = 3
    EB_RELEASE = 4
    EB_CLICK = 5
    EB_CLICKS = 6
    EB_REL_HOLD = 7
    EB_REL_HOLD_C = 8
    EB_REL_STEP = 9
    EB_REL_STEP_C = 10

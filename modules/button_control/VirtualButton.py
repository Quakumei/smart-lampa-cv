import time


class VirtualButton:
    # flags
    EB_PRESS = (1 << 0)  # нажатие на кнопку
    EB_HOLD = (1 << 1)  # кнопка удержана
    EB_STEP = (1 << 2)  # импульсноеудержание
    EB_RELEASE = (1 << 3)  # кнопка отпущена
    EB_CLICK = (1 << 4)  # одиночный клик
    EB_CLICKS = (1 << 5)  # сигнал о нескольких кликах
    EB_TURN = (1 << 6)  # поворот энкодера
    EB_REL_HOLD = (1 << 7)  # кнопка отпущена после удержания
    EB_REL_HOLD_C = (1 << 8)  # кнопка отпущена после удержания с предв. кликами
    EB_REL_STEP = (1 << 9)  # кнопка отпущена после степа
    EB_REL_STEP_C = (1 << 10)  # кнопка отпущена после степа с предв. кликами
    # pack flags
    EB_CLKS_R = (1 << 0)
    EB_PRS_R = (1 << 1)
    EB_HLD_R = (1 << 2)
    EB_STP_R = (1 << 3)
    EB_REL_R = (1 << 4)
    EB_PRS = (1 << 5)
    EB_HLD = (1 << 6)
    EB_STP = (1 << 7)
    EB_REL = (1 << 8)
    EB_BUSY = (1 << 9)
    EB_DEB = (1 << 10)
    EB_TOUT = (1 << 11)
    EB_INV = (1 << 12)
    EB_BOTH = (1 << 13)
    EB_BISR = (1 << 14)
    EB_EHLD = (1 << 15)

    # times
    EB_DEB_TIMEOUT = 50  # Debounce timeout in milliseconds
    EB_CLICK_T = 500  # Click timeout
    EB_HOLD_TIMEOUT = 600  # Hold timeout
    EB_STEP_TIMEOUT = 200  # Step timeout

    # ?
    EB_SHIFT = 4
    EB_FOR_SCALE = 6

    def __init__(self):
        self.flags = 0  # To store various states and flags
        self.clicks = 0  # To count the number of clicks
        self.timer = 0  # General purpose timer
        self.ftimer = 0  # Timer for tracking 'for' events
        self.callback = None  # Callback function for button events

    """ Set methods """

    def setHoldTimeout(self, tout):
        """ Set the hold timeout. Default is 600 ms. Max is 4000 ms. """
        self.EB_HOLD_TIMEOUT = tout

    def setStepTimeout(self, tout):
        """ Set the step timeout. Default is 200 ms. Max is 4000 ms. """
        self.EB_STEP_TIMEOUT = tout

    def setClickTimeout(self, tout):
        """ Set the click timeout. Default is 500 ms. Max is 4000 ms. """
        self.EB_CLICK_T = tout

    def setDebTimeout(self, tout):
        """ Set the debounce timeout. Default is 50 ms. Max is 255 ms. """
        self.EB_DEB_TIMEOUT = tout

    def setBtnLevel(self, level: bool):
        self.write_bf(self.EB_INV, not level)

    def pressISR(self):
        """ Call this method when the button is pressed. """
        if not self._read_bf(self.EB_DEB):
            self.timer = self.current_millis()
        self._set_bf(self.EB_DEB | self.EB_BISR)

    def reset(self):
        """ Reset all system flags (forcibly finish processing). """
        self.clicks = 0
        self._clr_bf(~self.EB_INV)

    def clear(self):
        """ Clear event flags. """
        if self._read_bf(self.EB_CLKS_R):
            self.clicks = 0
        flags_to_clear = self.EB_CLKS_R | self.EB_STP_R | self.EB_PRS_R | self.EB_HLD_R | self.EB_REL_R
        if self._read_bf(flags_to_clear):
            self._clr_bf(flags_to_clear)

    def attach(self, handler):
        """ connect an event handler function(like void f())"""
        self.callback = handler

    def detach(self):
        """ disconnect an event handler function"""
        self.callback = None

    """ Get methods """

    def press(self):
        """ Check if the button was pressed. """
        return self._read_bf(self.EB_PRS_R)

    def release(self):
        """ Check if the button is released (in any case) [event] """
        return self._eq_bf(self.EB_REL_R | self.EB_REL, self.EB_REL_R | self.EB_REL)

    def click(self):
        """ Check whether the button has been clicked (released without holding) [event] """
        return self._eq_bf(self.EB_REL_R | self.EB_REL | self.EB_HLD, self.EB_REL_R)

    def pressing(self):
        """ Check if the button is clamped (between press() and release()) [condition] """
        return self._read_bf(self.EB_PRS)

    def hold(self) -> bool:
        """ Check if the button was held down (more timeout) [event] """
        return self._read_bf(self.EB_HLD_R)

    def holdWithClicks(self, num: int) -> bool:
        return self.clicks == num and self.hold()

    def holding(self) -> bool:
        return self._eq_bf(self.EB_PRS | self.EB_HLD, self.EB_PRS | self.EB_HLD)

    def holdingWithClicks(self, num) -> bool:
        return self.clicks == num and self.holding()

    def step(self) -> bool:
        return self._read_bf(self.EB_STP_R)

    def stepWithClicks(self, num: int) -> bool:
        return self.clicks == num and self.step()

    def hasClicks(self) -> bool:
        return self._eq_bf(self.EB_CLKS_R | self.EB_HLD, self.EB_CLKS_R)

    def hasClicksWithClicks(self, num: int) -> bool:
        return self.clicks == num and self.hasClicks()

    def getClicks(self) -> int:
        return self.clicks

    # skip getStep()

    def releaseHold(self) -> bool:
        return self._eq_bf(self.EB_REL_R | self.EB_REL | self.EB_HLD | self.EB_STP, self.EB_REL_R | self.EB_HLD)

    def releaseHoldWithClicks(self, num: int) -> bool:
        return self.clicks == num and self._eq_bf(self.EB_CLKS_R | self.EB_HLD | self.EB_STP,
                                                  self.EB_CLKS_R | self.EB_HLD)

    def releaseStep(self) -> bool:
        return self._eq_bf(self.EB_REL_R | self.EB_REL | self.EB_STP, self.EB_REL_R | self.EB_STP)

    def releaseStepWithClicks(self, num) -> bool:
        return self.clicks == num and self.releaseStep()

    def waiting(self) -> bool:
        return self.clicks and self._eq_bf(self.EB_PRS | self.EB_REL, 0)

    def busy(self) -> bool:
        return self._read_bf(self.EB_BUSY)

    def action(self):
        """
        Returns a code representing the last action of the button.
        """
        action_flags = self.flags & 0b111111111

        if action_flags == (self.EB_PRS | self.EB_PRS_R):
            return "EB_PRESS"
        elif action_flags == (self.EB_PRS | self.EB_HLD | self.EB_HLD_R):
            return "EB_HOLD"
        elif action_flags == (self.EB_PRS | self.EB_HLD | self.EB_STP | self.EB_STP_R):
            return "EB_STEP"
        elif action_flags in [(self.EB_REL | self.EB_REL_R), (self.EB_REL | self.EB_REL_R | self.EB_HLD),
                              (self.EB_REL | self.EB_REL_R | self.EB_HLD | self.EB_STP)]:
            return "EB_RELEASE"
        elif action_flags == self.EB_REL_R:
            return "EB_CLICK"
        elif action_flags == self.EB_CLKS_R:
            return "EB_CLICKS"
        elif action_flags == (self.EB_REL_R | self.EB_HLD):
            return "EB_REL_HOLD"
        elif action_flags == (self.EB_CLKS_R | self.EB_HLD):
            return "EB_REL_HOLD_C"
        elif action_flags == (self.EB_REL_R | self.EB_HLD | self.EB_STP):
            return "EB_REL_STEP"
        elif action_flags == (self.EB_CLKS_R | self.EB_HLD | self.EB_STP):
            return "EB_REL_STEP_C"

        return None

    def timeout(self, tout):
        if self._read_bf(self.EB_TOUT) and (self.current_millis() - self.timer) > tout:
            self._clr_bf(self.EB_TOUT)
            return True
        return False

    def pressFor(self) -> int:
        if self.ftimer:
            return self.current_millis() - self.ftimer
        return 0

    def pressForTime(self, ms: int):
        return self.pressFor() > ms

    def holdFor(self):
        if self._read_bf(self.EB_HLD):
            return self.pressFor() - self.EB_HOLD_TIMEOUT
        return 0

    def holdForTime(self, ms: int):
        return self.holdFor() > ms

    def stepFor(self):
        if self._read_bf(self.EB_STP):
            return self.pressFor() - self.EB_HOLD_TIMEOUT * 2
        return 0

    def stepForTime(self, ms: int):
        return self.stepFor() > ms

    """ Poll methods """

    def tick(self, b0, b1):
        # Handling virtual button composed of b0 and b1
        if self._read_bf(self.EB_BOTH):
            if not b0.pressing() and not b1.pressing():
                self._clr_bf(self.EB_BOTH)
            if not b0.pressing():
                b0.reset()
            if not b1.pressing():
                b1.reset()
            b0.clear()
            b1.clear()
            return self.tick(1)
        else:
            if b0.pressing() and b1.pressing():
                self._set_bf(self.EB_BOTH)
            return self.tick(0)

    def tick(self, s):
        self.clear()
        state_changed = self._pollBtn(s)
        if self.callback and state_changed:
            self.callback()
        return state_changed

    def tickRaw(self, s):
        return self._pollBtn(s)

    # Utility functions
    _flags = 0  # all flags

    def _set_bf(self, flag):
        self.flags |= flag

    def _clr_bf(self, flag):
        self.flags &= ~flag

    def _read_bf(self, flag):
        return bool(self.flags & flag)

    def write_bf(self, x: int, v: bool):
        self._set_bf(x) if v else self._clr_bf(x)

    def _eq_bf(self, x: int, y: int):
        return (self._flags & x) == y

    def _pollBtn(self, s: bool) -> bool:
        if self._read_bf(self.EB_BISR):
            self._clr_bf(self.EB_BISR)
            s = True
        else:
            s ^= self._read_bf(self.EB_INV)
        if not self._read_bf(self.EB_BUSY):
            if s:
                self._set_bf(self.EB_BUSY)
            else:
                return False

        current_time = self.current_millis()
        debounce = current_time - self.timer

        if s:  # Button is pressed
            if not self._read_bf(self.EB_PRS):  # If button was not previously pressed
                if not self._read_bf(self.EB_DEB) and self.EB_DEB_TIMEOUT:  # If debounce is not active
                    self._set_bf(self.EB_DEB)  # Activate debounce
                    self.timer = current_time
                else:  # First press detected
                    if debounce >= self.EB_DEB_TIMEOUT or not self.EB_DEB_TIMEOUT:
                        self._set_bf(self.EB_PRS | self.EB_PRS_R)
                        self.ftimer = current_time
                        self.timer = current_time
            else:  # Button was already pressed
                if not self._read_bf(self.EB_HLD):  # Button not hold
                    if debounce >= self.EB_HOLD_TIMEOUT:
                        self._set_bf(self.EB_HLD | self.EB_HLD_R)
                        self.timer = current_time
                elif not self._read_bf(self.EB_STP):
                    if debounce >= self.EB_STEP_TIMEOUT:
                        self._set_bf(self.EB_STP | self.EB_STP_R)
                        self.timer = current_time
                # Handle other conditions as needed
        else:  # Button is not pressed
            if self._read_bf(self.EB_PRS):  # If button was previously pressed
                if debounce >= self.EB_DEB_TIMEOUT:
                    if not self._read_bf(self.EB_HLD):
                        self.clicks += 1
                    if self._read_bf(self.EB_EHLD):
                        self.clicks = 0
                    self._set_bf(self.EB_REL | self.EB_REL_R)
                    self._clr_bf(self.EB_PRS)
            elif self._read_bf(self.EB_REL):
                if not self._read_bf(self.EB_EHLD):
                    self._set_bf(self.EB_REL_R)
                self._clr_bf(self.EB_REL | self.EB_EHLD)
                self.timer = current_time
            elif self.clicks:
                if self._read_bf(self.EB_HLD | self.EB_STP) or debounce >= self.EB_CLICK_T:
                    self._set_bf(self.EB_CLKS_R)
                elif self.ftimer:
                    self.ftimer = 0
            elif self._read_bf(self.EB_BUSY):
                self._clr_bf(self.EB_HLD | self.EB_STP | self.EB_BUSY)
                self._set_bf(self.EB_TOUT)
                self.ftimer = 0
                self.timer = 0  # test!!

            # Reset debounce if necessary
            if self._read_bf(self.EB_DEB):
                self._clr_bf(self.EB_DEB)

        return self._read_bf(self.EB_CLKS_R | self.EB_PRS_R | self.EB_HLD_R | self.EB_STP_R | self.EB_REL_R)

    @staticmethod
    def current_millis():
        """ Return the current time in milliseconds. """
        return int(time.time() * 1000)
        # return debug_timer


debug_timer = 0


def demo():
    global debug_timer
    """ Example usage """
    button = VirtualButton()
    # Assuming `state` is the current state of the button
    while True:
        state = bool(input())
        button.tick(state)
        print(button.action(), f'{button.flags:16b}')
        debug_timer += 300

import threading
import time

from smbus2 import SMBus
from config.settings import DRIVER_ADDR

from rapprochement import define_catch_pos

class ServoController:
    def __init__(self, acc, max_s, init_pulse):
        self.current_pos = 0
        self.target_pos = 0
        self.current_speed = 0
        self.acceleration = acc
        self.max_speed = max_s
        self.initial_pulse = init_pulse
        self.previous_millis = int(time.time())

    def attach(self, pin):
        return [0, 0, 0xAA]

    def detach(self, pin):
        return [0, 0, 0xBB]

    def set_target_angle(self, angle):
        self.target_pos = max(min(angle, 180), 0)

    def tick(self):
        current_millis = int(time.time())
        deltaTime = (current_millis - self.previous_millis) / 1000.0
        self.previous_millis = current_millis

        if self.current_pos != self.target_pos:
            direction = 1 if self.target_pos > self.current_pos else -1

            # Determine stopping distance, considering current speed and acceleration
            stopping_distance = (self.current_speed * self.current_speed) / (2 * self.acceleration)

            # Determine current distance to target
            distance_to_target = abs(self.target_pos - self.current_pos)

            if abs(self.current_speed) <= 0.01:
                self.current_speed = self.initial_pulse * direction

            # Check if we should continue to accelerate or start decelerating
            if distance_to_target > stopping_distance:
                # Accelerate
                self.current_speed += self.acceleration * direction * deltaTime
            else:
                # Decelerate
                self.current_speed -= self.acceleration * direction * deltaTime

            self.current_speed = max(min(self.current_speed, self.max_speed), -self.max_speed)
            delta = self.current_speed * deltaTime

            if (direction > 0 and delta + self.current_pos >= self.target_pos) or (
                    direction < 0 and delta + self.current_pos <= self.target_pos):
                self.current_pos = self.target_pos
            else:
                self.current_pos += delta

            self.current_pos = max(min(self.current_pos, 180), 0)
            return self.current_pos
        else:
            self.current_speed = 0  # reset speed when target is reached


def main():
    bus = SMBus(0)
    servo1 = ServoController() # нижний
    servo2 = ServoController() # верхний

    def i2c_request(args):
        bus.write_i2c_block_data(DRIVER_ADDR, 0, args)

    def tick_servos():
        hand_prev_x = 0
        hand_prev_y = 0
        while True:
            hand_x = 90 # здесь получаем очередной х руки
            hand_y = 90 # здесь получаем очередной у руки
            (servo1.target_pos, servo2.target_pos) = define_catch_pos(
                servo1,
                servo2,
                hand_x,
                hand_y,
                hand_prev_x,
                hand_prev_y
            )
            hand_prev_x = hand_x
            hand_prev_y = hand_y

            servo1pos = servo1.tick()
            time.sleep(0.01)
            servo2pos = servo2.tick()
            i2c_request([servo1pos, servo2pos])
            time.sleep(0.01)

    # поток генерации I2C-сигналов
    t = threading.Thread(target=tick_servos, daemon=True)
    t.start()

    # тестовые сигналы
    # while True:
    #    bus.write_i2c_block_data(10, 0, [0, 0, 0xAA])# -- зааттачить
    #    time.sleep(1)
    #    bus.write_i2c_block_data(10, 0, [90, 90])# -- задать углы
    #    time.sleep(1)
    #    bus.write_i2c_block_data(10, 0, [180, 180])
    #    time.sleep(1)
    #    bus.write_i2c_block_data(10, 0, [0, 0, 0xBB])# -- задетачить
    #    #print(angle,' out:' ,bus.read_byte_data(ADDR, 0))
    #    time.sleep(0.1)


if __name__ == '__main__':
    main()

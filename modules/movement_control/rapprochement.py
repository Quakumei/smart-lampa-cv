import time
import numpy

def define_catch_pos(
        servo1,    # нижний сервомотор
        servo2,    # верхний сервомотор
        cur_x,     # координата х руки
        cur_y,     # координата у руки
        prev_x,  # предыдущая координата х руки
        prev_y,  # предыдущая координата у руки
    ):
    cur_t = int(time.time())
    prev_t = servo1.previous_millis

    target_x_v = (cur_x - prev_x) / (cur_t - prev_t) # скорость руки по оси х
    target_y_v = (cur_y - prev_y) / (cur_t - prev_t) # скорость руки по оси y

    # уравнение для нахождения момента времени пересечения камеры и руки
    eq_roots =\
    numpy.roots([
        (servo1.acceleration - servo2.acceleration) / 2,
        (cur_y - prev_y - cur_x + prev_x) / (cur_t - prev_t)
            + servo1.current_speed - servo2.current_speed,
        prev_t / (cur_t - prev_t) * (cur_x - prev_x - cur_y + prev_y)
            + servo1.current_pos - servo2.current_pos - prev_x + prev_y
    ])
    # выбираем первый неотрицательный корень
    catch_t = next((root for root in eq_roots if root >= 0), 0)

    # определяем точку перехвата
    catch_x = cur_x + target_x_v * (catch_t - cur_t)
    catch_y = cur_y + target_y_v * (catch_t - cur_t)

    return (catch_x, catch_y)

import sympy as sp
from math import sin, cos

def define_new_camera_pos(
        cam_x,     # положение нижнего сервомотора (вращающегося по оси х)
        cam_y,     # положение верхнего сервомотора (вращающегося по оси у)
        cam_v,     # скорость "камеры"
        cur_x,     # координата х руки
        cur_y,     # координата у руки
        cur_t,     # текущий момент времени
        prev_x,    # предыдущая координата х руки
        prev_y,    # предыдущая координата у руки
        prev_t     # предыдущий момент времени
    ):
    target_x_v = (cur_x - prev_x) / (cur_t - prev_t) # скорость руки по оси х
    target_y_v = (cur_y - prev_y) / (cur_t - prev_t) # скорость руки по оси y

    p, t = sp.symbols('p t')
    eq1 = (cam_v * sp.cos(p) + target_x_v) * t - cur_x + cam_x
    eq2 = (cam_v * sp.sin(p) + target_y_v) * t - cur_y + cam_y
    solution = sp.solve([eq1, eq2], (p, t), dict=True)

    print(solution)

    catch_x = cam_x + cam_v * cos(solution[0 if cur_y > 90 else 1][p]) * solution[0 if cur_y > 90 else 1][t]
    catch_y = cam_y + cam_v * sin(solution[0 if cur_y > 90 else 1][p]) * solution[0 if cur_y > 90 else 1][t]

    return (catch_x, catch_y)

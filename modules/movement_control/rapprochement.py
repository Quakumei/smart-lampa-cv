import numpy

def define_new_camera_pos(
        cam_x,     # положение нижнего сервомотора (вращающегося по оси х)
        cam_y,     # положение верхнего сервомотора (вращающегося по оси у)
        cam_x_a,   # ускорение нижнего сервомотора
        cur_x,     # координата х руки
        cur_y,     # координата у руки
        cur_t,     # момент времени
        cam_x_v=0, # скорость нижнего сервомотора
        prev_x=0,  # предыдущая координата х руки
        prev_y=0,  # предыдущая координата у руки
        prev_t=0   # предыдущий момент времени
    ):
    target_x_v = (cur_x - prev_x) / (cur_t - prev_t) # скорость руки по оси х
    target_y_v = (cur_y - prev_y) / (cur_t - prev_t) # скорость руки по оси y

    # уравнение для нахождения момента времени пересечения камеры и руки
    eq_roots =\
    numpy.roots([
        cam_x_a / 2,
        cam_x_v - target_x_v,
        target_x_v * prev_t + cam_x - prev_x
    ])
    # выбираем первый неотрицательный корень
    catch_t = next((root for root in eq_roots if root >= 0), 0)

    # определяем точку перехвата
    catch_x = prev_x + target_x_v * catch_t
    catch_y = prev_y + target_y_v * catch_t

    # вычисляем отношение расстояния, пройденного рукой, к расстоянию до точки перехвата
    x_coeff = abs((cur_x - prev_x) / (catch_x - prev_x))
    y_coeff = abs((cur_y - prev_y) / (catch_y - prev_y))

    # определяем точку, в которой должна оказаться камера
    cam_new_x = cam_x + (catch_x - cam_x) * x_coeff
    cam_new_y = cam_y + (catch_y - cam_y) * y_coeff

    return (cam_new_x, cam_new_y)

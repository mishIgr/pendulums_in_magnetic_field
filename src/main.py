import numpy as np
from params import Params
from vector import Vector
import butcher_tables as tb
from runge_kutta import runge_kutta_n_steps
import visual as vsl


def pendulum_derivatives(state, system_params):
    """
    Вычисляет производные состояния маятника с учетом магнитного взаимодействия
    """
    # Распаковываем текущее состояние
    theta = (state.theta + np.pi) % (2*np.pi) - np.pi  # Нормализуем в [-pi, pi]
    w = state.w

    # Распаковываем параметры системы
    m = system_params.m
    b = system_params.b
    l = system_params.l
    g = system_params.g
    magnets = system_params.magnets

    # Координаты груза маятника
    x = l * np.sin(theta)
    y = -l * np.cos(theta)  # ось y направлена вниз

    # Вычисляем суммарный магнитный момент
    F_magn = 0.0
    for magnet in magnets:
        xi, yi, ki = magnet.x, magnet.y, magnet.k
        dx = xi - x
        dy = yi - y
        r = np.sqrt(dx**2 + dy**2)

        n = np.array([-y, x]) / l

        F = ki * np.array([dx, dy]) / (r**3)
        F_magn += np.dot(n, F)

    # Уравнения движения
    dw = (-g/l * np.sin(theta)    # Гравитация
          - b * w                 # Трение
          + F_magn)               # Магнитное взаимодействие

    return Vector({
        'dtheta': w,
        'dw': dw
    })


# Параметры системы
params = Params({
    'm': 1.0,      # Масса маятника
    'b': 0.5,      # Коэффициент трения
    'g': 9.81,     # Ускорение свободного падения
    'l': 5.0,      # Длина маятника
    'magnets': [   # Характеристики магнитов x, y координаты, k сила магнита
        {'x': -5, 'y': -4, 'k': -20},
        {'x': -4, 'y': -5, 'k': -50},
    ]
})

initial_state = Vector({
    'theta': -1.5,
    'w': 0.6,
})

# Параметры интегрирования
table = tb.dopri5_table  # таблица Бучеры для РК
h = 0.01  # размер шага
steps = 2000  # количество шагов

# Интегрирование
history = runge_kutta_n_steps(
    table, pendulum_derivatives, initial_state, params, h, steps
)

# Визуализация (функцию create_animation нужно будет реализовать позже)
vsl.create_animation(history, h, params)

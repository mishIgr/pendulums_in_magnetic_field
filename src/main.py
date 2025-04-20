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
    mu = system_params.mu
    magnets = system_params.magnets

    # Координаты груза маятника
    x = l * np.sin(theta)
    y = -l * np.cos(theta)  # ось y направлена вниз

    # Вычисляем суммарный магнитный момент
    tau_magn = 0.0
    for magnet in magnets:
        xi, yi, ki = magnet.x, magnet.y, magnet.k
        dx = x - xi
        dy = y - yi
        r_sq = dx**2 + dy**2

        # Модель магнитного взаимодействия (потенциал ~1/r^2)
        # Сила притяжения/отталкивания пропорциональна ki
        # Момент силы = F * плечо = F * l * sin(angle_between)
        F_magn = ki * mu / r_sq
        angle = np.arctan2(dy, dx)
        tau_magn += F_magn * l * np.sin(abs(theta - angle))

    # Уравнения движения
    dtheta = w
    dw = (-g/l * np.sin(theta)        # Гравитация
          - b * w                     # Трение
          + tau_magn / (m * l**2))    # Магнитное взаимодействие

    return Vector({
        'dtheta': dtheta,
        'dw': dw
    })


# Параметры системы
params = Params({
    'm': 1.0,      # Масса маятника
    'b': 0.6,      # Коэффициент трения
    'g': 9.81,     # Ускорение свободного падения
    'l': 5.0,      # Длина маятника
    'mu': 1,       # Магнитная постоянная
    'magnets': [   # Характеристики магнитов x, y координаты, k сила магнита
        {'x': -5, 'y': -4, 'k': -1000},
        {'x': -4, 'y': -5, 'k': 1000},
    ]
})

initial_state = Vector({
    'theta': 5,
    'w': 1,
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

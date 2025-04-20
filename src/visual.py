import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np


def create_animation(history, h, params):
    magnet_coords = [(magnet.x, magnet.y) for magnet in params.magnets]
    if magnet_coords:
        x_magnets, y_magnets = zip(*magnet_coords)
        x_min = min(-params.l, min(x_magnets)) * 1.2
        x_max = max(params.l, max(x_magnets)) * 1.2
        y_min = min(-params.l, min(y_magnets)) * 1.2
        y_max = max(params.l, max(y_magnets)) * 1.2
    else:
        x_min, x_max = -params.l*1.2, params.l*1.2
        y_min, y_max = -params.l*1.2, params.l*1.2

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title('Маятник с магнитным взаимодействием')

    # Точка подвеса (0,0)
    pivot = plt.Circle((0, 0), 0.05, fc='k')

    # Нить и груз маятника
    line, = ax.plot([], [], 'b-', lw=2, alpha=0.2)
    bob = Circle((0, 0), 0.1, fc='black')

    # Текст для отображения времени
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    w_text = ax.text(0.02, 0.9, '', transform=ax.transAxes, fontsize=12)

    # Магниты (разные цвета для разных полярностей)
    magnets_patches = []
    for magnet in params.magnets:
        color = 'red' if magnet.k < 0 else 'blue'
        mag = Circle((magnet.x, magnet.y), 0.15, fc=color, alpha=0.7)

        # Добавляем подпись с силой магнита
        ax.text(magnet.x, magnet.y + 0.2, f'k={magnet.k}',
                ha='center', va='center', fontsize=8)

        ax.add_patch(mag)
        magnets_patches.append(mag)

    # Добавляем легенду (исправлена опечатка в 'handles')
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Отталкивающий (k < 0)',
               markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Притягивающий (k > 0)',
               markerfacecolor='blue', markersize=10),
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.add_patch(pivot)
    ax.add_patch(bob)

    current_time = 0

    def init():
        line.set_data([], [])
        time_text.set_text('')
        w_text.set_text('')
        return line, bob, time_text, w_text, *magnets_patches

    def update(frame):
        nonlocal current_time
        # Получаем текущий угол
        theta = history[frame].theta
        w = abs(history[frame].w)

        # Координаты груза
        x = params.l * np.sin(theta)
        y = -params.l * np.cos(theta)

        # Обновляем нить
        line.set_data([0, x], [0, y])

        # Обновляем положение груза
        bob.center = (x, y)

        # Обновляем время
        current_time += h
        time_text.set_text(f'Время: {current_time:.2f} с')
        w_text.set_text(f'Угловая скорость: {w:.2f}')

        return line, bob, time_text, w_text, *magnets_patches

    ani = FuncAnimation(fig, update, frames=len(history),
                        init_func=init, blit=True, interval=h*1000)

    plt.show()

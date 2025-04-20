import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np


def create_animation(history, h, params):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-params.l*1.2, params.l*1.2)
    ax.set_ylim(-params.l*1.2, params.l*1.2)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title('Маятник с магнитным взаимодействием')

    # Точка подвеса (0,0)
    pivot = plt.Circle((0, 0), 0.05, fc='k')

    # Нить и груз маятника
    line, = ax.plot([], [], 'b-', lw=2)
    bob = Circle((0, 0), 0.1, fc='r')

    # Магниты (отображаем их положение)
    magnets_patches = []
    for magnet in params.magnets:
        mag = Circle((magnet.x, magnet.y), 0.15, fc='blue', alpha=0.5)
        ax.add_patch(mag)
        magnets_patches.append(mag)

    ax.add_patch(pivot)
    ax.add_patch(bob)

    def init():
        line.set_data([], [])
        return line, bob, *magnets_patches

    def update(frame):
        # Получаем текущий угол
        theta = history[frame].theta

        # Координаты груза
        x = params.l * np.sin(theta)
        y = -params.l * np.cos(theta)  # ось Y вниз

        # Обновляем нить
        line.set_data([0, x], [0, y])

        # Обновляем положение груза
        bob.center = (x, y)

        return line, bob, *magnets_patches

    ani = FuncAnimation(fig, update, frames=len(history),
                        init_func=init, blit=True, interval=h*1000)

    plt.show()

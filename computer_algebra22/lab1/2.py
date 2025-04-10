# %%

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Generator
from itertools import product
from copy import deepcopy
import matplotlib.animation as animation

# %%

def simulate(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
) -> Generator[dict, ...]:
    yield {
        "x": xa,
        "y": y(xa),
        "v": np.zeros(2),
        "a": np.zeros(2),
        "t": 0,
    }
    t = 0
    # if xa == xb:
    #     x_values = np.linspace(xa, xa + n * 1e-3, n)
    # else:
    x_values = np.linspace(xa, xb, n)
    v_previous = np.zeros(2)
    for i in range(n - 1):
        x1 = x_values[i]
        x2 = x_values[i + 1]
        y1 = y(x1)
        y2 = y(x2)
        # if y2 > y1:
        #     yield {
        #         "x": x2,
        #         "y": y2,
        #         "v": 0,
        #         "a": 0,
        #         "t": -1,
        #     }
        #     return
        s = np.array([x2 - x1, y2 - y1])
        s_norm = np.sqrt(np.dot(s, s))
        v_norm = np.dot(v_previous, s) / s_norm
        sin = (y1 - y2) / s_norm
        if abs(sin) < 1e-6:
            if v_norm == 0:
                # return infinity
                yield {
                    "x": x2,
                    "y": y2,
                    "v": 0,
                    "a": 0,
                    "t": -1,
                }
                return
            dt = s_norm / v_norm
        else:
            dt = (-v_norm + np.sqrt(v_norm**2 + 2 * s_norm * g * sin)) / (g * sin)

        t += dt
        v = s / s_norm * (v_norm + g * sin * dt)
        a = (v - v_previous) / dt
        # print(s_norm)
        #
        # print(
        #     {
        #         "x": x2,
        #         "y": y2,
        #         "v": v_previous,
        #         "a": a,
        #         "t": t,
        #     }
        # )
        v_previous = v
        yield {
            "x": x2,
            "y": y2,
            "v": v_previous,
            "a": a,
            "t": t,
        }

# %%

def eval_time(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
) -> float:
    for i in simulate(xa, xb, y, g, n):
        # print(i["t"])
        t = i["t"]
    return t

# %%

def visualize(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
    t: float,
    width: int = 1,
) -> None:
    x_values = []
    y_values = []
    acceleration = None
    checked = False
    for s in simulate(xa, xb, y, g, n):
        x_values.append(s["x"])
        y_values.append(s["y"])
        if s["t"] > t and not checked:
            x0 = x_values[-1]
            y0 = y_values[-1]
            v = s["v"]
            acceleration = s["a"]
            checked = True
    if not checked:
        print("choose smaller time")
        return
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.plot(x_values, y_values)
    ax.plot(x0, y0, "ro", label="Частинка в момент часу t")

    # Вектори швидкості, прискорення, сили
    v = ax.quiver(
        x0,
        y0,
        v[0],
        v[1],
        angles="xy",
        scale_units="xy",
        scale=width,
        color="blue",
    )
    a = ax.quiver(
        x0,
        y0,
        acceleration[0],
        acceleration[1],
        angles="xy",
        scale_units="xy",
        scale=width,
        color="green",
    )
    n = ax.quiver(
        x0,
        y0,
        acceleration[0],
        acceleration[1] + g,
        angles="xy",
        scale_units="xy",
        scale=width,
        color="red",
    )
    mg = ax.quiver(
        x0,
        y0,
        0,
        -g,
        angles="xy",
        scale_units="xy",
        scale=width,
        color="yellow",
    )
    ax.quiverkey(v, X=0.8, Y=0.9, U=1, label="Швидкість", labelpos="E")
    ax.quiverkey(a, X=0.8, Y=0.85, U=1, label="Прискорення", labelpos="E")
    ax.quiverkey(n, X=0.8, Y=0.8, U=1, label="Реакція опори", labelpos="E")
    ax.quiverkey(mg, X=0.8, Y=0.75, U=1, label="Силя тяжіння", labelpos="E")
    plt.show()

# %%

# доказ того, що функція працює (падіння вниз)
eval_time(0, 0.001, lambda x: 10 - 10000 * x, 9.8, 100)
# eval_time((10, 10), (0, 0), lambda x: x, 9.8, 100)

eval_time(-1, 1, lambda x: np.exp(-x), 9.8, 100)

# %%

# visualize(0, 0.001, lambda x: 10 - 10000 * x, 9.8, 100, 0.001)
visualize(-1, 1, lambda x: np.exp(-x), 9.8, 100, 0.4, width=10)

# %%

# visualize(xa, xb, y, 9.8, n, t / 2, 10)

# %%

# def animate_movement(xa: float, xb: float, y: Callable[[int], int]):
#     ...
# %%

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Generator
from itertools import product
from copy import deepcopy

# %%

def simulate(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
) -> Generator[dict, ...]:
    yield {
        "x": xa,
        "y": y(xa),
        "v": np.zeros(2),
        "a": np.zeros(2),
        "t": 0,
    }
    t = 0
    # if xa == xb:
    #     x_values = np.linspace(xa, xa + n * 1e-3, n)
    # else:
    x_values = np.linspace(xa, xb, n)
    v_previous = np.zeros(2)
    for i in range(n - 1):
        x1 = x_values[i]
        x2 = x_values[i + 1]
        y1 = y(x1)
        y2 = y(x2)
        # if y2 > y1:
        #     yield {
        #         "x": x2,
        #         "y": y2,
        #         "v": 0,
        #         "a": 0,
        #         "t": -1,
        #     }
        #     return
        s = np.array([x2 - x1, y2 - y1])
        s_norm = np.sqrt(np.dot(s, s))
        v_norm = np.dot(v_previous, s) / s_norm
        sin = (y1 - y2) / s_norm
        if abs(sin) < 1e-6:
            if v_norm == 0:
                # return infinity
                yield {
                    "x": x2,
                    "y": y2,
                    "v": 0,
                    "a": 0,
                    "t": -1,
                }
                return
            dt = s_norm / v_norm
        else:
            dt = (-v_norm + np.sqrt(v_norm**2 + 2 * s_norm * g * sin)) / (g * sin)

        t += dt
        v = s / s_norm * (v_norm + g * sin * dt)
        a = (v - v_previous) / dt
        # print(s_norm)
        #
        # print(
        #     {
        #         "x": x2,
        #         "y": y2,
        #         "v": v_previous,
        #         "a": a,
        #         "t": t,
        #     }
        # )
        v_previous = v
        yield {
            "x": x2,
            "y": y2,
            "v": v_previous,
            "a": a,
            "t": t,
        }

# %%

def eval_time(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
) -> float:
    for i in simulate(xa, xb, y, g, n):
        # print(i["t"])
        t = i["t"]
    return t

# %%

def visualize(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: int,
    n: int,
    t: float,
    width: int = 1,
) -> None:
    x_values = []
    y_values = []
    acceleration = None
    checked = False
    for s in simulate(xa, xb, y, g, n):
        x_values.append(s["x"])
        y_values.append(s["y"])
        if s["t"] > t and not checked:
            x0 = x_values[-1]
            y0 = y_values[-1]
            v = s["v"]
            acceleration = s["a"]
            checked = True
    if not checked:
        print("choose smaller time")
        return
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.plot(x_values, y_values)
    ax.plot(x0, y0, "ro", label="Частинка в момент часу t")

    # Вектори швидкості, прискорення, сили
    v = ax.quiver(
        x0,
        y0,
        v[0],
        v[1],
        angles="xy",
        scale_units="xy",
        scale=width,
        color="blue",
    )
    a = ax.quiver(
        x0,
        y0,
        acceleration[0],
        acceleration[1],
        angles="xy",
        scale_units="xy",
        scale=width,
        color="green",
    )
    n = ax.quiver(
        x0,
        y0,
        acceleration[0],
        acceleration[1] + g,
        angles="xy",
        scale_units="xy",
        scale=width,
        color="red",
    )
    mg = ax.quiver(
        x0,
        y0,
        0,
        -g,
        angles="xy",
        scale_units="xy",
        scale=width,
        color="yellow",
    )
    ax.quiverkey(v, X=0.8, Y=0.9, U=1, label="Швидкість", labelpos="E")
    ax.quiverkey(a, X=0.8, Y=0.85, U=1, label="Прискорення", labelpos="E")
    ax.quiverkey(n, X=0.8, Y=0.8, U=1, label="Реакція опори", labelpos="E")
    ax.quiverkey(mg, X=0.8, Y=0.75, U=1, label="Силя тяжіння", labelpos="E")
    plt.show()

# %%

# доказ того, що функція працює (падіння вниз)
eval_time(0, 0.001, lambda x: 10 - 10000 * x, 9.8, 100)
# eval_time((10, 10), (0, 0), lambda x: x, 9.8, 100)

eval_time(-1, 1, lambda x: np.exp(-x), 9.8, 100)

def find_optimal_function(
    xa: float,
    xb: float,
    ya: float,
    yb: float,
    g: float,
    n: int,
) -> Callable[[float], float]:
    # optimal_values = [[ya] for _ in range(n)]
    options = np.linspace(yb, ya, n)
    # options = product(options, repeat=n)

    from itertools import combinations

    def decreasing_cartesian_product(vec, n):
        vec = sorted(vec, reverse=True)  # Сортуємо в порядку спадання
        return list(combinations(vec, n))  # Генеруємо всі допустимі комбінації
    options = decreasing_cartesian_product(list(options) * 2, n)
    print(options)
    # print(list(options))

    t = -1
    optimal_trajectory = None
    for trajectory in options:
        if trajectory[0] != ya or trajectory[-1] != yb:
            continue
        time = eval_time(
            xa, xb, lambda x: trajectory[int((x - xa) * (n - 1) / (xb - xa))], g, n
        )
        print(time)
        if 0 < time < t or t == -1:
            t = time
            print(f"{t}")
            optimal_trajectory = trajectory
    return lambda x: deepcopy(optimal_trajectory)[int((x - xa) * (n - 1) / (xb - xa))]

# %%

xa = 0
xb = 10
ya = 2 * np.exp(1)
yb = 0
g = 9.8
n = 12

# %%

y = find_optimal_function(xa, xb, ya, yb, g, n)

# %%

t = eval_time(xa, xb, y, g, n)
print(t)

# %%

# visualize(xa, xb, y, 9.8, n, t / 2, 10)

# %%

# def animate_movement(xa: float, xb: float, y: Callable[[int], int]):
#     ...

def animate_movement(
    xa: float,
    xb: float,
    y: Callable[[float], float],
    g: float,
    n: int,
    width: int = 1,
    interval: int = 50,  # Інтервал кадрів у мілісекундах
) -> None:
    time_data = list(simulate(xa, xb, y, g, n))  # Отримуємо всі дані руху

    # Створюємо графік
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    # Генеруємо траєкторію
    x_values = [s["x"] for s in time_data]
    y_values = [s["y"] for s in time_data]
    ax.plot(x_values, y_values, label="Траєкторія")

    # Межі графіка
    ax.set_xlim(min(x_values) - 1, max(x_values) + 1)
    ax.set_ylim(min(y_values) - 1, max(y_values) + 1)

    # Частинка, що рухається
    (particle,) = ax.plot([], [], "ro", markersize=8, label="Частинка")

    def update(frame):
        if frame >= len(time_data):
            return (particle,)
        particle.set_data([time_data[frame]["x"]], [time_data[frame]["y"]])
        return (particle,)
    ani = animation.FuncAnimation(
        fig, update, frames=len(time_data), interval=interval, blit=True
    )

    plt.legend()
    plt.show()

animate_movement(xa, xb, y, g, n)

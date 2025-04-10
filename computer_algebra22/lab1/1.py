# %%

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# %%

# counterclockwise rotation
W = 5
Q = lambda a: np.array(
    [
        [np.cos(a), -np.sin(a)],
        [np.sin(a), np.cos(a)],
    ]
)
Q1 = lambda a: np.array(
    [
        [-np.sin(a), -np.cos(a)],
        [np.cos(a), -np.sin(a)],
    ]
)
Q2 = lambda a: np.array(
    [
        [-np.cos(a), np.sin(a)],
        [-np.sin(a), -np.cos(a)],
    ]
)

# %%

G = np.array([0, -9.8])
U = np.array([3, 10])  # initial bomb speed
X0 = np.array([3, 4])  #  initial coordinates of bomb
R = np.array([0, 10])
XR = np.array([2, 1])  # center of rotation

# %%

# normal coordinates, velocity and acceleration
x1 = lambda t: X0 + U * t + G * t**2 / 2
v1 = lambda t: U + G * t
a1 = G
# observers' coordinates, velocity and acceleration
x = lambda t: x1(t) - XR - np.dot(Q(W * t), R)
v = lambda t: v1(t) - W * np.dot(Q1(W * t), R)
a = lambda t: a1 - W**2 * np.dot(Q2(W * t), R)

# %%

t_values = np.linspace(0, 2, 100)
coords = [x1(t) for t in t_values]
normal_trajectory = ([i[0] for i in coords], [i[1] for i in coords])
# plt.show()

# %% plot trajectory

t_values = np.linspace(0, 2, 100)
coords = [x(t) for t in t_values]
trajectory_plot = ([i[0] for i in coords], [i[1] for i in coords])
# plt.show()

# %% x of t

t_values = np.linspace(0, 10, 100)
coords = [x(t) for t in t_values]
x_plot = (t_values, [i[0] for i in coords])
# plt.show()

# %% y of t

t_values = np.linspace(0, 10, 100)
coords = [x(t) for t in t_values]
y_plot = (t_values, [i[1] for i in coords])
# plt.show()

# %% Vx of t

t_values = np.linspace(0, 10, 1000)
coords = [v(t) for t in t_values]
vx_plot = (t_values, [i[0] for i in coords])
# plt.show()

# %% Vy of t

t_values = np.linspace(0, 10, 1000)
coords = [v(t) for t in t_values]
vy_plot = (t_values, [i[1] for i in coords])
# plt.show()

# %% Ax of t

t_values = np.linspace(0, 10, 1000)
coords = [a(t) for t in t_values]
ax_plot = (t_values, [i[0] for i in coords])
# plt.show()

# %% Ay of t

t_values = np.linspace(0, 10, 1000)
coords = [a(t) for t in t_values]
ay_plot = (t_values, [i[1] for i in coords])
# plt.show()

# %% final plot

fig, axs = plt.subplots(3, 1, figsize=(10, 12))

axs[0].plot(*trajectory_plot)
axs[0].set_title("Траєкторія снаряду")
axs[0].set_xlabel("x (м)")
axs[0].set_ylabel("y (м)")

# Графіки координат та похідних
axs[1].plot(*x_plot, label="$x(t)$")
axs[1].plot(*vx_plot, label="$v_x(t)$")
axs[1].plot(*ax_plot, label="$a_x(t)$")
axs[1].set_title("Залежності координат, швидкості та прискорення по x")
axs[1].set_xlabel("Час (с)")
axs[1].set_ylabel("Значення")
axs[1].legend()

axs[2].plot(*y_plot, label="$y(t)$")
axs[2].plot(*vy_plot, label="$v_y(t)$")
axs[2].plot(*ay_plot, label="$a_y(t)$")
axs[2].set_title("Залежності координат, швидкості та прискорення по y")
axs[2].set_xlabel("Час (с)")
axs[2].set_ylabel("Значення")
axs[2].legend()

plt.tight_layout()
plt.show()

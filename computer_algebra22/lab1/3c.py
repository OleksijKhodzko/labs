import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ProjectileMotion:
    def __init__(self, g, k):
        self.g = g  # Прискорення вільного падіння
        self.k = k  # Коефіцієнт опору повітря

    def equations(self, t, state):
        x, y, z, vx, vy, vz = state
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        ax = -self.k * v * vx
        ay = -self.k * v * vy
        az = -self.g - self.k * v * vz
        return [vx, vy, vz, ax, ay, az]

    def simulate(self, v0, theta, phi, x0=0, y0=0, z0=0, dt=0.01):
        vx0 = v0 * np.cos(theta) * np.cos(phi)
        vy0 = v0 * np.cos(theta) * np.sin(phi)
        vz0 = v0 * np.sin(theta)

        state0 = [x0, y0, z0, vx0, vy0, vz0]
        t_span = (0, 100)
        sol = spi.solve_ivp(
            self.equations,
            t_span,
            state0,
            method="RK45",
            max_step=dt,
            events=self.hit_ground,
        )
        return sol.t, sol.y

    def hit_ground(self, t, state):
        return state[2]
    hit_ground.terminal = True
    hit_ground.direction = -1

    def find_initial_conditions(self, x0, y0, z0, xf, yf, dt=0.01):
        def error(v0_guess):
            _, traj = self.simulate(v0_guess, np.pi / 4, np.pi / 4, x0, y0, z0, dt)
            return (traj[0, -1] - xf) ** 2 + (traj[1, -1] - yf) ** 2
        from scipy.optimize import minimize

        res = minimize(error, x0=[10], bounds=[(0, 1000)])
        return res.x[0]

    def plot_trajectory(self, t, traj):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(traj[0], traj[1], traj[2], label="Trajectory")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.legend()
        plt.show()

# Приклад використання:
g = 9.81  # Прискорення вільного падіння
k = 0.1  # Коефіцієнт опору повітря
pm = ProjectileMotion(g, k)

t, traj = pm.simulate(v0=50, theta=np.pi / 4, phi=np.pi / 4, z0=100)
pm.plot_trajectory(t, traj)

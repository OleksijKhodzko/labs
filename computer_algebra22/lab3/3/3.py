# Оптимізована симуляція газу твердих сфер

import numpy as np
import matplotlib.pyplot as plt
from random import random
from copy import deepcopy

# Константи
k = 1.38e-23
S = np.pi * 1e-24
H = 1e-12
N = 1000
R = 2.86e-15
M = 9.1e-31
T = 273
G = 9.8

D = 2 * np.sqrt(S / np.pi)  # Діаметр основи циліндра

def random_k():
    while True:
        k = np.array([random() - 0.5 for _ in range(3)])
        norm = np.linalg.norm(k)
        if norm > 1e-10:
            return k / norm

def K(v):
    return M * v ** 2 / 2

def v(K):
    return np.sqrt(2 * K / M)

def update_velocity_on_obstacle(p, v):
    return v - 2 * (p @ v) * p

def update_velocities(p1, p2, v1, v2):
    p = (p1 - p2) / np.linalg.norm(p1 - p2)
    d1 = v1 - p * (p @ v1)
    d2 = v2 - p * (p @ v2)
    v1new = d1 + p * ((v1 + v2) @ p) / 2
    v2new = d2 - p * ((v1 + v2) @ p) / 2
    return v1new, v2new

def initialize_non_overlapping_positions(N, R, D, H, max_attempts=10000):
    positions = []
    attempts = 0
    while len(positions) < N and attempts < max_attempts:
        attempts += 1
        candidate = np.array([
            (random() - 0.5) * (D - 2 * R),
            (random() - 0.5) * (D - 2 * R),
            (random() - 0.5) * (H - 2 * R)
        ])
        if all(np.linalg.norm(candidate - p) > 2 * R for p in positions):
            positions.append(candidate)
    if len(positions) < N:
        raise RuntimeError(f"Не вдалося ініціалізувати всі {N} частинки без перетинів.")
    return np.array(positions)

def new_positions(positions, velocities, dt):
    return positions + velocities * dt

def detect_collisions(positions):
    cell_size = 2 * R
    cell_map = {}
    collisions = np.zeros((N, N))

    def cell_key(pos):
        return tuple((pos // cell_size).astype(int))

    for i, pos in enumerate(positions):
        key = cell_key(pos)
        cell_map.setdefault(key, []).append(i)

    for key, indices in cell_map.items():
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    neighbor_key = (key[0]+dx, key[1]+dy, key[2]+dz)
                    if neighbor_key in cell_map:
                        for i in indices:
                            for j in cell_map[neighbor_key]:
                                if i < j and np.linalg.norm(positions[i] - positions[j]) <= 2 * R:
                                    collisions[i][j] = 1
                                    collisions[j][i] = 1
    return collisions


def process_obstacles(positions, velocities):
    new_velocities = velocities.copy()
    for i, pos in enumerate(positions):
        # Бічні стінки
        if np.linalg.norm(pos[:2]) >= D / 2 - R:
            p = np.append(-pos[:2], 0)
            p /= np.linalg.norm(p)
            new_velocities[i] = update_velocity_on_obstacle(p, new_velocities[i])
        # Кришки
        if abs(pos[2]) >= H / 2 - R:
            p = np.array([0, 0, -pos[2]])
            p /= np.linalg.norm(p)
            new_velocities[i] = update_velocity_on_obstacle(p, new_velocities[i])
    return new_velocities


def new_velocities(positions, collisions_matrix, velocities):
    new_velocities = velocities.copy()
    for i in range(N):
        for j in range(i + 1, N):
            if collisions_matrix[i][j]:
                new = update_velocities(
                    positions[i], positions[j], new_velocities[i], new_velocities[j]
                )
                new_velocities[i], new_velocities[j] = new
    return process_obstacles(positions, new_velocities)

# Ініціалізація
positions = {0: initialize_non_overlapping_positions(N, R, D, H)}
total_energy = 3 * N * k * T / 2
energies = np.array([random() for _ in range(N)])
energies = energies / energies.sum() * total_energy
velocities = {0: np.array([random_k() * v(K) for K in energies])}

# Симуляція
simulation_time = 1e-13
t = 0

while t < simulation_time:
    current_positions = positions[t]
    current_velocities = velocities[t]
    dt = R / 4 / max(np.linalg.norm(v) for v in current_velocities)

    updated_positions = new_positions(current_positions, current_velocities, dt)
    collisions_matrix = detect_collisions(updated_positions)
    updated_velocities = new_velocities(updated_positions, collisions_matrix, current_velocities)

    t += dt
    positions[t] = updated_positions
    velocities[t] = updated_velocities

# Візуалізація
final_velocities = list(velocities.values())[-1]
speeds = [np.linalg.norm(v) for v in final_velocities]

plt.hist(speeds, bins=30, density=True, alpha=0.7, color='orange', edgecolor='black')
plt.title('Розподіл швидкостей частинок після симуляції')
plt.xlabel('Швидкість (м/с)')
plt.ylabel('Ймовірність')
plt.grid(True)
plt.show()
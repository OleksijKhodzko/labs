# %%

import matplotlib.pyplot as plt
from numpy import sin, cos, array, pi, dot, sqrt, exp, linspace, cross

# %%

G = 100
M = 1
K = 1e-3
PHI = pi / 4
THETA = 0
W = -0.001
R = 1000
H = 500
v0ii = array([0.2, 0, 0.5])

# %%

r0 = (R + H) * array(
    [
        sin(PHI) * cos(THETA),
        sin(PHI) * sin(THETA),
        cos(PHI),
    ]
)
Axii_xi = array(
    [
        [sin(PHI), 0, cos(PHI)],
        [0, 1, 0],
        [-cos(PHI), 0, sin(PHI)],
    ]
)
Axi_xii = Axii_xi.T

def Axi_x(t: float) -> array:
    return array(
        [
            [cos(THETA + W * t), -sin(THETA + W * t), 0],
            [sin(THETA + W * t), cos(THETA + W * t), 0],
            [0, 0, 1],
        ]
    )

def Ax_xi(t: float) -> array:
    return Axi_x(t).T

# %%

def B(vii: array, t: float) -> array:
    return dot(Axi_x(t), dot(Axii_xi, vii) + R * array([sin(PHI), 0, cos(PHI)]))

def F(v: array, t: float) -> array:
    return dot(Axi_xii, dot(Ax_xi(t), v) - R * array([sin(PHI), 0, cos(PHI)]))

# %%

v0 = cross(array([0, 0, W]), r0) + B(v0ii, 0)
n = r0 / sqrt(dot(r0, r0))

# %%

def ri(t: float) -> array:
    return (
        v0 * t
        - cross(array([0, 0, W]), v0) * t**2
        - G * t**3 / 6 / M * n
        - K / 2 / M * v0 * t**2
        + Ax_xi(0) @ r0
    )

# %%

def rii(t: float) -> array:
    # return F(r(t), t)
    return Axi_xii @ (
        ri(t)
        - R
        * array(
            [
                sin(PHI),
                0,
                cos(PHI),
            ]
        )
    )

# %%

def plot_trajectory(traj):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(
        traj[0],
        traj[1],
        traj[2],
        label="Trajectory",
    )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

# def plot_trajectory(traj):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#
#     # Plot the trajectory line
#     ax.plot(traj[0], traj[1], traj[2], label="Trajectory")
#
#     # Add arrows along the trajectory
#     for i in range(0, len(traj[0]) - 1, 100):  # Add arrows every 10 points
#         ax.quiver(
#             traj[0][i],
#             traj[1][i],
#             traj[2][i],
#             traj[0][i + 1] - traj[0][i],
#             traj[1][i + 1] - traj[1][i],
#             traj[2][i + 1] - traj[2][i],
#             color="r",
#             length=200,
#         )  # You can adjust `length` to scale the arrows
#
#     ax.set_xlabel("X")
#     ax.set_ylabel("Y")
#     ax.set_zlabel("Z")
#     ax.legend()
#     plt.show(block=False)

# %%

T = 100

# %%

traj = list(zip(*(rii(t) for t in linspace(0, T, T * 100))))
for i, z in enumerate(traj[2]):
    if z < -1:
        traj = [k[:i] for k in traj]
        break
plot_trajectory(traj)

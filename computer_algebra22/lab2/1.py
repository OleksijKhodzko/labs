from numpy import array, sin, cos, sqrt, pi, eye, cross
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt


def rodrigues_rotation_matrix(axis: array, theta: float) -> array:
    axis = axis / sqrt(axis @ axis)
    K = array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return eye(3) + sin(theta) * K + (1 - cos(theta)) * K @ K


def find_center(
    edges: list[(array, array, float), ...],
) -> array:
    m = sum(edge[2] for edge in edges)
    return sum((edge[0] + edge[1]) * edge[2] / 2 for edge in edges) / m


def rotate(
    edges: list[(array, array, float), ...],
    axis: ArrayLike,
    theta: float,
) -> list[(array, array, float), ...]:
    axis = array(axis)
    rotationMatrix = rodrigues_rotation_matrix(axis, theta)
    return [
        (rotationMatrix @ edge[0], rotationMatrix @ edge[1], edge[2]) for edge in edges
    ]


def move(
    edges: list[(array, array, float), ...],
    vec: array,
) -> list[(array, array, float), ...]:
    return [(edge[0] - vec, edge[1] - vec, edge[2]) for edge in edges]


def find_angle(v1: array, v2: array) -> float:
    return v1 @ v2 / sqrt(v1 @ v1) / sqrt(v2 @ v2)


def hang(
    edges: list[array, array, float],
    vertice_index: int,
) -> list[(array, array, float), ...]:
    vertice = edges[vertice_index][0]
    edges = move(edges, vertice)
    # return edges
    return rotate(
        edges,
        cross([0, 0, 1], find_center(edges)),
        find_angle(array([0, 0, 1]), find_center(edges)),
    )


def visualize(
    edges: list[(array, array, float), ...],
) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # Set axis labels
    ax.plot([-4, 4], [0, 0], [0, 0])
    ax.plot([0, 0], [-4, 4], [0, 0])
    ax.plot([0, 0], [0, 0], [-4, 4])
    ax.plot([-3, 3], [3, -3], [0, 0])
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    # Plot the vertices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color="red", s=50)

    ax.scatter(*find_center(edges), color="blue", s=10)
    # Plot the edges using your approach
    for edge in edges:
        start_point, end_point, _ = edge
        ax.plot(
            [start_point[0], end_point[0]],
            [start_point[1], end_point[1]],
            [start_point[2], end_point[2]],
            color="black",
            linestyle="-",
        )
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    vertices = array(
        [
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
        ]
    )
    edges = [
        (vertices[0], vertices[1], 1),
        (vertices[1], vertices[2], 1),
        (vertices[2], vertices[3], 1),
        (vertices[3], vertices[0], 1),
        (vertices[4], vertices[5], 1),
        (vertices[5], vertices[6], 1),
        (vertices[6], vertices[7], 1),
        (vertices[7], vertices[4], 1),
        (vertices[0], vertices[4], 1),
        (vertices[1], vertices[5], 1),
        (vertices[2], vertices[6], 1),
        (vertices[3], vertices[7], 1),
    ]
    # visualize(edges)
    visualize(move(edges, [1, 1, 1]))
    visualize(rotate(edges, [0, 0, 1], pi / 6))
    visualize(hang(edges, 1))

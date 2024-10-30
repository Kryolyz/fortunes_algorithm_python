import math
import matplotlib.pyplot as plt
import numpy as np


def plot_paraboles(paraboles, y_sweep):
    fig, ax = plt.subplots()
    x = np.linspace(-5, 8, 400)
    intersections = []
    for parabole in paraboles:
        y = (x - parabole[0]) ** 2 / (2 * (parabole[1] - y_sweep)) + (
            parabole[1] + y_sweep
        ) / 2
        ax.plot(x, y)
    for i, parabole1 in enumerate(paraboles):
        for j, parabole2 in enumerate(paraboles):
            if i != j:
                if parabole1[1] == y_sweep or parabole2[1] == y_sweep:
                    continue  # Handle edge case when site is on the sweep line
                if parabole1[1] == parabole2[1]:
                    x_int = (parabole1[0] + parabole2[0]) / 2
                    y_int = (
                        parabole1[1] + y_sweep
                    ) / 2  # The y-coordinate is the same for both paraboles
                else:
                    a = 1 / (2 * (parabole1[1] - y_sweep)) - 1 / (
                        2 * (parabole2[1] - y_sweep)
                    )
                    b = 2 * (
                        parabole2[0] / (2 * (parabole2[1] - y_sweep))
                        - parabole1[0] / (2 * (parabole1[1] - y_sweep))
                    )
                    c = (
                        parabole1[0] ** 2 / (2 * (parabole1[1] - y_sweep))
                        - (parabole1[1] + y_sweep) / 2
                    ) - (
                        parabole2[0] ** 2 / (2 * (parabole2[1] - y_sweep))
                        - (parabole2[1] + y_sweep) / 2
                    )
                    discriminant = b**2 - 4 * a * c
                    if discriminant < 0:
                        continue  # No real solutions means no intersection
                    x1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    x2 = (-b - math.sqrt(discriminant)) / (2 * a)
                    x_int = (x1 + x2) / 2
                    y_int = (
                        parabole1[1] + y_sweep
                    ) / 2  # The y-coordinate is the same for both paraboles
                if abs(i - j) == 1:
                    intersections.append((x_int, y_int))
                    ax.plot(x_int, y_int, "ro")
                    print(f"Intersection between {i} and {j}: {x_int:.2f}, {y_int:.2f}")
    ax.set_ylim((0, y_sweep))
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    n = 5
    # paraboles = [[np.random.uniform(-5, 5), np.random.uniform(0, 5)] for _ in range(n)]p
    # site1 = Arc(Site(1, 0))
    # site2 = Arc(Site(2, 1))
    # site3 = Arc(Site(2, 3))
    # site4 = Arc(Site(3, 4))
    paraboles = [[1, 0], [2, 1], [3, 3], [5, 4]]
    # site1 = Arc(Site(1, 0))
    # site2 = Arc(Site(2, 1))
    # site3 = Arc(Site(3, 3))
    # site4 = Arc(Site(5, 4))

    y_sweep = 5
    plot_paraboles(paraboles, y_sweep)

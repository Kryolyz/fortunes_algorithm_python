import math
import matplotlib.pyplot as plt
import numpy as np


def parabole_equation(x, p, sweep_y):
    """
    Returns the y-coordinate of the parabole at the given x-coordinate, site coordinates and sweep line y-coordinate.

    The parabole equation is derived from the definition of a parabole as a set of points equidistant from a given point (the focus) and a given line (the directrix).

    :param x: The x-coordinate
    :param p: The coordinates of the site (x, y)
    :param sweep_y: The y-coordinate of the sweep line
    :return: The y-coordinate of the parabole at the given x-coordinate
    """
    y = (x - p[0]) ** 2 / (2 * (p[1] - sweep_y)) + (p[1] + sweep_y) / 2
    return y


def plot_paraboles(paraboles, y_sweep):
    """
    Plots the paraboles of the given sites at the given sweep line y-coordinate.
    Also calculates the intersection points between consecutive paraboles.

    :param paraboles: The list of paraboles to be plotted, where each parabole is a tuple of (x, y) coordinates
    :param y_sweep: The y-coordinate of the sweep line
    :return: None
    """
    fig, ax = plt.subplots()
    x = np.linspace(-5, 8, 400)
    intersections = []
    for parabole in paraboles:
        y = parabole_equation(x, parabole, y_sweep)
        ax.plot(x, y)
    for i, parabole1 in enumerate(paraboles):
        for j, parabole2 in enumerate(paraboles):
            if i != j and abs(j - i) == 1:
                if parabole1[1] == y_sweep or parabole2[1] == y_sweep:
                    continue  # Handle edge case when site is on the sweep line
                if parabole1[1] == parabole2[1]:
                    x_int = (parabole1[0] + parabole2[0]) / 2
                    y_int = (
                        parabole1[1] + y_sweep
                    ) / 2  # The y-coordinate is the same for both paraboles
                else:
                    xp1 = parabole1[0]
                    yp1 = parabole1[1]
                    xp2 = parabole2[0]
                    yp2 = parabole2[1]

                    p = (-xp1 * yp2 + xp1 * y_sweep + xp2 * yp1 - xp2 * y_sweep) / (
                        yp1 - yp2
                    )
                    q = (
                        (yp1 - y_sweep)
                        * (yp2 - y_sweep)
                        * (
                            xp1**2
                            - 2 * xp1 * xp2
                            + xp2**2
                            + yp1**2
                            - 2 * yp1 * yp2
                            + yp2**2
                        )
                    )
                    q = math.sqrt(q) / (yp1 - yp2)

                    x1 = p + q
                    x2 = p - q
                    print("X1:", x1, "X2:", x2)
                    y_int = parabole_equation(x1, parabole1, y_sweep)

                    intersections.append((x1, y_int))
                    ax.plot(x1, y_int, "ro")
                    print(f"Intersection between {i} and {j}: {x1:.2f}, {y_int:.2f}")
    ax.set_ylim((0, y_sweep))
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    n = 5
    paraboles = [[1, 0], [2, 1], [3, 3], [5, 4]]
    y_sweep = 5
    plot_paraboles(paraboles, y_sweep)

from utils.arc import Arc, Site
from utils.voronoi_diagram import VoronoiDiagram


voronoi_diagram = VoronoiDiagram()
import random

random.seed(0)
sites = [Arc(Site(random.uniform(0, 10), random.uniform(0, 10))) for _ in range(10)]
for site in sites:
    print(site)

voronoi_diagram.add_site_events(sites)
while not voronoi_diagram.event_queue.is_empty():
    voronoi_diagram.process_next_event()

import matplotlib.pyplot as plt

# Extract the original sites, vertices, and half-edges
original_sites = [(site.site.x, site.site.y) for site in sites]
vertices = [(vertex.x, vertex.y) for vertex in voronoi_diagram.beachline.vertices]

edges = [
    (
        edge.origin.x,
        edge.origin.y,
        edge.origin.x + edge.calculate_direction().x / 5,
        edge.origin.y + edge.calculate_direction().y / 5,
    )
    for edge in voronoi_diagram.beachline.edges
]

# Plot the original sites in red
for x, y in original_sites:
    plt.plot(x, y, "ro")  # red dots

# Plot the vertices in blue
for x, y in vertices:
    print(x, y)
    plt.plot(x, y, "bo")  # blue dots

# Plot the half-edges in black
for x1, y1, x2, y2 in edges:
    plt.plot([x1, x2], [y1, y2], "k-")  # black lines

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Voronoi Diagram Visualization")
plt.show()

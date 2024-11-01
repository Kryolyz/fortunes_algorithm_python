from copy import copy
from utils.arc import Arc, Site
from utils.voronoi_diagram import VoronoiDiagram


voronoi_diagram = VoronoiDiagram()
import random

random.seed(0)
sites = [Arc(Site(random.uniform(0, 10), random.uniform(0, 10))) for _ in range(7)]
for site in sites:
    print(site)


def visualize_sites(ax, sites):  # Plot the original sites in red
    for site in sites:
        ax.plot(site.site.x, site.site.y, "ro")  # red dots


def visualize_edges(edges):
    pass


def visualize_vertices(ax, vertices):
    for vertex in vertices:
        ax.plot(vertex.x, vertex.y, "bo")
        edge_directions = vertex.make_edge_directions()
        for site, direction in zip(vertex.origin_sites, edge_directions):
            target_x = vertex.x + direction.x
            target_y = vertex.y + direction.y
            ax.plot([vertex.x, target_x], [vertex.y, target_y], "g-")  # green lines


voronoi_diagram.add_site_events(sites)
beachlines = []
x_values = [i * 0.01 for i in range(int(10 / 0.01) + 1)]
y_resolution = 0.1
y_values = []
while not voronoi_diagram.event_queue.is_empty():
    current_step = {
        "vertices": copy(voronoi_diagram.beachline.vertices),
        "edges": copy(voronoi_diagram.beachline.edges),
        "faces": {k: copy(v) for k, v in voronoi_diagram.beachline.faces.items()},
    }
    voronoi_diagram.process_next_event()
    sorted_events = sorted(
        voronoi_diagram.event_queue.queue, key=lambda event: event.site.y
    )
    next_event_y = sorted_events[0].site.y if sorted_events else None
    current_y = voronoi_diagram.sweep_y
    while next_event_y and current_y < next_event_y:
        y_values.append(
            voronoi_diagram.beachline.get_beachline(current_y + 0.001, x_values)
        )
        current_y += y_resolution

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox

# Global index to track the current step
current_step = 0


# Function to update plot data based on the current step
def update_plot(step):
    """Clear and redraw the plot with the y_values at the specified step."""
    ax.cla()  # Clear the current plot area
    ax.plot(x_values, y_values[step])  # Plot with updated y_values index
    visualize_sites(ax, sites)
    visualize_vertices(ax, voronoi_diagram.beachline.vertices)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Voronoi Diagram Visualization - Step {step + 1}")
    plt.draw()  # Redraw the updated plot


# Slider callback function
def on_slider_change(val):
    """Update the plot based on slider position."""
    global current_step
    current_step = int(val)  # Get the slider's integer value
    update_plot(current_step)


# Text box callback function
def on_text_submit(text):
    """Update the plot based on the entered text value."""
    global current_step
    try:
        index = int(text)
        if 0 <= index < len(y_values):  # Check for valid index
            current_step = index
            update_plot(current_step)
            slider.set_val(current_step)  # Sync slider with text input
        else:
            print(f"Index {index} out of range.")  # Handle out-of-range input
    except ValueError:
        print("Invalid input. Enter an integer.")


# Set up the figure and plot the initial step
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust plot to make space for widgets

# Plot the initial step
update_plot(current_step)

# Add slider for step selection
ax_slider = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor="lightgoldenrodyellow")
slider = Slider(
    ax_slider, "Step", 0, len(y_values) - 1, valinit=current_step, valstep=1
)
slider.on_changed(on_slider_change)  # Bind slider to its function

# Add text box for direct index input
ax_textbox = plt.axes([0.82, 0.1, 0.1, 0.05])
textbox = TextBox(ax_textbox, "Go to Step")
textbox.on_submit(on_text_submit)  # Bind text box to its function

# Show the interactive plot
plt.show()

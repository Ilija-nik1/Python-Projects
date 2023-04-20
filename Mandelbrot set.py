import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Define the size of the image
width, height = 1000, 1000

# Create a mesh grid of complex numbers spanning the region of interest
x_min, x_max = -2, 1
y_min, y_max = -1.5, 1.5
real_axis = np.linspace(x_min, x_max, width)
imag_axis = np.linspace(y_min, y_max, height) * 1j
c = real_axis[:, np.newaxis] + imag_axis[np.newaxis, :]

# Create an array to store the number of iterations for each point in the grid
n_iterations = np.zeros((width, height), dtype=int)

# Set a maximum number of iterations for each point
max_iterations = 100

# Calculate the Mandelbrot set by iterating z = z**2 + c for each point
z = np.zeros_like(c)
for i in range(max_iterations):
    mask = (abs(z) <= 2)
    n_iterations[mask] = i
    z[mask] = z[mask]**2 + c[mask]

# Create a custom colormap to colorize the plot
cmap = colors.ListedColormap(['darkblue', 'blue', 'purple', 'red', 'orange', 'yellow', 'white'])

# Plot the Mandelbrot set using a custom colormap
plt.imshow(n_iterations.T, cmap=cmap, extent=(x_min, x_max, y_min, y_max))

# Add a colorbar to the plot
plt.colorbar()

# Set the x and y axis labels
plt.xlabel('Real')
plt.ylabel('Imaginary')

# Set the limits of the plot
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Add a zoom function to the plot
def onclick(event):
    global x_min, x_max, y_min, y_max
    zoom_factor = 0.5
    x_range = x_max - x_min
    y_range = y_max - y_min
    x_center = x_min + x_range / 2
    y_center = y_min + y_range / 2
    x_new_range = x_range * zoom_factor
    y_new_range = y_range * zoom_factor
    x_min = x_center - x_new_range / 2
    x_max = x_center + x_new_range / 2
    y_min = y_center - y_new_range / 2
    y_max = y_center + y_new_range / 2
    plt.clf()
    plt.imshow(n_iterations.T, cmap=cmap, extent=(x_min, x_max, y_min, y_max))
    plt.colorbar()
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.show()
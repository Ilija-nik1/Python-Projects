import numpy as np
import matplotlib.pyplot as plt

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

# Plot the Mandelbrot set using a grayscale colormap
plt.imshow(n_iterations.T, cmap='gray', extent=(x_min, x_max, y_min, y_max))
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.show()
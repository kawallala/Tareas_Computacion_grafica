import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import sys

# load the matrix in the argument
volume = np.load(sys.argv[2])
fig = plt.figure(figsize=plt.figaspect(1 / 3))

#plot with cuts in Z
ax = fig.add_subplot(1, 3, 1, projection="3d")

X = np.arange(-10, 10, 10 / volume.shape[1] * 2)
Y = np.arange(-10, 10, 10 / volume.shape[2] * 2)
x, y = np.meshgrid(X, Y)

for i in range(0, volume.shape[2]):
    Z = volume[:, :, i]
    cset = ax.contour(x, y, Z, zdir="y", offset=i / (volume.shape[1] / 20) - 10)
    
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Valor")


#plot with cuts in Y
ax = fig.add_subplot(1, 3, 2, projection="3d")

X = np.arange(-10, 10, 10 / volume.shape[1] * 2)
Y = np.arange(-10, 10, 10 / volume.shape[2] * 2)
x, y = np.meshgrid(X, Y)

for i in range(0, volume.shape[2]):
    Z = volume[:, i, :]
    cset = ax.contour(x, y, Z, zdir="y", offset=i / (volume.shape[1] / 20) - 10)

ax.set_xlabel("Y")
ax.set_ylabel("X")
ax.set_zlabel("Valor")
ax.set_title("Representaciones de la matriz 3D")

#plot with cuts in X
ax = fig.add_subplot(1, 3, 3, projection="3d")

X = np.arange(-10, 10, 10 / volume.shape[1] * 2)
Y = np.arange(-10, 10, 10 / volume.shape[2] * 2)
x, y = np.meshgrid(X, Y)

for i in range(0, volume.shape[2]):
    Z = volume[i, :, :]
    cset = ax.contour(x, y, Z, zdir="z", offset=i / (volume.shape[1] / 20) - 10)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_zlim(-10, 10)

plt.savefig("matriz20.png")
plt.show()

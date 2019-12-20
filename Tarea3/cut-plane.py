import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import sys

# load the matrix in the argument
volume = np.load(sys.argv[3])
print(volume.shape[1])
if int(sys.argv[2])>(volume.shape[1]-1):
    print("Numero fuera del rango de la matriz")
    sys.exit()

#plot with cuts in Z
if sys.argv[1] in ['z','Z']:
    fig, ax = plt.subplots(1,1)
    pcm = ax.pcolormesh(volume[:,:,int(sys.argv[2])], cmap='RdBu_r')
    fig.colorbar(pcm)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Plano de corte en '+sys.argv[1]+' == '+sys.argv[2])
    ax.set_aspect('equal', 'datalim')

# #plot with cuts in Y
if sys.argv[1] in ['x','X']:
    fig, ax = plt.subplots(1,1)
    pcm = ax.pcolormesh(volume[int(sys.argv[2]),:,:], cmap='RdBu_r')
    fig.colorbar(pcm)
    ax.set_xlabel('y')
    ax.set_ylabel('z')
    ax.set_title('Plano de corte en '+sys.argv[1]+' == '+sys.argv[2])
    ax.set_aspect('equal', 'datalim')

# #plot with cuts in X
if sys.argv[1] in ['y','Y']:
    fig, ax = plt.subplots(1,1)
    pcm = ax.pcolormesh(volume[:,int(sys.argv[2]),:], cmap='RdBu_r')
    fig.colorbar(pcm)
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_title('Plano de corte en '+sys.argv[1]+' == '+sys.argv[2])
    ax.set_aspect('equal', 'datalim')

plt.savefig('corte'+sys.argv[1]+sys.argv[2])
plt.show()
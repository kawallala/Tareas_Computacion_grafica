# coding=utf-8

import numpy as np
import matplotlib.pyplot as mpl
import sys
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# Problem setup
H = 20
W = 20
Depth = 20
# Dirichlet condition
D = int(sys.argv[2])

# step
h = 20 / (int(sys.argv[1]))

"""ρ(x,y,z) = 0,1(A−5)z + (0,1Bx**2 + (A−5)**2y**2)
Mi rut es 20020425-5
por lo tanto ρ(x,y,z) = 0,1(2−5)z + (0,1*5*x**2 + (2−5)**2y**2)
ρ(x,y,z) = -0,3z + (0,5x**2 + 9*y**2)"""

# Boundary Dirichlet Conditions:
TOP = D
BOTTOM = D
LEFT = D
RIGHT = D
NEAR = D
FAR = D

# Number of unknowns
nw = int(sys.argv[1])
nh = int(sys.argv[1])
nd = int(sys.argv[1])

# funcion to use
F = (lambda i, j, k: -0.3 * (j - nd // 2) + 0.5 * (i - nw // 2) ** 2 + 9 * (k - nh // 2) ** 2)
# In this case, the domain is just a rectangle
N = nw * nh * nd

# We define a function to convert the indices from i,j to k and viceversa
# i,j indexes the discrete domain in 2D.
# k parametrize those i,j, this way we can tidy the unknowns
# in a column vector and use the standard algebra


def getU(i, j, k):
    return k * nw * nh + j * nw + i


def getIJK(u):
    i = u % nw
    j = (u // nw) % nh
    k = u // (nw * nh)
    return i, j, k


# In this matrix we will write all the coefficients of the unknowns, we use lil_matrix for low memory use
A = lil_matrix((N, N))

# In this vector we will write all the right side of the equations
b = np.zeros((N,))

# Note: To write an equation is equivalent to write a row in the matrix system

# We iterate over each point inside the domain
# Each point has an equation associated
# The equation is different depending on the point location inside the domain
for i in range(0, nw):
    for j in range(0, nd):
        for k in range(0, nh):

            # We will write the equation associated with row k
            u = getU(i, j, k)

            # We obtain indices of the other coefficients
            u_up = getU(i, j, k + 1)
            u_down = getU(i, j, k - 1)
            u_left = getU(i - 1, j, k)
            u_right = getU(i + 1, j, k)
            u_near = getU(i, j - 1, k)
            u_far = getU(i, j + 1, k)

            # Depending on the location of the point, the equation is different
            # Interior
            if (
                1 <= i
                and i <= nw - 2
                and 1 <= j
                and j <= nd - 2
                and 1 <= k
                and k <= nh - 2
            ):
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = h**2*(F(i,j,k))

            # left side
            elif i == 0 and 1 <= j and j <= nd - 2 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -LEFT + h**2*(F(i,j,k))

            # right side
            elif i == nw - 1 and 1 <= j and j <= nd - 2 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -RIGHT + h**2*(F(i,j,k))

            # top side
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nd - 2 and k == nh - 1:
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -TOP + h**2*(F(i,j,k))

            # bottom side
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nd - 2 and k == 0:
                A[u, u_up] = 1
                A[u, u_left] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM + h**2*(F(i,j,k))

            # near side
            elif 1 <= i and i <= nw - 2 and j == 0 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_right] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -NEAR + h**2*(F(i,j,k))

            # far side
            elif 1 <= i and i <= nw - 2 and j == nd - 1 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -FAR + h**2*(F(i,j,k))

            # left bottom edge
            elif i == 0 and 1 <= j and j <= nd - 2 and k == 0:
                A[u, u_up] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - LEFT + h**2*(F(i,j,k))

            # near bottom edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == 0:
                A[u, u_up] = 1
                A[u, u_right] = 1
                A[u, u_left] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - NEAR + h**2*(F(i,j,k))

            # right bottom edge
            elif i == nw - 1 and 1 <= j and j <= nd - 1 and k == 0:
                A[u, u_up] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - RIGHT + h**2*(F(i,j,k))

            # far bottom edge
            elif 1 <= i and i <= nw - 2 and j == nd - 1 and k == 0:
                A[u, u_up] = 1
                A[u, u_right] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - FAR + h**2*(F(i,j,k))

            # left near edge
            elif i == 0 and j == 0 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -LEFT - NEAR + h**2*(F(i,j,k))

            # right near edge
            elif i == nw - 1 and j == 0 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -RIGHT - NEAR + h**2*(F(i,j,k))

            # left far edge
            elif i == 0 and j == nd - 1 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -LEFT - FAR + h**2*(F(i,j,k))

            # right far edge
            elif i == nw - 1 and j == nd - 1 and 1 <= k and k <= nh - 2:
                A[u, u_up] = 1
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -RIGHT - FAR + h**2*(F(i,j,k))

            # left top edge
            elif i == 0 and 1 <= j and j <= nd - 2 and k == nh - 1:
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -LEFT - TOP + h**2*(F(i,j,k))

            # near top edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == nh - 1:
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_left] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -NEAR - TOP + h**2*(F(i,j,k))

            # right top edge
            elif i == nw - 1 and 1 <= j and j <= nd - 2 and k == nh - 1:
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -RIGHT - TOP + h**2*(F(i,j,k))

            # far top edge
            elif 1 <= i and i <= nw - 2 and j == nd - 1 and k == nh - 1:
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -FAR - TOP + h**2*(F(i,j,k))

            # corner left near lower
            elif (i, j, k) == (0, 0, 0):
                A[u, u_up] = 1
                A[u, u_right] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - LEFT - NEAR + h**2*(F(i,j,k))

            # corner rigth near lower
            elif (i, j, k) == (nw - 1, 0, 0):
                A[u, u_up] = 1
                A[u, u_left] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - RIGHT - NEAR + h**2*(F(i,j,k))

            # corner left far lower
            elif (i, j, k) == (0, nd - 1, 0):
                A[u, u_up] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - LEFT - FAR + h**2*(F(i,j,k))

            # corner right far lower
            elif (i, j, k) == (nw - 1, nd - 1, 0):
                A[u, u_up] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -BOTTOM - RIGHT - FAR + h**2*(F(i,j,k))

            # corner left near upper
            elif (i, j, k) == (0, 0, nh - 1):
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -TOP - LEFT - NEAR + h**2*(F(i,j,k))

            # corner rigth near upper
            elif (i, j, k) == (nw - 1, 0, nh - 1):
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_far] = 1
                A[u, u] = -6
                b[u] = -TOP - RIGHT - NEAR + h**2*(F(i,j,k))

            # corner left far upper
            elif (i, j, k) == (0, nd - 1, nh - 1):
                A[u, u_down] = 1
                A[u, u_right] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -TOP - LEFT - FAR + h**2*(F(i,j,k))

            # corner right far upper
            elif (i, j, k) == (nw - 1, nd - 1, nh - 1):
                A[u, u_down] = 1
                A[u, u_left] = 1
                A[u, u_near] = 1
                A[u, u] = -6
                b[u] = -TOP - RIGHT - FAR + h**2*(F(i,j,k))

            else:
                print("Point (" + str(i) + ", " + str(j) + ", " + str(k) + ") missed!")
                print("Associated point index is " + str(k))
                raise Exception()


# We convert the lil_matrix to a csr_matrix for solving
A = A.tocsr()

# Solving our system
x = spsolve(A, b)

# Now we return our solution to the 3d discrete domain
# In this matrix we will store the solution in the 3d domain
u = np.zeros((nw, nd, nh))

for t in range(0, N):
    i, j, k = getIJK(t)
    u[i, j, k] = x[t]

# Adding the borders, as they have known values
ub = np.zeros((nw + 2, nd + 2, nh + 2))

ub[1 : nw + 1, 1 : nd + 1, 1 : nh + 1] = u[:, :, :]

# Dirichlet boundary condition
# top face
ub[0 : nw + 2, 0 : nd + 2, nh + 1] = TOP
# bottom face
ub[0 : nw + 2, 0 : nd + 2, 0] = BOTTOM
# left face
ub[0, 0 : nd + 2, 0 : nh + 2] = LEFT
# right face
ub[nw + 1, 0 : nd + 2, 0 : nh + 2] = RIGHT
# near face
ub[0 : nw + 2, 0, 0 : nh + 2] = NEAR
# far face
ub[0 : nw + 2, nd + 1, 0 : nh + 2] = FAR


np.save(sys.argv[3], ub)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from D import D, D_raw
import csv


# Partial derivative

def partial_derivative(f, x0, index, epsilon=1e-4):
    x_forward = np.array(x0, dtype=float)
    x_backward = np.array(x0, dtype=float)

    x_forward[index] += epsilon
    x_backward[index] -= epsilon

    return (f(x_forward) - f(x_backward)) / (2 * epsilon)


# Fixed inputs

h_fixed = 1
r_fixed = 1
m_fixed = 0


# Grid

s_vals = np.linspace(20000, 200000, 60)
a_vals = np.linspace(18, 80, 60)

S, A = np.meshgrid(s_vals, a_vals)

indicator = np.zeros_like(S)


eps = 1e-6 #step size for numerical derivative, this seems good enough to get stable results without too much noise

for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        point = [S[i,j], A[i,j], h_fixed, r_fixed, m_fixed]

        dD_ds = partial_derivative(D_raw, point, 0)
        dD_da = partial_derivative(D_raw, point, 1)

        indicator[i,j] = abs(dD_ds) / (abs(dD_da) + eps)

# Plot

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(S, A, indicator, cmap='plasma')

ax.set_xlabel("Income (s)")
ax.set_ylabel("Age (a)")
ax.set_zlabel("Sensitivity Ratio |∂D/∂s| / |∂D/∂a|")
ax.set_title("Which Variable Dominates Disposable Income Sensitivity?")

fig.colorbar(surf, shrink=0.5, aspect=10)
with open('sensitivity_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['s', 'a', 'ratio'])
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            writer.writerow([S[i,j], A[i,j], indicator[i,j]])

plt.show()

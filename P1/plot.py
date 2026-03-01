import csv
import os


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from D import D_raw, D  # Use the raw function without max(0)
#for D positive D-raw is just D, and as it turns out now all D's are positive
#thanks to austin for setting and finding caps on expenses

# Fixing inputs so I can make a 3d graph of D_raw(s,a) with h,r,m fixed
#changed D to D_raw because D was giving me 0's all around, which was not useful for the plot


h_fixed = 1       # household size / food factor
r_fixed = 1       # housing region factor
m_fixed = 0       # standard deduction


# Generate grid of income and age

s_values = np.linspace(20000, 200000, 50)   # income
a_values = np.linspace(18, 80, 50)          # age

S, A = np.meshgrid(s_values, a_values)
D_values = np.zeros_like(S)

# Compute D_raw for each (s,a) pair
for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        x = [S[i,j], A[i,j], h_fixed, r_fixed, m_fixed]
        D_values[i,j] = D_raw(x)


# 3D Plot, please be good
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(S, A, D_values, cmap='viridis', edgecolor='k', alpha=0.9)
ax.set_xlabel('Income (s)')
ax.set_ylabel('Age (a)')
ax.set_zlabel('Disposable Income D')
ax.set_title('Raw Disposable Income vs Income and Age (h=1, r=1, m=0)')
fig.colorbar(surf, shrink=0.5, aspect=10, label='D')


with open('D_raw_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['s', 'a', 'D'])
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            writer.writerow([S[i,j], A[i,j], D_values[i,j]])
print("Saved to:", os.path.abspath('D_raw_data.csv'))
plt.show()

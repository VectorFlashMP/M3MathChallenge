import numpy as np
import pandas as pd

#sigh, ok so Austin basically said "fine, I'll do it myself", so I will just leave all my work, he'll get a function and I willl just make this
#test
csv_path = 
df = pd.read_csv(csv_path)

# Separating inputs (X) and true outputs (y)
# Assumes last column is y
X = df.iloc[:, :-1].values   # all columns except last
y_true = df.iloc[:, -1].values


def f(x):
    # Just some random function
    return x[0]**2 + x[1]*np.exp(x[2])


y_pred = np.array([f(x) for x in X])
mse = np.mean((y_true - y_pred)**2)
print("Predicted values (y_pred):", y_pred)
print("Mean Squared Error:", mse)

def directional_derivative(f, x0, v, epsilon=1e-6):
    """
    f: function from R^n -> R
    x0: point (numpy array)
    v: unit vector direction (numpy array)
    epsilon: small step for finite difference
    """
    x0 = np.array(x0, dtype=float)
    v = np.array(v, dtype=float)
    v = v / np.linalg.norm(v)  # ensure unit vector
    return (f(x0 + epsilon*v) - f(x0 - epsilon*v)) / (2*epsilon)

#testing cases
point = X[0]  # point 
direction = np.array([1, 0, 0])  # derivative along x1 (adjust dimension)
dd_val = directional_derivative(f, point, direction)
print(f"Directional derivative at {point} along {direction}:", dd_val)

# i+j
direction2 = np.array([1,1,0])/np.sqrt(2)
dd_val2 = directional_derivative(f, point, direction2)
print(f"Directional derivative along {direction2}:", dd_val2)

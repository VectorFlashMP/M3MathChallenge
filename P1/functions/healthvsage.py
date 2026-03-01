import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Full path to your CSV
csv_path = r"C:\Users\nishu\math-modeling\python\healthcare.csv"

# Load CSV
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Automatically detect year columns
year_cols = [col for col in df.columns if col.isdigit()]

# Keep only rows that are actual age groups, ignore 'Total' and other columns
age_rows = df[df['Age Group'].str.strip().str.contains(r'\d')]

# Function to convert age group to midpoint
def age_midpoint(age_group):
    age_group = str(age_group).strip()
    if '-' in age_group:
        low, high = age_group.split('-')
        return (float(low) + float(high)) / 2
    if '+' in age_group:
        low = age_group.replace('+','')
        return float(low) + 10  # approximate midpoint for open-ended
    return np.nan

# Prepare vectors
age_vector = np.array([age_midpoint(r) for r in age_rows['Age Group']])
cost_vector = age_rows[year_cols].mean(axis=1).values  # average across years

# Exponential model
def model(age, a, b, c):
    return a * np.exp(b * age) + c

# Initial guess
p0 = [min(cost_vector), 0.01, 0]  # ensure b > 0

# Fit curve
params, cov = curve_fit(model, age_vector, cost_vector, p0=p0, maxfev=10000)
a_opt, b_opt, c_opt = params
print(f"Optimized parameters: a={a_opt:.2f}, b={b_opt:.4f}, c={c_opt:.2f}")

# Plot
age_smooth = np.linspace(min(age_vector), max(age_vector), 200)
cost_fit = model(age_smooth, *params)

plt.scatter(age_vector, cost_vector, label="Average Cost per Age Group")
plt.plot(age_smooth, cost_fit, color='red', label="Exponential Fit")
plt.xlabel("Age")
plt.ylabel("Healthcare Cost")
plt.title("Healthcare Cost vs Age (All Years Averaged)")
plt.legend()
plt.show()
#result upon running on a csv from https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data: a=-0.00, b=0.4221, c=22142.20 so, factor in exponential is 0.4221(really low_
#improvements to be made: a better fit

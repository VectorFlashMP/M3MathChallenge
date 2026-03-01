# D.py
import numpy as np


# Constants

# Federal tax brackets
B = np.array([0, 11600, 47150, 100525, 191950, 243725, 609350, np.inf])
t = np.array([0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37])

# Other constants
bar_H = 1487      # median housing cost
beta = 0.8
f_bar = 1.0       # scale factor for food
s0 = 1.0          # reference income for Engel's law
f_max = 600       # capped food per person
R_urban = 130
R_suburban = 965

# FICA constants
W = 168600        # Social Security wage base
c0 = 92           # healthcare baseline
c1 = 4.3          # healthcare increment per year above 40


# Component functions
def d_m(m):
    """Standard deduction by marital status"""
    return 14600 if m == 0 else 29200

def tau_fed(s, m):
    """Federal income tax with standard deduction"""
    s_tilde = s - d_m(m)
    tax = 0.0
    for k in range(1, len(B)):
        taxable = max(0, min(s_tilde - B[k-1], B[k] - B[k-1]))
        tax += t[k-1] * taxable
    return tax

def tau_state(s, tau_state_rate=0.05):
    """Simple flat state tax (can adjust regionally)"""
    return tau_state_rate * s

def tau_FICA(s):
    """Social Security + Medicare"""
    return 0.062 * min(s, W) + 0.0145 * s

def T(s, m, tau_state_rate=0.05):
    """Total monthly tax burden"""
    total_tax = tau_fed(s, m) + tau_state(s, tau_state_rate) + tau_FICA(s)
    return total_tax / 12.0

def H(r, m):
    """Housing cost"""
    return r * bar_H / (1 + 0.4*m)

def F(s, h):
    """Food cost via Engel's Law with cap"""
    return h * min(f_max, f_bar * (s/s0)**beta)

def R_cost(location='urban'):
    """Transportation cost"""
    return R_urban if location.lower() == 'urban' else R_suburban

def C(a):
    """Healthcare cost"""
    return c0 + c1 * max(0, a - 40)

def B_cost(a):
    """Debt cost"""
    if 22 <= a <= 35:
        return 350
    elif 35 < a <= 50:
        return 150
    else:
        return 0


# 3. Master disposable income


def D(x):
    """Disposable income (capped at 0)"""
    s, a, h, r, m = x
    disposable = (
        (s - tau_fed(s, m) - tau_state(s) - tau_FICA(s))/12
        - H(r, m)
        - F(s, h)
        - R_cost('urban')
        - C(a)
        - B_cost(a)
    )
    return max(0.0, disposable)

def D_raw(x):
    """Raw disposable income without max(0) for derivatives/sensitivity"""
    s, a, h, r, m = x
    disposable = (
        (s - tau_fed(s, m) - tau_state(s) - tau_FICA(s))/12
        - H(r, m)
        - F(s, h)
        - R_cost('urban')
        - C(a)
        - B_cost(a)
    )
    return disposable

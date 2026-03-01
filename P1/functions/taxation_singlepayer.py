import numpy as np
tax_rate=np.array([10,12,22,24,32,35,37])
income=np.array([0,11926,48476,103351,197301,250526,626351])
def tax(income):
    tax_amount=0
    for i in range(len(income)):
        if income>income[i]:
            tax_amount+=(min(income,income[i+1])-income[i])*tax_rate[i]/100
        else:
            break
    return tax_amount

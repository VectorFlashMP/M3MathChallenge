import numpy as np
m=int(input("Enter 1 if not married 0 if married: "))
#wasted memory but who cares, 2-m will not become an int otherwise
#if I called it a bool, 
# hmm maybe I should use C++ instead
if m==1:
    tax_rate=np.array([10,12,22,24,32,35,37])
    income=np.array([0,11926,48476,103351,197301,250526,626351])
else:
    tax_rate=np.array([10,12,22,24,32,35,37])
    income=np.array([0,23851,96951,206761,394601,501051,751601])
def tax(income):
        tax_amount=0
        for i in range(len(income)):
            if income>income[i]:
                tax_amount+=(min(income,income[i+1])-income[i])*tax_rate[i]/100
            else:
                break
        return tax_amount

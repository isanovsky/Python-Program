import math

def f(x):
    return (math.log(x) - 1 - (1/x**2))

xl = 2
xu = 5
tol = 0.000005
APRE = 100  # Initial APRE value
i = 0 #itersi
xr = (xl + xu) / 2  # Initialize xr to avoid referencing it before assignment

print("-"*90)
print("iter. \t xl \t\t xu \t\t xr \t\t APRE (%)")
print("-"*90)
while (i < 5 or APRE > tol):
    xr_old = xr  # Store the previous value of xr
    xr = (xl + xu) / 2  # Compute the midpoint
    APRE = abs((xr - xr_old) / xr) * 100  # Calculate APRE
    print("{0:d} \t {1:.7f} \t{2:.7f} \t{3:.7f} \t{4:.7f}".format(i, xl, xu, xr, APRE))

    if f(xr) * f(xl) < 0:
        xu = xr
    else:
        xl = xr
    
    i += 1  # Increment iteration
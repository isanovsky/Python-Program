import math

print("-" * 45 + "Regula Falsi Method" + "-" * 45)
def regula_falsi_method(f, a, b, tol=0.5e-5, max_iterations=100):
    if f(a) * f(b) >= 0:
        print("Regula Falsi method fails. The function must have different signs at a and b.")
        return None

    print(f"{'Iteration':<10} {'a':<12} {'b':<12} {'c':<12} {'f(a)':<12} {'f(b)':<12} {'f(c)':<12} {'error %':<12}")
    
    c = a  # Initial approximation
    prev_c = None 
    iteration = 0
    
    for iteration in range(1, max_iterations + 1):
        f_a = f(a)
        f_b = f(b)
        c = (a * f_b - b * f_a) / (f_b - f_a)
        f_c = f(c)

        if prev_c is not None:
            error = abs((c - prev_c) / c) * 100
        else:
            error = None

        print(f"{iteration:<10} {a:<12.7f} {b:<12.7f} {c:<12.7f} {f_a:<12.7f} {f_b:<12.7f} {f_c:<12.7f} {error if error is not None else 0.0 :<12.7f}")
        
        if error is not None and error < tol and abs(f_c) < tol:
            return c, iteration

        if f_a * f_c < 0:
            b = c
        else:
            a = c

        prev_c = c

    return None, iteration

def f(x):
    return math.log(x) - 1 - 1 / x**2

a = 2.0
b = 5.0

root, iterations = regula_falsi_method(f, a, b, tol=0.5e-5)

if root is not None:
    print(f"\nThe approximate root is: {root} at {iterations} iterations")
else:
    print("\nThe regula falsi method failed to converge.")

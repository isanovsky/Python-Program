import math

print("-" * 45 + "Secant Method" + "-" * 45)
def secant_method(f, x0, x1, tolerance=0.5e-5, max_iterations=100):
    print(f"{'Iteration':<10} {'xi-1':<12} {'x1':<12} {'xi+1':<12} {'f(xi-1)':<12} {'f(xi)':<12} {'f(xi+1)':<12} {'error %':<12}")
    print("-" * 103)
    iteration = 0
    
    while iteration < max_iterations:
        f_x0 = f(x0)
        f_x1 = f(x1)
        error = 0
        
        if f_x1 == f_x0:  
            print("Error: Division by zero due to f(x1) - f(x0) being zero.")
            return None

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = f(x2)

        if iteration > 0:
            error = abs((x2 - x1) / x2) * 100 if x2 != 0 else 0

        print(f"{iteration:<10} {x0:<12.7f} {x1:<12.7f} {x2:<12.7f} {f_x0:<12.7f} {f_x1:<12.7f} {f_x2:<12.7f} {error:<12.7f}")
        
        if abs(x2 - x1) < tolerance:
            print(f"\nThe approximate root is: {x2} after {iteration+1} iterations")
            return x2

        x0, x1 = x1, x2
        iteration += 1

    print("Did not converge within the maximum number of iterations")
    return None

def f(x):
    return math.log(x) - 1 - 1/x**2

x0 = float(input("Enter the initial guess for x0: "))
x1 = float(input("Enter the initial guess for x1: "))
root = secant_method(f, x0, x1)

import math

print("-" * 45 + "Newton Raphson Method" + "-" * 45)
def newton_raphson(xi, tolerance, max_iterations):
    # F(x) 
    f = lambda x: math.log(x) - 1 - 1 / (x ** 2)
    # F'(x)
    df = lambda x: 1 / x + 2 / (x ** 3)

    print(f"{'Iteration':<10} {'xi':<10} {'f(xi)':<10} {'f\'(xi)':<10} {'error %':<10}")

    previous_xi = xi
    for i in range(max_iterations):
        fxi = f(xi)
        dfxi = df(xi)
        error = 0.0
        next_xi = xi - fxi / dfxi

        if i > 0:
            error = abs((xi - previous_xi) / xi) * 100

        print(f"{i:<10} {xi:<10.7f} {fxi:<10.7f} {dfxi:<10.7f} {error:<10.8f}")

        if error < tolerance and i > 0:
            print(f"The approximate root is {xi:.8f} after {i+1} iterations")
            break

        previous_xi = xi
        xi = next_xi

xi = 2.0
tolerance = 0.5e-5
max_iterations = 100

newton_raphson(xi, tolerance, max_iterations)

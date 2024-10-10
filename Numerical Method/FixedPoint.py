import math

print("-" * 20 + "Fixed Point Iteration Method" + "-" * 20)
def fixed_point_iteration(xi, tolerance, max_iterations):
    # Define g(x) and f(x)
    g = lambda x: math.exp(1 + 1 / (x * x))
    f = lambda x: math.log(x) - 1 - 1 / (x * x)

    print(f"{'Iteration':<10} {'xi':<10} {'g(xi)':<10} {'f(xi)':<10} {'error %':<10}")

    previous_xi = xi
    for i in range(max_iterations):
        gxi = g(xi)
        fxi = f(xi)
        error = 0.0

        if i > 0:
            error = abs((xi - previous_xi) / xi) * 100

        print(f"{i:<10} {xi:<10.7f} {gxi:<10.7f} {fxi:<10.7f} {error:<10.7f}")

        if error < tolerance and i > 0:
            break

        previous_xi = xi
        xi = gxi

    print(f"The approximate root is {xi:.7f} after {i+1} iterations.")

xi = 2.0
tolerance = 0.5e-5
max_iterations = 100

fixed_point_iteration(xi, tolerance, max_iterations)

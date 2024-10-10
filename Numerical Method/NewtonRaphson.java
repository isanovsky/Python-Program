import java.util.function.Function;

public class NewtonRaphson {

    public static void main(String[] args) {
        double xi = 2.0;
        double tolerance = 0.5e-5;
        int maxIterations = 100;

        // F(x)
        Function<Double, Double> f = x -> Math.log(x) - 1 - 1 / (x * x);
        // F'(x)
        Function<Double, Double> df = x -> 1 / x + 2 / (x * x * x);

        System.out.printf("%-10s %-10s %-10s %-10s %-10s%n", "Iteration", "xi", "f(xi)", "f'(xi)", "error %");

        double previousXi = xi;
        for (int i = 0; i < maxIterations; i++) {
            double fxi = f.apply(xi);
            double dfxi = df.apply(xi);
            double error = 0.0;
            double nextXi = xi - fxi / dfxi;

            if (i > 0) {
                error = Math.abs((xi - previousXi) / xi) * 100;
            }

            System.out.printf("%-10d %-10.7f %-10.7f %-10.7f %-10.8f%n", i, xi, fxi, dfxi, error);

            if (error < tolerance && i > 0) {
                System.out.printf("The approximate root is %8f after %d iterations", xi, i+1);
                break;
            }

            previousXi = xi;
            xi = nextXi;
        }
    }
}
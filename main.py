import math


class Result:
    def __init__(self, iterations, x):
        self.iterations = iterations
        self.x = x


def f(polynomial, x):
    polynomial_sum = 0
    exponent = len(polynomial) - 1
    for coefficient in polynomial:
        polynomial_sum += coefficient * pow(x, exponent)
        exponent -= 1
    return polynomial_sum


def derivative(polynomial):
    new_polynomial = polynomial.copy()
    exponent = len(polynomial) - 1
    for i in range(len(polynomial) - 1):
        new_polynomial[i] *= exponent
        exponent -= 1
    new_polynomial.pop()
    return new_polynomial


def bisection_method(polynomial, start_point, end_point, epsilon):
    a = start_point
    b = end_point
    c = (a + b) / 2
    max_iterations = math.ceil(-math.log10(epsilon / (b - a))/math.log10(2))

    for i in range(max_iterations + 1):
        c = (a + b) / 2
        if abs(f(polynomial, c)) < epsilon or (b - a)/2 < epsilon:
            return Result(i + 1, c)
        if f(polynomial, a) * f(polynomial, c) < 0:
            b = c
        else:
            a = c
    return None


def newton_method(polynomial, start_point, end_point, epsilon):
    polynomial_derivative = derivative(polynomial)
    x = (start_point + end_point)/2

    for i in range(30):
        x = x - f(polynomial, x)/f(polynomial_derivative, x)
        if abs(f(polynomial, x)) < epsilon:
            return Result(i + 1, x)
    return None


def secant_method(polynomial, start_point, end_point, epsilon):
    a = start_point
    b = end_point
    i = 0
    while abs(f(polynomial, b) - f(polynomial, a)) > epsilon:
        b, a = (a*f(polynomial, b) - b*f(polynomial, a))/(f(polynomial, b) - f(polynomial, a)), b
        if abs(f(polynomial, b)) < epsilon:
            return Result(i + 1, b)
        i += 1
    return None


def main():
    methods = [bisection_method, newton_method, secant_method]
    def_epsilon = 0.00001

    polynomial = [1, 0, -25]  # example: [1, 0, -25] is x^2 - 25
    polynomial_derivative = derivative(polynomial)

    start_point = -10
    end_point = 10
    step = 0.1

    choice = int(input("1. Bisection method\n2. Newton–Raphson method\n3. Secant method\n4. Exit\nInput: ")) - 1
    while 0 <= choice <= 2:
        x = start_point
        results = []
        while x + step <= end_point:
            if f(polynomial, x) * f(polynomial, x + step) < 0:
                print("- Found possible root, f({}) * f({}) < 0".format(x, x + step))
                result = methods[choice](polynomial, x - step, x + step, def_epsilon)
                if result is not None:
                    print("- Result x = {} found, it took {} iterations.".format(result.x, result.iterations))
                    results.append(result.x)
                else:
                    print("Result not found, method failed.")
            elif f(polynomial_derivative, x) * f(polynomial_derivative, x + step) < 0:
                print("- Found possible root using the derivative, f'({}) * f'({}) < 0".format(x, x + step))
                result = methods[choice](polynomial_derivative, x - step, x + step, def_epsilon)
                if result is not None:
                    print("- Result x = {} found, it took {} iterations.".format(result.x, result.iterations), end=' ')
                    if abs(f(polynomial, result.x)) > def_epsilon:
                        print("But it's invalid as it's not a root for the original function.")
                    else:
                        results.append(result.x)
                        print()
                else:
                    print("Result not found, method failed.")
            x += step
        if len(results):
            print("\nFinal results:")
            for x in results:
                print("x = {}".format(x))
            print()
        choice = int(input("1. Bisection method\n2. Newton–Raphson method\n3. Secant method\n4. Exit\nInput: ")) - 1


if __name__ == '__main__':
    main()

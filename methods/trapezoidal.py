import numpy as np

def trapezoidal_rule(f, a, b, n):
    """
    Approximates the integral using the Trapezoidal Rule.
    n: number of sub-intervals (replaces max_iter in UI)
    """
    steps = []
    h = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    
    total_sum = 0.5 * (f(a) + f(b))
    
    for i in range(1, n):
        x = a + i * h
        fx = f(x)
        total_sum += fx
        
        steps.append({
            "Iteration": i,
            "a": round(x, 6),
            "b": "-",
            "Midpoint (x)": "-",
            "f(x)": round(fx, 6),
            "Error": "-"
        })
        
    result = total_sum * h
    return steps, result
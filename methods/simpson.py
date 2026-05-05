import numpy as np

def simpson_rule(f, a, b, n):
    """
    Approximates the integral using Simpson's 1/3 Rule.
    n: must be even.
    """
    if n % 2 != 0:
        return None, "Error: Number of intervals (n) must be even for Simpson's Rule."
        
    steps = []
    h = (b - a) / n
    total_sum = f(a) + f(b)
    
    for i in range(1, n):
        x = a + i * h
        fx = f(x)
        
        if i % 2 == 0:
            total_sum += 2 * fx
        else:
            total_sum += 4 * fx
            
        steps.append({
            "Iteration": i,
            "a": round(x, 6),
            "b": "-",
            "Midpoint (x)": "-",
            "f(x)": round(fx, 6),
            "Error": "-"
        })
        
    result = total_sum * (h / 3)
    return steps, result
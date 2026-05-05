def bisection_method(f, xl, xr, tol, max_iter):
    steps = []
    
    # Round initial inputs
    xl = round(float(xl), 6)
    xr = round(float(xr), 6)
    tol = float(tol)
    
    fxl_init = round(float(f(xl)), 6)
    fxr_init = round(float(f(xr)), 6)
    
    check_initial = round(fxl_init * fxr_init, 6)
    if check_initial > 0:
        return None, "Error: No sign change in interval."

    for i in range(1, max_iter + 1):
        sum_x = round(xl + xr, 6)
        xn = round(sum_x / 2.0, 6)
        
        fxl = round(float(f(xl)), 6)
        fxr = round(float(f(xr)), 6)
        fxn = round(float(f(xn)), 6)
        
        # Dictionary keys strictly match the client's Excel headers
        steps.append({
            "iteration no.": i,
            "xl": f"{xl:.6f}",
            "xr": f"{xr:.6f}",
            "xn": f"{xn:.6f}",
            "f(xl)": f"{fxl:.6f}",
            "f(xr)": f"{fxr:.6f}",
            "F(xn)": f"{fxn:.6f}"
        })

        # New Stopping Condition: Stop when the absolute value of F(xn) is less than the tolerance
        if abs(fxn) < tol:
            return steps, xn
            
        # Determine which bound to replace
        check_sign = round(fxl * fxn, 6)
        if check_sign < 0:
            xr = xn
        else:
            xl = xn
            
    return steps, xn
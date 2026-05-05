import sympy as sp

def newton_raphson_method(f_lambda, x0, tol, max_iter, func_str):
    steps = []
    x_sym = sp.symbols('x')
    df_expr = sp.diff(sp.sympify(func_str), x_sym)
    df = sp.lambdify(x_sym, df_expr, modules=['numpy'])
    
    curr_x = round(float(x0), 6)
    
    fx = round(float(f_lambda(curr_x)), 6)
    dfx = round(float(df(curr_x)), 6)
    
    steps.append({
        "Iteration": 1,
        "x": f"{curr_x:.6f}",
        "f(X)": f"{fx:.6f}",
        "f'(x)": f"{dfx:.6f}",
        "Relative Error (%)": "N/A"
    })
    
    for i in range(2, max_iter + 2):
        if abs(dfx) < 1e-12:
            return None, "Error: Derivative is zero. Method fails."
        
        # compute using rounded values
        ratio = round(fx / dfx, 6)
        next_x = round(curr_x - ratio, 6)
        
        # relative error using rounded values
        if next_x != 0:
            error = round(abs((next_x - curr_x) / next_x), 6)
        else:
            error = 0.000000
        
        error_percent = round(error * 100, 6)
        
        curr_x = next_x
        fx = round(float(f_lambda(curr_x)), 6)
        dfx = round(float(df(curr_x)), 6)
        
        steps.append({
            "Iteration": i,
            "x": f"{curr_x:.6f}",
            "f(X)": f"{fx:.6f}",
            "f'(x)": f"{dfx:.6f}",
            "Relative Error (%)": f"{error_percent:.6f}"
        })
        
        if error < tol:
            return steps, curr_x
            
    return steps, curr_x
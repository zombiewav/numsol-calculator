import sympy as sp


def fixed_point_iteration(g_lambda, x0, tol, max_iter, g_str):
    steps = []
    x_sym = sp.symbols('x')

    try:
        g_expr = sp.sympify(g_str)
        dg_expr = sp.diff(g_expr, x_sym)
        dg_lambda = sp.lambdify(x_sym, dg_expr, modules=['numpy', 'sympy'])
    except Exception as e:
        return None, f"Invalid g(x): {e}"

    x_prev = round(float(x0), 6)
    tol = float(tol)

    try:
        dg_at_x0 = round(float(dg_lambda(x_prev)), 6)
    except Exception as e:
        return None, f"Convergence test error: {e}"

    if abs(dg_at_x0) >= 1:
        return None, f"Convergence test failed: |g'(x0)| = {abs(dg_at_x0):.6f}. Enter a different g(x)."

    for i in range(1, max_iter + 1):
        try:
            # compute using rounded value only
            gx = round(float(g_lambda(x_prev)), 6)
        except Exception as e:
            return None, f"Calculation error: {e}"

        # error based on rounded values
        error = round(abs(gx - x_prev), 6)

        steps.append({
            "Iteration": i,
            "x": f"{x_prev:.6f}",
            "g(x)": f"{gx:.6f}",
            "Error": f"{error:.6f}"
        })

        if error < tol:
            return steps, gx

        # carry forward rounded value only
        x_prev = round(float(gx), 6)

    return steps, x_prev
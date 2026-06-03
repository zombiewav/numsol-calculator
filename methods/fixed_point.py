from decimal import Decimal, ROUND_HALF_UP
import sympy as sp


def retain_6(value):
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.000001"),
            rounding=ROUND_HALF_UP
        )
    )


def format_6(value):
    return f"{retain_6(value):.6f}"


def fixed_point_iteration(g_lambda, x0, tol, max_iter, g_str):

    steps = []
    x_sym = sp.symbols('x')

    try:
        g_expr = sp.sympify(g_str)
        dg_expr = sp.diff(g_expr, x_sym)
        dg_lambda = sp.lambdify(x_sym, dg_expr, modules=['numpy', 'sympy'])
    except Exception as e:
        return None, f"Invalid g(x): {e}"

    x_prev = retain_6(float(x0))
    tol = float(tol)

    # convergence warning only
    try:
        dg_at_x0 = retain_6(dg_lambda(x_prev))
    except Exception as e:
        return None, f"Convergence test error: {e}"

    convergence_warning = None

    if abs(dg_at_x0) >= 1:
        convergence_warning = (
            f"Warning: |g'(x0)| = {abs(dg_at_x0):.6f} ≥ 1. "
            f"The method may not converge."
        )

    for i in range(1, max_iter + 1):

        try:
            gx = retain_6(g_lambda(x_prev))
        except Exception as e:
            return None, f"Calculation error: {e}"

        # current relative approximate error
        if gx == 0:
            current_error_value = 0.0 if gx == x_prev else float("inf")
        else:
            current_error_value = retain_6(
                abs((gx - x_prev) / gx) * 100
            )

        if i == 1:
            steps.append({
                "Iteration": i,
                "x": format_6(x_prev),
                "g(x)": format_6(gx),
                "Error": ""
            })
        else:
            steps.append({
                "Iteration": i,
                "x": format_6(x_prev),
                "g(x)": format_6(gx),
                "Error": format_6(current_error_value)
            })

        # actual stopping condition
        if current_error_value < tol:
            return steps, gx

        x_prev = gx

    return steps, x_prev
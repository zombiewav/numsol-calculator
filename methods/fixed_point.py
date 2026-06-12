from decimal import Decimal, ROUND_HALF_UP
import sympy as sp


def retain_6(value):
    return float(
        Decimal(str(float(value))).quantize(
            Decimal("0.000001"),
            rounding=ROUND_HALF_UP
        )
    )


def format_6(value):
    return f"{retain_6(value):.6f}"


def safe_float(val):
    try:
        return float(val)
    except Exception:
        try:
            return float(sp.N(val))
        except Exception:
            return float(complex(val).real)


def fixed_point_iteration(g_lambda, x0, tol, max_iter, g_str):

    steps = []
    x_sym = sp.symbols('x')

    try:
        g_expr = sp.sympify(g_str)
        dg_expr = sp.diff(g_expr, x_sym)
        dg_lambda = sp.lambdify(x_sym, dg_expr, modules=['math'])
    except Exception as e:
        return None, f"Invalid g(x): {e}"

    try:
        g_expr_clean = sp.sympify(g_str)
        g_lambda_math = sp.lambdify(x_sym, g_expr_clean, modules=['math'])
    except Exception as e:
        return None, f"Could not build math lambda: {e}"

    x_prev = retain_6(float(x0))
    tol = float(tol)

    try:
        dg_at_x0 = retain_6(safe_float(dg_lambda(x_prev)))
    except Exception as e:
        return None, f"Convergence test error: {e}"

    if abs(dg_at_x0) >= 1:
        convergence_warning = (
            f"Warning: |g'(x0)| = {abs(dg_at_x0):.6f} ≥ 1. "
            f"The method may not converge."
        )

    previous_error = None

    for i in range(1, max_iter + 1):

        try:
            gx = retain_6(safe_float(g_lambda_math(x_prev)))
        except Exception as e:
            return None, f"Calculation error at iteration {i}: {e}"

        actual_error = (
            retain_6(abs((gx - x_prev) / gx) * 100)
            if gx != 0
            else 0.0
        )

        if i == 1:
            display_error = "N/A"
        else:
            display_error = format_6(previous_error)

        steps.append({
            "Iteration": i,
            "x": format_6(x_prev),
            "g(x)": format_6(gx),
            "Error": display_error
        })

        previous_error = actual_error

        if actual_error < tol:

            try:
                gx_next = retain_6(
                    safe_float(g_lambda_math(gx))
                )
            except Exception:
                gx_next = gx

            steps.append({
                "Iteration": i + 1,
                "x": format_6(gx),
                "g(x)": format_6(gx_next),
                "Error": format_6(actual_error)
            })

            return steps, gx_next

        x_prev = gx

    return steps, x_prev
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


def newton_raphson_method(f_lambda, x0, tol, max_iter, func_str):
    steps = []

    x_sym = sp.symbols('x')
    df_expr = sp.diff(sp.sympify(func_str), x_sym)
    df = sp.lambdify(x_sym, df_expr, modules=['numpy'])

    curr_x = retain_6(float(x0))
    tol = float(tol)

    fx = retain_6(f_lambda(curr_x))
    dfx = retain_6(df(curr_x))

    steps.append({
        "Iteration": 1,
        "x": format_6(curr_x),
        "f(X)": format_6(fx),
        "f'(x)": format_6(dfx),
        "Relative Error (%)": "N/A"
    })

    if abs(fx) < tol:
        return steps, curr_x

    for i in range(2, max_iter + 2):

        if abs(dfx) < 1e-12:
            return None, "Error: Derivative is zero. Method fails."

        ratio = retain_6(fx / dfx)
        next_x = retain_6(curr_x - ratio)

        if abs(next_x) < 1e-12:
            error = 0.0
        else:
            error = retain_6(abs((next_x - curr_x) / next_x))

        error_percent = retain_6(error * 100)

        curr_x = next_x
        fx = retain_6(f_lambda(curr_x))
        dfx = retain_6(df(curr_x))

        steps.append({
            "Iteration": i,
            "x": format_6(curr_x),
            "f(X)": format_6(fx),
            "f'(x)": format_6(dfx),
            "Relative Error (%)": format_6(error_percent)
        })

        if abs(fx) < tol or error < tol:

            # one extra verification iteration
            if abs(dfx) > 1e-12:

                verify_ratio = retain_6(fx / dfx)
                verify_x = retain_6(curr_x - verify_ratio)

                if verify_x == curr_x:

                    steps.append({
                        "Iteration": i + 1,
                        "x": format_6(curr_x),
                        "f(X)": format_6(fx),
                        "f'(x)": format_6(dfx),
                        "Relative Error (%)": format_6(0.0)
                    })

            return steps, curr_x

    return steps, curr_x
from decimal import Decimal, ROUND_HALF_UP


def retain_6(value):
    return float(
        Decimal(str(float(value))).quantize(
            Decimal("0.000001"),
            rounding=ROUND_HALF_UP
        )
    )


def format_6(value):
    val = retain_6(value)
    formatted = f"{val:.6f}"
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    return formatted


def round_6(value):
    return retain_6(value)


def safe_float(val):
    try:
        return float(val)
    except Exception:
        import sympy as sp
        return float(sp.N(val))


def secant_method(f, xa, xb, tol, max_iter):
    steps = []

    x0_full = float(xa)
    x1_full = float(xb)
    tol = float(tol)

    fx0_full = safe_float(f(x0_full))
    fx1_full = safe_float(f(x1_full))

    x0_display = round_6(x0_full)
    x1_display = round_6(x1_full)
    fx0_display = safe_float(f(x0_display))
    fx1_display = safe_float(f(x1_display))

    steps.append({
        "Iteration": 1,
        "Xa": format_6(x0_display),
        "Xb": format_6(x1_display),
        "f(Xa)": format_6(fx0_display),
        "f(Xb)": format_6(fx1_display),
        "Relative Error (%)": "N/A"
    })

    previous_x1_display = x1_display

    for iteration in range(2, max_iter + 1):

        diff_f = fx1_full - fx0_full

        if abs(diff_f) < 1e-10:
            return steps, float(f"{x1_full:.6f}")

        x_next_full = x1_full - (fx1_full * (x1_full - x0_full)) / diff_f

        x0_full = x1_full
        x1_full = x_next_full

        fx0_full = fx1_full
        fx1_full = safe_float(f(x1_full))

        x0_display = round_6(x0_full)
        x1_display = round_6(x1_full)
        fx0_display = safe_float(f(x0_display))
        fx1_display = safe_float(f(x1_display))

        error_percent = abs((x1_display - previous_x1_display) / x1_display) * 100

        row = {
            "Iteration": iteration,
            "Xa": format_6(x0_display),
            "Xb": format_6(x1_display),
            "f(Xa)": format_6(fx0_display),
            "f(Xb)": format_6(fx1_display),
            "Relative Error (%)": format_6(error_percent)
        }
        steps.append(row)

        # Stop when Xa == Xb at display level (no more change)
        if x0_display == x1_display:
            return steps, float(f"{x1_full:.6f}")

        previous_x1_display = x1_display

    return steps, float(f"{x1_full:.6f}")
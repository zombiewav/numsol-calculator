from decimal import Decimal, ROUND_HALF_UP


def retain_6(value):
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.000001"),
            rounding=ROUND_HALF_UP
        )
    )


def format_6(value):
    return f"{retain_6(value):.6f}"


def bisection_method(f, xl, xr, tol, max_iter):
    steps = []

    # Round initial inputs properly
    xl = retain_6(float(xl))
    xr = retain_6(float(xr))
    tol = float(tol)

    fxl_init = retain_6(f(xl))
    fxr_init = retain_6(f(xr))

    check_initial = retain_6(fxl_init * fxr_init)

    if check_initial > 0:
        return None, "Error: No sign change in interval."

    for i in range(1, max_iter + 1):

        sum_x = retain_6(xl + xr)
        xn = retain_6(sum_x / 2.0)

        fxl = retain_6(f(xl))
        fxr = retain_6(f(xr))
        fxn = retain_6(f(xn))

        steps.append({
            "iteration no.": i,
            "xl": format_6(xl),
            "xr": format_6(xr),
            "xn": format_6(xn),
            "f(xl)": format_6(fxl),
            "f(xr)": format_6(fxr),
            "F(xn)": format_6(fxn)
        })

        # Classroom / video-style stopping condition
        if abs(fxn) < tol:
            return steps, xn

        # interval update
        check_sign = retain_6(fxl * fxn)

        if check_sign < 0:
            xr = xn
        else:
            xl = xn

    return steps, xn
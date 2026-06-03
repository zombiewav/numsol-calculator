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


def regula_falsi_method(f, xL, xR, tol, max_iter):

    xL = retain_6(float(xL))
    xR = retain_6(float(xR))
    tol = float(tol)

    fxL = retain_6(f(xL))
    fxR = retain_6(f(xR))

    if abs(fxL) < tol:
        steps = [{
            "Iteration no": 1,
            "xL": format_6(xL),
            "xR": format_6(xR),
            "xN": format_6(xL),
            "f(xL)": format_6(fxL),
            "f(xR)": format_6(fxR),
            "f(xN)": format_6(fxL),
        }]
        return steps, xL

    if abs(fxR) < tol:
        steps = [{
            "Iteration no": 1,
            "xL": format_6(xL),
            "xR": format_6(xR),
            "xN": format_6(xR),
            "f(xL)": format_6(fxL),
            "f(xR)": format_6(fxR),
            "f(xN)": format_6(fxR),
        }]
        return steps, xR

    if retain_6(fxL * fxR) > 0:
        return None, "Root not bracketed. f(xL) and f(xR) must have opposite signs."

    steps = []

    for i in range(1, max_iter + 1):

        diff_f = retain_6(fxL - fxR)

        if abs(diff_f) < 1e-12:
            return None, "Error: Division by zero."

        xN = retain_6(
            xR - (fxR * (xL - xR)) / diff_f
        )

        fxN = retain_6(f(xN))

        steps.append({
            "Iteration no": i,
            "xL": format_6(xL),
            "xR": format_6(xR),
            "xN": format_6(xN),
            "f(xL)": format_6(fxL),
            "f(xR)": format_6(fxR),
            "f(xN)": format_6(fxN),
        })

        # Classroom / video-style stopping condition
        if abs(fxN) < tol:
            return steps, xN

        # bracket update
        if retain_6(fxL * fxN) < 0:
            xR = xN
            fxR = fxN
        else:
            xL = xN
            fxL = fxN

    return steps, xN
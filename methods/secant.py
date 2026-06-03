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


def secant_method(f, xa, xb, tol, max_iter):

    steps = []

    xa = float(xa)
    xb = float(xb)
    tol = float(tol)

    fxa = f(xa)
    fxb = f(xb)

    steps.append({
        "Iteration": 1,
        "Xa": format_6(xa),
        "Xb": format_6(xb),
        "f(Xa)": format_6(fxa),
        "f(Xb)": format_6(fxb),
        "Relative Error (%)": "N/A"
    })

    previous_xb = xb

    for iteration in range(2, max_iter + 1):

        diff_f = fxb - fxa

        if abs(diff_f) < 1e-12:
            return None, "Error: Division by zero."

        xn = xb - (fxb * (xb - xa)) / diff_f

        xa = xb
        xb = xn

        fxa = f(xa)
        fxb = f(xb)

        error_percent = abs((xb - previous_xb) / xb) * 100

        row = {
            "Iteration": iteration,
            "Xa": format_6(xa),
            "Xb": format_6(xb),
            "f(Xa)": format_6(fxa),
            "f(Xb)": format_6(fxb),
            "Relative Error (%)": format_6(error_percent)
        }

        # Video-style final row
        if abs(fxb) < tol:

            next_diff = fxb - fxa

            if abs(next_diff) > 1e-12:

                hidden_xn = xb - (fxb * (xb - xa)) / next_diff

                hidden_error = abs(
                    (hidden_xn - xb) / hidden_xn
                ) * 100

                row["Relative Error (%)"] = format_6(hidden_error)

            steps.append(row)
            return steps, retain_6(xb)

        steps.append(row)

        previous_xb = xb

    return steps, retain_6(xb)
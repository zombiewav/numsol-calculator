def regula_falsi_method(f, xL, xR, tol, max_iter):
    xL = round(float(xL), 6)
    xR = round(float(xR), 6)
    tol = float(tol)

    fxL = round(float(f(xL)), 6)
    fxR = round(float(f(xR)), 6)

    if abs(fxL) < tol:
        steps = [{
            "Iteration no": 1,
            "xL": f"{xL:.6f}",
            "xR": f"{xR:.6f}",
            "xN": f"{xL:.6f}",
            "f(xL)": f"{fxL:.6f}",
            "f(xR)": f"{fxR:.6f}",
            "f(xN)": f"{fxL:.6f}"
        }]
        return steps, xL

    if abs(fxR) < tol:
        steps = [{
            "Iteration no": 1,
            "xL": f"{xL:.6f}",
            "xR": f"{xR:.6f}",
            "xN": f"{xR:.6f}",
            "f(xL)": f"{fxL:.6f}",
            "f(xR)": f"{fxR:.6f}",
            "f(xN)": f"{fxR:.6f}"
        }]
        return steps, xR

    if round(fxL * fxR, 6) > 0:
        return None, "Root not bracketed. f(xL) and f(xR) must have opposite signs."

    steps = []
    x_prev = None

    for i in range(1, max_iter + 1):
        # use only rounded values
        diff_f = round(fxL - fxR, 6)
        if abs(diff_f) < 1e-12:
            return None, "Error: Division by zero."

        xN = round(xR - (fxR * (xL - xR)) / diff_f, 6)
        fxN = round(float(f(xN)), 6)

        steps.append({
            "Iteration no": i,
            "xL": f"{xL:.6f}",
            "xR": f"{xR:.6f}",
            "xN": f"{xN:.6f}",
            "f(xL)": f"{fxL:.6f}",
            "f(xR)": f"{fxR:.6f}",
            "f(xN)": f"{fxN:.6f}",
        })

        # stopping conditions based on rounded values
        if abs(fxN) < tol:
            return steps, xN

        if x_prev is not None:
            error = round(abs(xN - x_prev), 6)
            if error < tol:
                return steps, xN

        # bracket update using rounded values
        if round(fxL * fxN, 6) < 0:
            xR = xN
            fxR = fxN
        else:
            xL = xN
            fxL = fxN

        x_prev = xN

    return steps, xN
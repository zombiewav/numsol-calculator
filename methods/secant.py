def secant_method(f, xa, xb, tol, max_iter):
    steps = []

    xa = round(float(xa), 6)
    xb = round(float(xb), 6)
    tol = float(tol)

    for i in range(1, max_iter + 1):
        fxa = round(float(f(xa)), 6)
        fxb = round(float(f(xb)), 6)

        if abs(fxb - fxa) < 1e-12:
            return None, "Error: Division by zero."

        # compute using rounded values only
        xn = round(xb - (fxb * (xb - xa)) / (fxb - fxa), 6)
        fxn = round(float(f(xn)), 6)

        # error must be based on current xb before update
        error = round(abs(xn - xb), 6)

        steps.append({
            "Iteration": i,
            "Xa": f"{xa:.6f}",
            "Xb": f"{xb:.6f}",
            "f(Xa)": f"{fxa:.6f}",
            "f(Xb)": f"{fxb:.6f}",
            "Error": f"{error:.6f}"
        })

        if error < tol or abs(fxn) < tol:
            return steps, xn

        # update using rounded values only
        xa = xb
        xb = xn

    return steps, xb
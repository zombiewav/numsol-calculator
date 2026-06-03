import numpy as np

from methods.iterative_utils import (
    check_strict_diagonal_dominance,
    evaluate_iteration_equation,
    format_solution,
    parse_augmented_matrix,
    parse_initial_guesses,
    variable_labels,
)


def _format_jacobi_result(values, iteration_count, residuals):
    errors_text = ", ".join(
        f"Error {idx} = {float(residual):.6f}"
        for idx, residual in enumerate(residuals, start=1)
    )
    return (
        f"{format_solution(values)} | "
        f"Iterations = {iteration_count} | "
        f"{errors_text}"
    )


def jacobi_method(matrix_str, tol, max_iter, initial_guess_str=""):
    try:
        matrix_a, vector_b = parse_augmented_matrix(matrix_str)
    except ValueError as e:
        return None, f"Matrix format error: {e}"

    is_dominant, row_idx, diagonal, off_diagonal_sum = check_strict_diagonal_dominance(matrix_a)
    if not is_dominant:
        return None, (
            f"Convergence check failed: row {row_idx} is not diagonally dominant "
            f"(|aii| = {diagonal:.6f}, sum of others = {off_diagonal_sum:.6f})."
        )

    tol = float(tol)
    variable_names = variable_labels(len(vector_b))

    try:
        current_values = parse_initial_guesses(initial_guess_str, len(vector_b))
        current_values = [round(float(v), 6) for v in current_values]
    except ValueError as e:
        return None, str(e)

    steps = []

    residuals = np.abs(np.dot(matrix_a, current_values) - vector_b)

    if all(float(residual) < tol for residual in residuals):
        return [], _format_jacobi_result(current_values, 0, residuals)

    for iteration in range(1, max_iter + 1):
        previous_values = current_values.copy()
        next_values = np.zeros(len(vector_b), dtype=float)

        for row_idx in range(len(vector_b)):
            if abs(matrix_a[row_idx][row_idx]) < 1e-12:
                return None, f"Error: Zero diagonal element at row {row_idx + 1}."

            next_value, _ = evaluate_iteration_equation(
                matrix_a[row_idx],
                vector_b[row_idx],
                previous_values,
                row_idx
            )

            next_value = round(float(next_value), 6)
            next_values[row_idx] = next_value

        step = {"Iteration": iteration}

        for variable_name, value in zip(variable_names, next_values):
            step[variable_name] = f"{value:.6f}"

        residuals = np.abs(np.dot(matrix_a, next_values) - vector_b)

        for eq_idx, residual in enumerate(residuals, start=1):
            step[f"Error {eq_idx}"] = f"{float(residual):.6f}"

        steps.append(step)

        if all(float(residual) < tol for residual in residuals):
            return steps, _format_jacobi_result(next_values, iteration, residuals)

        current_values = [round(float(v), 6) for v in next_values]

    return steps, _format_jacobi_result(current_values, max_iter, residuals)
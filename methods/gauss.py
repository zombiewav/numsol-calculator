import numpy as np

from methods.iterative_utils import (
    evaluate_iteration_equation,
    format_solution,
    parse_augmented_matrix,
    parse_initial_guesses,
    variable_labels,
)


def _format_gauss_seidel_result(values, iteration_count, residuals):
    errors_text = ", ".join(
        f"Error {idx} = {float(residual):.6f}"
        for idx, residual in enumerate(residuals, start=1)
    )
    return (
        f"{format_solution(values)} | "
        f"Iterations = {iteration_count} | "
        f"{errors_text}"
    )


def gauss_seidel_method(matrix_str, tol, max_iter, initial_guess_str=""):
    try:
        matrix_a, vector_b = parse_augmented_matrix(matrix_str)
    except ValueError as e:
        return None, f"Matrix format error: {e}"

    if matrix_a.shape != (3, 3):
        return None, "Gauss-Seidel requires exactly 3 linear equations with 3 variables."

    for row_idx in range(3):
        diagonal = round(abs(float(matrix_a[row_idx][row_idx])), 6)
        off_diagonal_sum = round(
            sum(
                abs(float(matrix_a[row_idx][col_idx]))
                for col_idx in range(3)
                if col_idx != row_idx
            ),
            6
        )

        if diagonal < off_diagonal_sum:
            return None, "System is not diagonally dominant. Gauss-Seidel cannot proceed."

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
        return [], _format_gauss_seidel_result(current_values, 0, residuals)

    for iteration in range(1, max_iter + 1):

        for row_idx in range(len(vector_b)):
            if abs(matrix_a[row_idx][row_idx]) < 1e-12:
                return None, f"Error: Zero diagonal element at row {row_idx + 1}."

            next_value, _ = evaluate_iteration_equation(
                matrix_a[row_idx],
                vector_b[row_idx],
                current_values,
                row_idx
            )

            next_value = round(float(next_value), 6)
            current_values[row_idx] = next_value

        step = {"Iteration": iteration}

        for variable_name, value in zip(variable_names, current_values):
            step[variable_name] = f"{value:.6f}"

        residuals = np.abs(np.dot(matrix_a, current_values) - vector_b)

        for eq_idx, residual in enumerate(residuals, start=1):
            step[f"Error {eq_idx}"] = f"{float(residual):.6f}"

        steps.append(step)

        if all(float(residual) < tol for residual in residuals):
            return steps, _format_gauss_seidel_result(
                current_values,
                iteration,
                residuals
            )

    return steps, _format_gauss_seidel_result(
        current_values,
        max_iter,
        residuals
    )
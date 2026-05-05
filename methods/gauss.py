import numpy as np

from methods.iterative_utils import (
    check_strict_diagonal_dominance,
    evaluate_iteration_equation,
    format_solution,
    parse_augmented_matrix,
    parse_initial_guesses,
    variable_labels,
)


def gauss_seidel_method(matrix_str, tol, max_iter, initial_guess_str=""):
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

    for iteration in range(1, max_iter + 1):
        previous_values = current_values.copy()
        equation_traces = []

        for row_idx in range(len(vector_b)):
            if abs(matrix_a[row_idx][row_idx]) < 1e-12:
                return None, f"Error: Zero diagonal element at row {row_idx + 1}."

            next_value, trace = evaluate_iteration_equation(
                matrix_a[row_idx],
                vector_b[row_idx],
                current_values,
                row_idx
            )

            # enforce rounding before reuse
            next_value = round(float(next_value), 6)
            current_values[row_idx] = next_value

            equation_traces.append(trace)

        # compute error using rounded values only
        max_error = round(
            max(abs(current_values[i] - previous_values[i]) for i in range(len(current_values))),
            6
        )

        step = {"Iteration": iteration}

        for variable_name, value in zip(variable_names, current_values):
            step[variable_name] = f"{value:.6f}"

        for eq_idx, trace in enumerate(equation_traces, start=1):
            step[f"Equation {eq_idx}"] = trace

        steps.append(step)

        if max_error < tol:
            return steps, format_solution(current_values)

    return steps, format_solution(current_values)
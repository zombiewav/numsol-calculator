import ast
import re
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


_PARSE_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def _split_system_rows(text):
    if ";" in text:
        return [row.strip() for row in text.split(";") if row.strip()]
    return [row.strip() for row in text.splitlines() if row.strip()]


def _parse_matrix_rows(text):
    if text.startswith("["):
        raw_matrix = ast.literal_eval(text)
    else:
        rows = _split_system_rows(text)
        raw_matrix = [
            [float(value.strip()) for value in row.split(",")]
            for row in rows
        ]

    matrix = np.array(raw_matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("Matrix must be two-dimensional.")

    row_count, col_count = matrix.shape
    if row_count == 0 or col_count != row_count + 1:
        raise ValueError("Use an augmented matrix with n rows and n+1 columns.")

    return np.round(matrix[:, :-1], 6), np.round(matrix[:, -1], 6)


def _normalize_equation_text(text):
    cleaned = text.replace("^", "**")
    cleaned = re.sub(r"(?<=\d)(?=[A-Za-z(])", "*", cleaned)
    return cleaned


def _parse_equation_rows(text):
    rows = _split_system_rows(text)
    if not rows or not all("=" in row for row in rows):
        raise ValueError("Each equation must include '='.")

    equations = []
    symbols = set()

    for row in rows:
        left_text, right_text = row.split("=", 1)
        left_expr = parse_expr(_normalize_equation_text(left_text), transformations=_PARSE_TRANSFORMS)
        right_expr = parse_expr(_normalize_equation_text(right_text), transformations=_PARSE_TRANSFORMS)
        equations.append(sp.Eq(left_expr, right_expr))
        symbols.update(left_expr.free_symbols)
        symbols.update(right_expr.free_symbols)

    if not symbols:
        raise ValueError("No variables found in the equations.")

    ordered_symbols = sorted(symbols, key=lambda sym: sym.name)
    coeff_matrix, rhs_matrix = sp.linear_eq_to_matrix(equations, ordered_symbols)

    matrix_a = np.array(coeff_matrix.tolist(), dtype=float)
    vector_b = np.array(rhs_matrix, dtype=float).reshape(-1)

    if matrix_a.shape[0] == 0 or matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError("Use the same number of linear equations and variables.")

    return np.round(matrix_a, 6), np.round(vector_b, 6)


def parse_augmented_matrix(matrix_str):
    text = matrix_str.strip()
    if not text:
        raise ValueError("Enter an augmented matrix or equations.")

    try:
        if "=" in text:
            return _parse_equation_rows(text)
        return _parse_matrix_rows(text)
    except Exception as e:
        raise ValueError(
            "Invalid system format. Use 'a,b,c,d; ...', [[...], [...]], or equations like "
            "'10x-y+2z=6; -x+11y-z=25; 2x-y+10z=-11'."
        ) from e


def parse_initial_guesses(initial_guess_str, variable_count):
    text = initial_guess_str.strip() if initial_guess_str is not None else ""
    if not text:
        return np.zeros(variable_count, dtype=float)

    cleaned = text.strip().strip("()[]")
    try:
        guess_values = [
            round(float(value.strip()), 6)
            for value in cleaned.split(",")
            if value.strip()
        ]
    except Exception as e:
        raise ValueError(
            "Invalid initial guesses. Use comma-separated values like 0,0,0."
        ) from e

    if len(guess_values) != variable_count:
        raise ValueError(
            f"Enter exactly {variable_count} initial guess values."
        )

    return np.array(guess_values, dtype=float)


def check_strict_diagonal_dominance(matrix_a):
    for row_idx in range(len(matrix_a)):
        diagonal = round(abs(float(matrix_a[row_idx][row_idx])), 6)
        off_diagonal_sum = round(
            sum(
                abs(float(matrix_a[row_idx][col_idx]))
                for col_idx in range(len(matrix_a[row_idx]))
                if col_idx != row_idx
            ),
            6
        )
        if diagonal <= off_diagonal_sum:
            return False, row_idx + 1, diagonal, off_diagonal_sum
    return True, None, None, None


def variable_labels(size):
    if size == 1:
        return ["x"]
    if size == 2:
        return ["x", "y"]
    if size == 3:
        return ["x", "y", "z"]
    return [f"x{i + 1}" for i in range(size)]


def format_solution(values):
    labels = variable_labels(len(values))
    return ", ".join(
        f"{label} = {round(float(value), 6):.6f}"
        for label, value in zip(labels, values)
    )


def evaluate_iteration_equation(coeff_row, rhs, values_used, solve_index):
    diagonal = round(float(coeff_row[solve_index]), 6)
    sigma = 0.0
    terms = []

    for col_idx, coefficient in enumerate(coeff_row):
        if col_idx == solve_index:
            continue
        coefficient = round(float(coefficient), 6)
        used_value = round(float(values_used[col_idx]), 6)
        term = round(coefficient * used_value, 6)
        sigma = round(sigma + term, 6)
        terms.append(f"({coefficient:.6f}*{used_value:.6f})")

    rhs = round(float(rhs), 6)  # FIXED
    numerator = round(rhs - sigma, 6)
    result = round(numerator / diagonal, 6)

    terms_text = " + ".join(terms) if terms else "0.000000"
    trace = f"({rhs:.6f} - ({terms_text})) / {diagonal:.6f} = {result:.6f}"

    return result, trace
from main import *
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# ========================== ТЕСТЫ ===========================
# ============================================================

def test_create_vector():
    v = create_vector()
    assert isinstance(v, np.ndarray)
    assert v.shape == (10,)
    assert np.array_equal(v, np.arange(10))


def test_create_matrix():
    m = create_matrix()
    assert isinstance(m, np.ndarray)
    assert m.shape == (5, 5)
    assert np.all((m >= 0) & (m < 1))


def test_reshape_vector():
    v = np.arange(10)
    reshaped = reshape_vector(v)
    assert reshaped.shape == (2, 5)
    assert reshaped[0, 0] == 0
    assert reshaped[1, 4] == 9


def test_vector_add():
    assert np.array_equal(
        vector_add(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([5, 7, 9])
    )
    assert np.array_equal(
        vector_add(np.array([0, 1]), np.array([1, 1])),
        np.array([1, 2])
    )


def test_scalar_multiply():
    assert np.array_equal(
        scalar_multiply(np.array([1, 2, 3]), 2),
        np.array([2, 4, 6])
    )


def test_elementwise_multiply():
    assert np.array_equal(
        elementwise_multiply(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([4, 10, 18])
    )


def test_dot_product():
    assert dot_product(np.array([1, 2, 3]), np.array([4, 5, 6])) == 32
    assert dot_product(np.array([2, 0]), np.array([3, 5])) == 6


def test_matrix_multiply():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[2, 0], [1, 2]])
    assert np.array_equal(matrix_multiply(A, B), A @ B)


def test_matrix_determinant():
    A = np.array([[1, 2], [3, 4]])
    assert round(matrix_determinant(A), 5) == -2.0


def test_matrix_inverse():
    A = np.array([[1, 2], [3, 4]])
    invA = matrix_inverse(A)
    assert np.allclose(A @ invA, np.eye(2))


def test_solve_linear_system():
    A = np.array([[2, 1], [1, 3]])
    b = np.array([1, 2])
    x = solve_linear_system(A, b)
    assert np.allclose(A @ x, b)


def test_load_dataset():
    test_data = "math,physics,informatics\n78,81,90\n85,89,88"
    with open("test_data.csv", "w") as f:
        f.write(test_data)
    try:
        data = load_dataset("test_data.csv")
        assert data.shape == (2, 3)
        assert np.array_equal(data[0], [78, 81, 90])
    finally:
        os.remove("test_data.csv")


def test_statistical_analysis():
    data = np.array([10, 20, 30])
    result = statistical_analysis(data)
    assert result["mean"] == 20
    assert result["min"] == 10
    assert result["max"] == 30


def test_normalization():
    data = np.array([0, 5, 10])
    norm = normalize_data(data)
    assert np.allclose(norm, np.array([0, 0.5, 1]))


def test_plot_histogram():
    data = np.array([1, 2, 3, 4, 5])
    plot_histogram(data)


def test_plot_heatmap():
    matrix = np.array([[1, 0.5], [0.5, 1]])
    plot_heatmap(matrix)


def test_plot_line():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_line(x, y)


if __name__ == "__main__":
    print("Запустите python -m pytest -v test.py для проверки лабораторной работы.")

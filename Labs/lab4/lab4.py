import timeit
import matplotlib.pyplot as plt
import random


def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=50, repeat=20)
    return min(times)



def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(10, 1001, 50))

    res_recursive = []
    res_iterative = []

    for n in test_data:
      res_recursive.append(benchmark(fact_recursive, n))
      res_iterative.append(benchmark(fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()
    
    # Вывод времени для конкретных значений n
    test_values = [100, 500, 700]
    print("Время выполнения для рекурсивного факториала:")
    for n in test_values:
        time_recursive = benchmark(fact_recursive, n)
        print(f"n = {n}: {time_recursive:.6f} сек")
    
    print("\nВремя выполнения для итеративного факториала:")
    for n in test_values:
        time_iterative = benchmark(fact_iterative, n)
        print(f"n = {n}: {time_iterative:.6f} сек")


if __name__ == "__main__":
    main()
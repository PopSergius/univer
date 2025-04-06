import sys
import time
import math


def prime_factorize(n):
    """
    Розкладає число n на прості множники.
    Повертає список пар (простий множник, степінь)
    """
    factors = []

    # Обробляємо випадок, коли число ділиться на 2
    if n % 2 == 0:
        count = 0
        while n % 2 == 0:
            count += 1
            n //= 2
        factors.append((2, count))

    # Перевіряємо непарні числа до sqrt(n)
    i = 3
    while i <= math.isqrt(n):
        if n % i == 0:
            count = 0
            while n % i == 0:
                count += 1
                n //= i
            factors.append((i, count))
        i += 2

    # Якщо залишилось просте число більше за sqrt(n)
    if n > 1:
        factors.append((n, 1))

    return factors


def factorize_large_number(n):
    """
    Розкладає великі числа на прості множники з оптимізацією для великих чисел.
    """
    print(f"Початок факторизації числа {n}...")
    start_time = time.time()

    factors = prime_factorize(n)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Факторизація завершена за {elapsed_time:.6f} секунд")
    return factors


def format_factorization(factors):
    """
    Форматує результат факторизації у вигляді добутку простих множників у степенях.
    """
    terms = []
    for factor, power in factors:
        if power == 1:
            terms.append(f"{factor}")
        else:
            terms.append(f"{factor}^{power}")

    return " * ".join(terms)


def print_factorization(n, factors):
    """
    Виводить результат факторизації у зручному форматі.
    """
    formatted_result = format_factorization(factors)
    print(f"{n} = {formatted_result}")


def main():
    # a) Довільне число
    while True:
        try:
            user_number = int(
                input(
                    "Введіть довільне число для факторизації (або 0 для продовження): "
                )
            )
            if user_number == 0:
                break
            if user_number < 0:
                print("Введіть додатнє число!")
                continue

            factors = prime_factorize(user_number)
            print_factorization(user_number, factors)
            print()
        except ValueError:
            print("Помилка! Введіть коректне ціле число.")

    # б) Максимальне число типу long integer
    # В Python 3 тип int не має обмежень, але для сумісності з C/C++ використаємо 2^63-1
    max_long = 2**63 - 1  # 9,223,372,036,854,775,807
    print("\nб) Максимальне число типу long integer в системах C/C++:")
    print(f"Значення: {max_long}")
    print("Початок факторизації...")

    factors = factorize_large_number(max_long)
    print_factorization(max_long, factors)

    # в) Максимальне число типу unsigned long long
    # В Python 3 тип int не має обмежень, але для сумісності з C/C++ використаємо 2^64-1
    max_ulonglong = 2**64 - 1  # 18,446,744,073,709,551,615
    print("\nв) Максимальне число типу unsigned long long в системах C/C++:")
    print(f"Значення: {max_ulonglong}")
    print("Початок факторизації...")

    factors = factorize_large_number(max_ulonglong)
    print_factorization(max_ulonglong, factors)


if __name__ == "__main__":
    print("Програма для розкладання чисел на прості множники\n")
    main()

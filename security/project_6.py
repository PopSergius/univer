import hashlib
import random
import math

# ========== 6.1. Створення власної хеш-функції ==========


def custom_hash(message, block_size=8):
    """
    Створює хеш за допомогою побітового XOR кожного блоку повідомлення

    Args:
        message (str): Повідомлення для хешування
        block_size (int): Розмір блоку в бітах

    Returns:
        str: Хеш-код у вигляді рядка бітів
    """
    # Перетворення повідомлення в послідовність бітів
    message_bytes = message.encode("utf-8")
    bits = "".join(format(byte, "08b") for byte in message_bytes)

    # Доповнення бітів, щоб довжина була кратна block_size
    padding = (
        block_size - (len(bits) % block_size) if len(bits) % block_size != 0 else 0
    )
    bits = bits + "0" * padding

    # Розбиття на блоки
    blocks = [bits[i : i + block_size] for i in range(0, len(bits), block_size)]

    # Ініціалізація хешу
    hash_value = ["0"] * block_size

    # Обчислення хешу за допомогою XOR
    for block in blocks:
        for i in range(block_size):
            hash_value[i] = str(int(hash_value[i]) ^ int(block[i]))

    return "".join(hash_value)


def verify_message_integrity(message, hash_function=custom_hash):
    """
    Перевіряє цілісність повідомлення за допомогою хеш-функції

    Args:
        message (str): Повідомлення для перевірки
        hash_function (function): Функція для обчислення хешу

    Returns:
        tuple: (оригінальний хеш, змінене повідомлення, новий хеш, результат перевірки)
    """
    # Обчислення хешу оригінального повідомлення
    original_hash = hash_function(message)

    # Внесення змін у повідомлення (заміна 1-2 символів)
    modified_message = list(message)

    # Визначення позицій для зміни (1-2 символи)
    positions_to_modify = random.sample(range(len(message)), min(2, len(message)))

    for pos in positions_to_modify:
        # Заміна символу на інший випадковий символ
        modified_message[pos] = chr(
            (ord(modified_message[pos]) + random.randint(1, 25)) % 128
        )

    modified_message = "".join(modified_message)

    # Обчислення хешу зміненого повідомлення
    modified_hash = hash_function(modified_message)

    # Перевірка цілісності
    integrity_check = original_hash == modified_hash

    return original_hash, modified_message, modified_hash, integrity_check


# ========== 6.2. Отримання хешу повідомлення стандартними функціями ==========


def hash_with_standard_functions(message):
    """
    Обчислює хеш повідомлення за допомогою SHA-256 та MD5

    Args:
        message (str): Повідомлення для хешування

    Returns:
        tuple: (SHA-256 хеш, MD5 хеш)
    """
    # Хешування SHA-256
    sha256_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()

    # Хешування MD5
    md5_hash = hashlib.md5(message.encode("utf-8")).hexdigest()

    return sha256_hash, md5_hash


def verify_with_standard_functions(message):
    """
    Перевіряє цілісність повідомлення за допомогою стандартних хеш-функцій

    Args:
        message (str): Повідомлення для перевірки

    Returns:
        tuple: (результати для SHA-256, результати для MD5)
    """
    # Обчислення хешів оригінального повідомлення
    original_sha256, original_md5 = hash_with_standard_functions(message)

    # Внесення змін у повідомлення (заміна 1-2 символів)
    modified_message = list(message)

    # Визначення позицій для зміни (1-2 символи)
    positions_to_modify = random.sample(range(len(message)), min(2, len(message)))

    for pos in positions_to_modify:
        # Заміна символу на інший випадковий символ
        modified_message[pos] = chr(
            (ord(modified_message[pos]) + random.randint(1, 25)) % 128
        )

    modified_message = "".join(modified_message)

    # Обчислення хешів зміненого повідомлення
    modified_sha256, modified_md5 = hash_with_standard_functions(modified_message)

    # Перевірка цілісності
    sha256_check = original_sha256 == modified_sha256
    md5_check = original_md5 == modified_md5

    return (original_sha256, modified_message, modified_sha256, sha256_check), (
        original_md5,
        modified_message,
        modified_md5,
        md5_check,
    )


# ========== 6.3. Створення ЕЦП (оптимізований варіант) ==========


def miller_rabin_test(n, k=40):
    """
    Тест Міллера-Рабіна на простоту числа

    Args:
        n (int): Число для перевірки
        k (int): Кількість ітерацій (більше значення = більша надійність)

    Returns:
        bool: True, якщо число ймовірно просте, False інакше
    """
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Представимо n - 1 як 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Проведемо k тестів
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime_number(bits):
    """
    Генерація простого числа з заданою кількістю бітів

    Args:
        bits (int): Кількість бітів у числі

    Returns:
        int: Просте число
    """
    while True:
        # Генеруємо випадкове число з заданою кількістю бітів
        candidate = random.getrandbits(bits)
        # Встановлюємо найстарший біт щоб гарантувати потрібну довжину
        candidate |= 1 << bits - 1
        # Встановлюємо найменший біт щоб гарантувати непарність
        candidate |= 1

        # Перевіряємо чи число просте
        if miller_rabin_test(candidate):
            return candidate


def gcd(a, b):
    """Найбільший спільний дільник"""
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    """Обчислення мультиплікативного оберненого по модулю phi"""

    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return (gcd, y - (b // a) * x, x)

    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception("Модульний обернений не існує")
    else:
        return x % phi


def generate_rsa_keys(key_size=512):  # Зменшено розмір ключа для швидшої роботи
    """
    Генерація ключів RSA

    Args:
        key_size (int): Розмір ключа в бітах

    Returns:
        tuple: ((e, n), (d, n)) - публічний та приватний ключі
    """
    # Генеруємо два великих простих числа
    print("Генерація простого числа p...")
    p = generate_prime_number(key_size // 2)
    print("Генерація простого числа q...")
    q = generate_prime_number(key_size // 2)

    # Обчислюємо модуль n = p * q
    n = p * q

    # Обчислюємо функцію Ейлера phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)

    # Вибираємо відкритий ключ e, такий що 1 < e < phi та gcd(e, phi) = 1
    e = 65537  # Стандартне значення для e (просте число Ферма)
    if gcd(e, phi) != 1:
        # У рідкісних випадках, коли 65537 не підходить, шукаємо інше значення
        for candidate in [65537, 257, 17, 5, 3]:
            if gcd(candidate, phi) == 1:
                e = candidate
                break

    # Обчислюємо закритий ключ d, такий що (d*e) % phi = 1
    print("Обчислення закритого ключа d...")
    d = mod_inverse(e, phi)

    return (e, n), (d, n)


def rsa_sign(message, private_key):
    """
    Створення цифрового підпису за допомогою RSA

    Args:
        message (str): Повідомлення для підпису
        private_key (tuple): Приватний ключ (d, n)

    Returns:
        int: Цифровий підпис
    """
    # Обчислюємо хеш повідомлення
    message_hash = int(hashlib.sha256(message.encode("utf-8")).hexdigest(), 16)

    # Створюємо підпис: s = (hash^d) mod n
    d, n = private_key
    signature = pow(message_hash, d, n)

    return signature


def rsa_verify(message, signature, public_key):
    """
    Верифікація цифрового підпису за допомогою RSA

    Args:
        message (str): Повідомлення для перевірки
        signature (int): Цифровий підпис
        public_key (tuple): Публічний ключ (e, n)

    Returns:
        bool: Результат верифікації
    """
    # Обчислюємо хеш повідомлення
    message_hash = int(hashlib.sha256(message.encode("utf-8")).hexdigest(), 16)

    # Відновлюємо оригінальний хеш з підпису: v = (s^e) mod n
    e, n = public_key
    verification_hash = pow(signature, e, n)

    # Перевіряємо, чи співпадає відновлений хеш з оригінальним
    return verification_hash == message_hash


def test_rsa_signature(message):
    """
    Тестування RSA цифрового підпису

    Args:
        message (str): Повідомлення для підпису

    Returns:
        tuple: (результат верифікації оригінального повідомлення,
                результат верифікації зміненого повідомлення)
    """
    # Генеруємо ключі
    print("Генерація ключів RSA...")
    public_key, private_key = generate_rsa_keys()

    # Створюємо підпис
    print("Створення цифрового підпису...")
    signature = rsa_sign(message, private_key)

    # Верифікація оригінального повідомлення
    print("Верифікація оригінального повідомлення...")
    original_verification = rsa_verify(message, signature, public_key)

    # Внесення змін у повідомлення
    modified_message = list(message)

    # Визначення позицій для зміни (1-2 символи)
    positions_to_modify = random.sample(range(len(message)), min(2, len(message)))

    for pos in positions_to_modify:
        # Заміна символу на інший випадковий символ
        modified_message[pos] = chr(
            (ord(modified_message[pos]) + random.randint(1, 25)) % 128
        )

    modified_message = "".join(modified_message)

    # Верифікація зміненого повідомлення
    print("Верифікація зміненого повідомлення...")
    modified_verification = rsa_verify(modified_message, signature, public_key)

    return original_verification, modified_message, modified_verification


# ========== Основна програма ==========


def main():
    print("===== ПРОГРАМА ДЛЯ РОБОТИ З ХЕШ-ФУНКЦІЯМИ ТА ЦИФРОВИМ ПІДПИСОМ =====\n")

    # Введення повідомлення
    message = input("Введіть повідомлення для хешування та підпису: ")

    print("\n===== 6.1. Власна хеш-функція =====")

    # Тестування власної хеш-функції
    original_hash, modified_message, modified_hash, integrity_check = (
        verify_message_integrity(message)
    )

    print(f"Оригінальне повідомлення: '{message}'")
    print(f"Оригінальний хеш: {original_hash}")
    print(f"Змінене повідомлення: '{modified_message}'")
    print(f"Хеш зміненого повідомлення: {modified_hash}")
    print(
        f"Результат перевірки цілісності: {'FAIL - повідомлення змінено' if not integrity_check else 'OK - повідомлення не змінено'}"
    )

    print("\n===== 6.2. Стандартні хеш-функції =====")

    # Тестування стандартних хеш-функцій
    sha256_results, md5_results = verify_with_standard_functions(message)

    print("\nSHA-256:")
    print(f"Оригінальний хеш: {sha256_results[0]}")
    print(f"Змінене повідомлення: '{sha256_results[1]}'")
    print(f"Хеш зміненого повідомлення: {sha256_results[2]}")
    print(
        f"Результат перевірки цілісності: {'FAIL - повідомлення змінено' if not sha256_results[3] else 'OK - повідомлення не змінено'}"
    )

    print("\nMD5:")
    print(f"Оригінальний хеш: {md5_results[0]}")
    print(f"Змінене повідомлення: '{md5_results[1]}'")
    print(f"Хеш зміненого повідомлення: {md5_results[2]}")
    print(
        f"Результат перевірки цілісності: {'FAIL - повідомлення змінено' if not md5_results[3] else 'OK - повідомлення не змінено'}"
    )

    print("\n===== 6.3. Електронний цифровий підпис RSA =====")

    # Тестування RSA цифрового підпису
    original_verification, modified_message_rsa, modified_verification = (
        test_rsa_signature(message)
    )

    print(f"Оригінальне повідомлення: '{message}'")
    print(
        f"Результат верифікації оригінального повідомлення: {'OK - підпис верифіковано' if original_verification else 'FAIL - підпис не верифіковано'}"
    )
    print(f"Змінене повідомлення: '{modified_message_rsa}'")
    print(
        f"Результат верифікації зміненого повідомлення: {'OK - підпис верифіковано' if modified_verification else 'FAIL - підпис не верифіковано'}"
    )


if __name__ == "__main__":
    main()

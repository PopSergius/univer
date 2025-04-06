# -*- coding: utf-8 -*-
import os


def clear_screen():
    """Функція для очищення консолі"""
    os.system("cls" if os.name == "nt" else "clear")


def display_menu():
    """Відображення головного меню"""
    clear_screen()
    print("\n===== ПРОГРАМА ПЕРЕВІРКИ ЦІЛІСНОСТІ ДАНИХ =====\n")
    print("1. Метод контрольних сум (8-бітова)")
    print("2. Посимвольний контроль парності")
    print("3. Поблочний контроль парності (поздовжній)")
    print("0. Вихід")
    return input("\nВиберіть опцію (0-3): ")


def calculate_checksum(message):
    """Розрахунок 8-бітової контрольної суми як суми байт"""
    checksum = 0
    for byte in message.encode("utf-8"):
        checksum = (checksum + byte) & 0xFF  # 8-бітова сума (обмеження до 255)
    return checksum


def test_checksum():
    """Функція для тестування методу контрольних сум"""
    clear_screen()
    print("\n===== МЕТОД КОНТРОЛЬНИХ СУМ =====\n")

    # Введення повідомлення
    message = input("Введіть повідомлення: ")

    # Розрахунок контрольної суми
    checksum = calculate_checksum(message)
    print(f"Контрольна сума: {checksum} (0x{checksum:02X})")

    # Модифікація повідомлення
    while True:
        print("\nОпції:")
        print("1. Змінити повідомлення")
        print("2. Повернутися до головного меню")
        choice = input("\nВиберіть опцію (1-2): ")

        if choice == "1":
            new_message = input("Введіть модифіковане повідомлення: ")
            new_checksum = calculate_checksum(new_message)
            print(f"Нова контрольна сума: {new_checksum} (0x{new_checksum:02X})")

            if checksum == new_checksum:
                print("Контрольні суми співпадають. Зміни не виявлено.")
            else:
                print("Контрольні суми відрізняються. Виявлено зміни в повідомленні!")

            # Аналіз змін побайтово
            print("\nАналіз змін побайтово:")
            orig_bytes = message.encode("utf-8")
            new_bytes = new_message.encode("utf-8")

            print(
                "Оригінальне повідомлення (байти):",
                " ".join(f"{b:02X}" for b in orig_bytes),
            )
            print(
                "Модифіковане повідомлення (байти):",
                " ".join(f"{b:02X}" for b in new_bytes),
            )

        elif choice == "2":
            return
        else:
            print("Невірний вибір. Спробуйте ще раз.")


def check_parity(byte, even_parity=True):
    """
    Перевірка біта парності
    even_parity=True - перевірка на парність
    even_parity=False - перевірка на непарність
    """
    # Підрахунок кількості одиниць в байті
    count_ones = bin(byte).count("1")

    if even_parity:
        # Для парності: якщо кількість одиниць парна, то біт парності = 0
        parity_bit = 0 if count_ones % 2 == 0 else 1
    else:
        # Для непарності: якщо кількість одиниць непарна, то біт парності = 0
        parity_bit = 0 if count_ones % 2 == 1 else 1

    return parity_bit


def add_parity_bit(byte, even_parity=True):
    """Додає біт парності до байту (в старший біт)"""
    parity_bit = check_parity(byte, even_parity)
    # Встановлюємо біт парності в старший біт
    return (byte & 0x7F) | (parity_bit << 7)


def verify_parity(byte, even_parity=True):
    """Перевіряє чи коректний біт парності в байті"""
    # Отримуємо встановлений біт парності
    set_parity = (byte & 0x80) >> 7
    # Обчислюємо очікуваний біт парності для нижніх 7 біт
    expected_parity = check_parity(byte & 0x7F, even_parity)
    return set_parity == expected_parity


def test_char_parity():
    """Функція для тестування посимвольного контролю парності"""
    clear_screen()
    print("\n===== ПОСИМВОЛЬНИЙ КОНТРОЛЬ ПАРНОСТІ =====\n")

    # Вибір варіанту перевірки
    print("Варіанти перевірки:")
    print("1. Перевірка на непарність")
    print("2. Перевірка на парність")
    parity_choice = input("\nВиберіть варіант (1-2): ")

    even_parity = True if parity_choice == "2" else False
    parity_type = "парність" if even_parity else "непарність"

    # Введення повідомлення
    message = input("\nВведіть повідомлення: ")
    message_bytes = message.encode("utf-8")

    # Додаємо біт парності до кожного байту
    protected_bytes = []
    for byte in message_bytes:
        protected_byte = add_parity_bit(byte, even_parity)
        protected_bytes.append(protected_byte)

    print(f"\nДодано біти {parity_type} до кожного символу.")
    print("Оригінальні байти:", " ".join(f"{b:08b}" for b in message_bytes))
    print(
        f"Байти з бітом {parity_type}:", " ".join(f"{b:08b}" for b in protected_bytes)
    )

    # Симуляція помилки передачі
    while True:
        print("\nОпції:")
        print("1. Симулювати помилку в передачі (змінити один біт)")
        print("2. Перевірити цілісність даних")
        print("3. Повернутися до головного меню")
        choice = input("\nВиберіть опцію (1-3): ")

        if choice == "1":
            try:
                position = int(
                    input("Введіть позицію байту для модифікації (починається з 0): ")
                )
                bit_pos = int(input("Введіть позицію біту для інвертування (0-7): "))

                if 0 <= position < len(protected_bytes) and 0 <= bit_pos <= 7:
                    # Інвертуємо вказаний біт
                    protected_bytes[position] ^= 1 << bit_pos
                    print(f"Біт {bit_pos} в байті {position} було інвертовано.")
                    print(
                        "Модифіковані байти:",
                        " ".join(f"{b:08b}" for b in protected_bytes),
                    )
                else:
                    print("Невірні позиції. Перевірте діапазон.")
            except ValueError:
                print("Введіть коректні числові значення.")

        elif choice == "2":
            print("\nПеревірка цілісності даних:")
            all_ok = True
            for i, byte in enumerate(protected_bytes):
                if verify_parity(byte, even_parity):
                    print(f"Байт {i}: OK")
                else:
                    print(f"Байт {i}: ПОМИЛКА - порушення контролю {parity_type}")
                    all_ok = False

            if all_ok:
                print("\nУсі дані цілісні. Помилок не виявлено.")
            else:
                print("\nВиявлено помилки в даних!")

        elif choice == "3":
            return
        else:
            print("Невірний вибір. Спробуйте ще раз.")


def calculate_block_parity(data, block_size=8, even_parity=True):
    """
    Розрахунок поблочного (поздовжнього) контролю парності
    Повертає контрольну послідовність для перевірки цілісності
    """
    # Створення списку для зберігання контрольних бітів
    parity_bits = []

    # Для кожної позиції біту в блоці
    for bit_pos in range(block_size):
        count_ones = 0

        # Рахуємо кількість одиниць в даній позиції для кожного байту
        for byte in data:
            if byte & (1 << bit_pos):
                count_ones += 1

        # Визначаємо біт парності для даної позиції
        if even_parity:
            # Для парності
            parity_bit = 0 if count_ones % 2 == 0 else 1
        else:
            # Для непарності
            parity_bit = 0 if count_ones % 2 == 1 else 1

        # Додаємо біт до контрольної послідовності
        if parity_bit:
            parity_bits.append(1 << bit_pos)
        else:
            parity_bits.append(0)

    # Обчислюємо один байт контрольної суми
    checksum = 0
    for bit_value in parity_bits:
        checksum |= bit_value

    return checksum


def test_block_parity():
    """Функція для тестування поблочного контролю парності"""
    clear_screen()
    print("\n===== ПОБЛОЧНИЙ КОНТРОЛЬ ПАРНОСТІ (ПОЗДОВЖНІЙ) =====\n")

    # Завжди перевірка на непарність для цього завдання
    even_parity = False

    # Введення повідомлення
    message = input("Введіть повідомлення: ")
    message_bytes = message.encode("utf-8")

    # Розрахунок контрольної послідовності
    parity_checksum = calculate_block_parity(message_bytes, even_parity=even_parity)

    print(f"\nДані: {' '.join(f'{b:08b}' for b in message_bytes)}")
    print(f"Контрольна послідовність (непарність): {parity_checksum:08b}")

    # Симуляція помилки передачі
    while True:
        print("\nОпції:")
        print("1. Симулювати помилку в передачі (змінити один біт)")
        print("2. Перевірити цілісність даних")
        print("3. Повернутися до головного меню")
        choice = input("\nВиберіть опцію (1-3): ")

        if choice == "1":
            try:
                position = int(
                    input("Введіть позицію байту для модифікації (починається з 0): ")
                )
                bit_pos = int(input("Введіть позицію біту для інвертування (0-7): "))

                if 0 <= position < len(message_bytes) and 0 <= bit_pos <= 7:
                    # Створюємо копію даних для модифікації
                    modified_bytes = bytearray(message_bytes)
                    # Інвертуємо вказаний біт
                    modified_bytes[position] ^= 1 << bit_pos
                    print(f"Біт {bit_pos} в байті {position} було інвертовано.")
                    print(
                        "Модифіковані дані:",
                        " ".join(f"{b:08b}" for b in modified_bytes),
                    )

                    # Обчислюємо нову контрольну послідовність
                    new_parity_checksum = calculate_block_parity(
                        modified_bytes, even_parity=even_parity
                    )
                    print(f"Нова контрольна послідовність: {new_parity_checksum:08b}")

                    # Оновлюємо дані
                    message_bytes = modified_bytes
                else:
                    print("Невірні позиції. Перевірте діапазон.")
            except ValueError:
                print("Введіть коректні числові значення.")

        elif choice == "2":
            print("\nПеревірка цілісності даних:")

            # Розрахунок нової контрольної послідовності
            current_checksum = calculate_block_parity(
                message_bytes, even_parity=even_parity
            )

            if current_checksum == parity_checksum:
                print("Дані цілісні. Помилок не виявлено.")
            else:
                print("Виявлено помилки в даних!")
                print(f"Оригінальна контрольна послідовність: {parity_checksum:08b}")
                print(f"Поточна контрольна послідовність:     {current_checksum:08b}")

                # Визначення позицій, де відбулися зміни
                diff = parity_checksum ^ current_checksum
                print(f"Різниця (XOR):                         {diff:08b}")

                if diff:
                    print("Змінені біти в позиціях:", end=" ")
                    for i in range(8):
                        if diff & (1 << i):
                            print(i, end=" ")
                    print()

        elif choice == "3":
            return
        else:
            print("Невірний вибір. Спробуйте ще раз.")


def main():
    """Головна функція програми"""
    while True:
        choice = display_menu()

        if choice == "1":
            test_checksum()
        elif choice == "2":
            test_char_parity()
        elif choice == "3":
            test_block_parity()
        elif choice == "0":
            print("\nДякуємо за використання програми. До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

        input("\nНатисніть Enter для продовження...")


if __name__ == "__main__":
    main()

import random

BASE = 10**4  # Block base (10000) — each block stores up to 4 digits


# Генерація випадкового багаторозрядного числа заданої довжини
def generate_big_number(digits):
    num_str = str(random.randint(1, 9))  # перший розряд — не нуль
    while len(num_str) < digits:
        num_str += str(random.randint(0, 9))
    return num_str


# Перетворення рядка числа на список блоків (від кінця)
def string_to_blocks(number_str):
    blocks = []
    while number_str:
        blocks.insert(0, int(number_str[-4:]))
        number_str = number_str[:-4]
    return blocks


# Додавання двох багаторозрядних чисел у вигляді блоків
def add_big_numbers(a_blocks, b_blocks):
    max_len = max(len(a_blocks), len(b_blocks))
    a_blocks = [0] * (max_len - len(a_blocks)) + a_blocks
    b_blocks = [0] * (max_len - len(b_blocks)) + b_blocks

    result = []
    carry = 0

    # Adding block by block from right to left
    for i in range(max_len - 1, -1, -1):
        total = a_blocks[i] + b_blocks[i] + carry
        result.insert(0, total % BASE)
        carry = total // BASE

    if carry:
        result.insert(0, carry)

    return result


# Віднімання двох багаторозрядних чисел у вигляді блоків (a >= b)
def subtract_big_numbers(a_blocks, b_blocks):
    max_len = max(len(a_blocks), len(b_blocks))
    a_blocks = [0] * (max_len - len(a_blocks)) + a_blocks
    b_blocks = [0] * (max_len - len(b_blocks)) + b_blocks

    result = []
    borrow = 0

    # Subtracting block by block from right to left
    for i in range(max_len - 1, -1, -1):
        diff = a_blocks[i] - b_blocks[i] - borrow
        if diff < 0:
            diff += BASE
            borrow = 1
        else:
            borrow = 0
        result.insert(0, diff)

    # Remove leading zeros
    while len(result) > 1 and result[0] == 0:
        result.pop(0)

    return result


# Перетворення блоків назад у рядок
def blocks_to_string(blocks):
    result = str(blocks[0])
    for block in blocks[1:]:
        result += f"{block:04d}"
    return result


# Демонстрація роботи
if __name__ == "__main__":
    digits = 18
    num1 = generate_big_number(digits)
    num2 = generate_big_number(digits)

    if int(num1) < int(num2):
        num1, num2 = num2, num1

    print("Число 1:", num1)
    print("Число 2:", num2)

    blocks1 = string_to_blocks(num1)
    blocks2 = string_to_blocks(num2)

    result_add_blocks = add_big_numbers(blocks1, blocks2)
    result_add_str = blocks_to_string(result_add_blocks)

    result_sub_blocks = subtract_big_numbers(blocks1, blocks2)
    result_sub_str = blocks_to_string(result_sub_blocks)

    print("\nРезультат додавання:")
    print(result_add_str)
    print(f"Кількість розрядів: {len(result_add_str)}")

    print("\nРезультат віднімання:")
    print(result_sub_str)
    print(f"Кількість розрядів: {len(result_sub_str)}")

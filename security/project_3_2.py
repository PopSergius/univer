from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)


# Функція для шифрування методом маршрутної перестановки
def spiral_encrypt(text):
    length = len(text)
    rows = cols = math.ceil(math.sqrt(length))  # Розрахунок розміру таблиці
    matrix = [[" " for _ in range(cols)] for _ in range(rows)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Напрями: вправо, вниз, вліво, вгору
    r, c, d = 0, 0, 0  # Початкові координати та напрямок

    # Заповнення таблиці за спіральним порядком
    for char in text.ljust(rows * cols):  # Додаємо пробіли для заповнення таблиці
        matrix[r][c] = char
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] == " "):
            d = (d + 1) % 4  # Зміна напрямку
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc

    # Повертаємо зашифрований текст
    return "".join("".join(row) for row in matrix)


# Функція для дешифрування методом маршрутної перестановки
def spiral_decrypt(text):
    length = len(text)
    rows = cols = math.ceil(math.sqrt(length))  # Розмір таблиці для дешифрування
    matrix = [
        list(text[i * cols : (i + 1) * cols]) for i in range(rows)
    ]  # Формуємо матрицю
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Напрями: вправо, вниз, вліво, вгору
    r, c, d = 0, 0, 0  # Початкові координати та напрямок
    result = []

    while len(result) < length:
        result.append(matrix[r][c])
        matrix[r][c] = " "  # Видаляємо символ, щоб не зчитати його знову
        nr, nc = r + dirs[d][0], c + dirs[d][1]

        # Перевірка, чи наступний індекс знаходиться в межах
        if not (0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != " "):
            d = (d + 1) % 4  # Зміна напрямку
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc

    # Відновлюємо початковий текст (відкидаючи лише пробіли з кінця)
    return "".join(result).rstrip()


@app.route("/")
def index():
    return render_template("project_3_2.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json
    text = data.get("text", "")
    encrypted_text = spiral_encrypt(text)
    return jsonify({"encrypted": encrypted_text})


@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.json
    text = data.get("text", "")
    decrypted_text = spiral_decrypt(text)
    return jsonify({"decrypted": decrypted_text})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)


def generate_playfair_square(key):
    key = key.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    square = []
    seen = set()

    for char in key:
        if char not in seen and char in alphabet:
            square.append(char)
            seen.add(char)

    for char in alphabet:
        if char not in seen:
            square.append(char)
            seen.add(char)

    return [square[i : i + 5] for i in range(0, 25, 5)]


def playfair_encrypt(plaintext, key):
    square = generate_playfair_square(key)
    plaintext = plaintext.upper().replace("J", "I")
    plaintext = "".join(filter(str.isalpha, plaintext))

    prepared_text = ""
    i = 0
    while i < len(plaintext):
        prepared_text += plaintext[i]
        if i + 1 < len(plaintext) and plaintext[i] == plaintext[i + 1]:
            prepared_text += "X"
        i += 1

    if len(prepared_text) % 2 != 0:
        prepared_text += "X"

    ciphertext = ""
    for i in range(0, len(prepared_text), 2):
        a, b = prepared_text[i], prepared_text[i + 1]

        row_a, col_a, row_b, col_b = -1, -1, -1, -1
        for row in range(5):
            if a in square[row]:
                row_a, col_a = row, square[row].index(a)
            if b in square[row]:
                row_b, col_b = row, square[row].index(b)

        if row_a == row_b:
            ciphertext += (
                square[row_a][(col_a + 1) % 5] + square[row_b][(col_b + 1) % 5]
            )
        elif col_a == col_b:
            ciphertext += (
                square[(row_a + 1) % 5][col_a] + square[(row_b + 1) % 5][col_b]
            )
        else:
            ciphertext += square[row_a][col_b] + square[row_b][col_a]

    return ciphertext


def playfair_decrypt(ciphertext, key):
    square = generate_playfair_square(key)
    ciphertext = ciphertext.upper().replace("J", "I")
    ciphertext = "".join(filter(str.isalpha, ciphertext))

    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]

        row_a, col_a, row_b, col_b = -1, -1, -1, -1
        for row in range(5):
            if a in square[row]:
                row_a, col_a = row, square[row].index(a)
            if b in square[row]:
                row_b, col_b = row, square[row].index(b)

        if row_a == row_b:
            plaintext += square[row_a][(col_a - 1) % 5] + square[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += square[(row_a - 1) % 5][col_a] + square[(row_b - 1) % 5][col_b]
        else:
            plaintext += square[row_a][col_b] + square[row_b][col_a]

    # Remove padding 'X' if it was added during encryption
    cleaned_plaintext = ""
    i = 0
    while i < len(plaintext):
        cleaned_plaintext += plaintext[i]
        if (
            i + 2 < len(plaintext)
            and plaintext[i] == plaintext[i + 2]
            and plaintext[i + 1] == "X"
        ):
            i += 2
        else:
            i += 1

    if cleaned_plaintext.endswith("X"):
        cleaned_plaintext = cleaned_plaintext[:-1]

    return cleaned_plaintext


@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"]
        action = request.form["action"]

        if action == "Encrypt":
            result_text = playfair_encrypt(text, key)
        elif action == "Decrypt":
            result_text = playfair_decrypt(text, key)

    return render_template("project_1.html", result_text=result_text)


if __name__ == "__main__":
    app.run(debug=True)

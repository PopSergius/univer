from flask import Flask, render_template, request

app = Flask(__name__)


def vigenere_encrypt(plaintext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    plaintext = plaintext.upper().replace(" ", "").replace("J", "I")
    ciphertext = ""

    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char in alphabet:
            text_index = alphabet.index(char)
            key_index = alphabet.index(key[i % key_length])
            cipher_index = (text_index + key_index) % 26
            ciphertext += alphabet[cipher_index]
        else:
            ciphertext += char

    return ciphertext


def vigenere_decrypt(ciphertext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    ciphertext = ciphertext.upper().replace(" ", "").replace("J", "I")
    plaintext = ""

    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in alphabet:
            cipher_index = alphabet.index(char)
            key_index = alphabet.index(key[i % key_length])
            text_index = (cipher_index - key_index) % 26
            plaintext += alphabet[text_index]
        else:
            plaintext += char

    return plaintext


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        text = request.form["text"]
        key = request.form["key"]

        if action == "Encrypt":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)

        return render_template("project_2.html", result=result)

    return render_template("project_2.html")


if __name__ == "__main__":
    app.run(debug=True)

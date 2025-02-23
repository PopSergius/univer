from flask import Flask, render_template, request

app = Flask(__name__)


# Функція шифрування
def encrypt(text, order):
    text_list = list(text)
    encrypted_text = [""] * len(text)
    for i, pos in enumerate(order):
        encrypted_text[pos] = text_list[i]
    return "".join(encrypted_text)


# Функція дешифрування
def decrypt(text, order):
    decrypted_text = [""] * len(text)
    for i, pos in enumerate(order):
        decrypted_text[i] = text[pos]
    return "".join(decrypted_text)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        order = list(map(int, request.form["order"].split(",")))
        action = request.form["action"]

        if action == "Encrypt":
            result = encrypt(text, order)
        else:
            result = decrypt(text, order)

        return render_template("project_3_1.html", result=result)

    return render_template("project_3_1.html", result=None)


if __name__ == "__main__":
    app.run(debug=True)

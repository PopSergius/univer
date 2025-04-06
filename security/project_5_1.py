from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import math
import random

app = Flask(__name__)


# ========== Функції для RSA ==========
def is_prime(n):
    """Перевірка, чи є число простим"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


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


def get_prime_in_range(start, end):
    """Отримати випадкове просте число в діапазоні"""
    primes = [n for n in range(start, end + 1) if is_prime(n)]
    return random.choice(primes)


p = get_prime_in_range(2, 32)
q = get_prime_in_range(2, 32)

while p == q:
    q = get_prime_in_range(2, 32)

n = p * q
phi = (p - 1) * (q - 1)

e = random.randint(2, phi - 1)
while gcd(e, phi) != 1:
    e = random.randint(2, phi - 1)
d = mod_inverse(e, phi)

public_key = (e, n)
private_key = (d, n)


def encrypt_rsa(message_bytes):
    """Шифрування повідомлення з використанням RSA"""
    encrypted_bytes = bytearray()
    for byte in message_bytes:
        encrypted_value = pow(byte, public_key[0], public_key[1])
        encrypted_bytes.extend(encrypted_value.to_bytes(4, byteorder="big"))
    return bytes(encrypted_bytes)


def decrypt_rsa(encrypted_bytes):
    """Дешифрування повідомлення з використанням RSA"""
    decrypted_bytes = bytearray()
    for i in range(0, len(encrypted_bytes), 4):
        encrypted_value = int.from_bytes(encrypted_bytes[i : i + 4], byteorder="big")
        decrypted_value = pow(encrypted_value, private_key[0], private_key[1])
        decrypted_bytes.append(decrypted_value)
    return bytes(decrypted_bytes)


def encrypt_aes(message_bytes, key, iv):
    """Шифрування повідомлення з використанням AES"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(message_bytes, AES.block_size))


def decrypt_aes(ciphertext, key, iv):
    """Дешифрування повідомлення з використанням AES"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


@app.route("/", methods=["GET", "POST"])
def index():
    results = {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}

    if request.method == "POST":
        surname = request.form["surname"].encode("utf-8")
        message = request.form["message"].encode("utf-8")

        # RSA шифрування прізвища
        encrypted_surname = encrypt_rsa(surname)
        decrypted_surname = decrypt_rsa(encrypted_surname)

        # AES шифрування повідомлення
        aes_key = get_random_bytes(16)
        iv = get_random_bytes(16)
        encrypted_message = encrypt_aes(message, aes_key, iv)

        # Шифрування AES ключа за допомогою RSA
        encrypted_aes_key = encrypt_rsa(aes_key)
        decrypted_aes_key = decrypt_rsa(encrypted_aes_key)

        # Дешифрування повідомлення
        decrypted_message = decrypt_aes(encrypted_message, decrypted_aes_key, iv)

        results.update(
            {
                "surname_plain": surname.decode("utf-8"),
                "surname_encrypted": base64.b64encode(encrypted_surname).decode(),
                "surname_decrypted": decrypted_surname.decode("utf-8"),
                "aes_key_encrypted": base64.b64encode(encrypted_aes_key).decode(),
                "message_plain": message.decode("utf-8"),
                "message_encrypted": base64.b64encode(encrypted_message).decode(),
                "message_decrypted": decrypted_message.decode("utf-8"),
                "iv": base64.b64encode(iv).decode(),
            }
        )

    return render_template("project_5_1.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)

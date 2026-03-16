from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash
import socket

app = Flask(__name__)
app.secret_key = "REDES"

# CONFIGURACIÓN DE USUARIO (REEMPLAZA CON TUS DATOS)
APP_USER = "cesar" 
APP_PW_HASH = "scrypt:32768:8:1$9fgWhAiU3pbTc1Wr$04f2fb7ee35c76468120e3004538406b4bc42785f4293bfa42f7c760fa1003cc8be95e48a313e52d7e0e1e067f17674be2db08b652b41b7aa559e6315263cdad" # Tu hash aquí

TCP_HOST = "127.0.0.1"
TCP_PORT = 5001

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user == APP_USER and check_password_hash(APP_PW_HASH, pw):
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Error de acceso")
    return render_template("login.html")

@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.post("/update_sensor")
def update_sensor():
    data = request.get_json()
    cmd = f"{data['type']}_{data['status']}"
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=1) as s:
            s.sendall((cmd + "\n").encode())
            resp = s.recv(1024).decode()
            return jsonify({"status": "ok", "resp": resp})
    except:
        return jsonify({"status": "error", "msg": "TCP Offline"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

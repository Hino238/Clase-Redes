import socket
import serial

SERIAL_PORT = "/dev/ttyACM0" 
BAUDRATE = 9600

VALID_CMDS = ["HUMEDAD_OK", "HUMEDAD_ADVERTENCIA", "HUMEDAD_ALERTA", "TEMP_NORMAL", "TEMP_ELEVADA", "TEMP_ALERTA"]

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print("[*] Conectado a Arduino")
    except:
        ser = None
        print("[!] Advertencia: Sin Arduino físico")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5001))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                cmd = conn.recv(1024).decode().strip()
                print(f"Recibido: {cmd}")
                if cmd in VALID_CMDS and ser:
                    ser.write((cmd + "\n").encode())
                conn.sendall(b"OK\n")

if __name__ == "__main__":
    main()

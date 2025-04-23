import serial
import tkinter as tk
from tkinter import messagebox

# Ganti dengan port kamu (lihat di Arduino IDE Tools > Port)
SERIAL_PORT = '/dev/ttyUSB0'  # Contoh Windows: 'COM4', Linux/Mac: '/dev/ttyUSB0'
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Gagal membuka port serial: {e}")
    messagebox.showerror("Serial Error", f"Gagal membuka port serial:\n{e}")
    exit()  # Stop program


# Fungsi untuk kirim data ke Arduino
# def kirim_pwm():
    # try:
    #     pwm = int(entry_pwm.get())
    #     if pwm < 0 or pwm > 255:
    #         raise ValueError("Nilai harus 0-255")
    #     ser.write(f"{pwm}\n".encode())
    #     lbl_status.config(text=f"PWM {pwm} dikirim")
    # except ValueError as e:
    #     messagebox.showerror("Input Error", f"Masukkan angka antara 0 - 255\n\n{e}")


def kirim_pwm():
    if not ser or not ser.is_open:
        messagebox.showerror("Serial Error", "Port serial belum terbuka!")
        return
    try:
        pwm = int(entry_pwm.get())
        if pwm < 0 or pwm > 255:
            raise ValueError("Nilai harus 0-255")
        ser.write(f"{pwm}\n".encode())
        lbl_status.config(text=f"PWM {pwm} dikirim")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Masukkan angka antara 0 - 255\n\n{e}")


# Inisialisasi Serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except:
    ser = None
    print("Gagal membuka port serial")

# GUI
root = tk.Tk()
root.title("Kontrol Motor DC N20 via GUI Python")

tk.Label(root, text="Masukkan Nilai PWM (0-255):").pack(pady=5)
entry_pwm = tk.Entry(root)
entry_pwm.pack()

btn_kirim = tk.Button(root, text="Kirim ke Arduino", command=kirim_pwm)
btn_kirim.pack(pady=10)

lbl_status = tk.Label(root, text="Menunggu input...")
lbl_status.pack(pady=5)

root.mainloop()

if ser:
    ser.close()

import tkinter as tk
from tkinter import messagebox
import serial
import time

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Motor & Servo")
        self.root.geometry("500x400")
        self.root.configure(bg="white")

        try:
            self.ser = serial.Serial('COM6', 115200, timeout=1)  # Ganti COM port sesuai PC kamu
            time.sleep(2)  # Tunggu koneksi stabil
        except:
            messagebox.showerror("Error", "Tidak bisa terhubung ke Arduino!")

        self._setup_ui()

    def _setup_ui(self):
        header = tk.Label(self.root, text="Kontrol Motor Kiri, Kanan, dan Servo", font=("Arial", 14, "bold"), bg="white")
        header.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        # Motor Kiri
        frame_motorL = tk.LabelFrame(frame, text="Motor Kiri", bg="#f0f0f0")
        frame_motorL.grid(row=0, column=0, padx=10, pady=10)
        self.motorL_entry = self._create_input(frame_motorL, "ML", 0, 255)

        # Motor Kanan
        frame_motorR = tk.LabelFrame(frame, text="Motor Kanan", bg="#f0f0f0")
        frame_motorR.grid(row=0, column=1, padx=10, pady=10)
        self.motorR_entry = self._create_input(frame_motorR, "MR", 0, 255)

        # Servo
        frame_servo = tk.LabelFrame(frame, text="Servo", bg="#f0f0f0")
        frame_servo.grid(row=1, column=0, columnspan=2, pady=10)
        self.servo_entry = self._create_input(frame_servo, "S", 0, 180)

    def _create_input(self, parent, tag, min_val, max_val):
        tk.Label(parent, text=f"Masukkan nilai ({min_val}-{max_val}):", bg="#f0f0f0").pack()
        entry = tk.Entry(parent)
        entry.pack(pady=5)

        btn = tk.Button(parent, text="Kirim", command=lambda: self._validate_and_send(entry, min_val, max_val, tag))
        btn.pack()

        return entry

    def _validate_and_send(self, entry, min_val, max_val, tag):
        try:
            value = int(entry.get())
            if min_val <= value <= max_val:
                self.kirim_data(tag, value)
                messagebox.showinfo("Info", f"{tag}:{value} berhasil dikirim.")
            else:
                messagebox.showerror("Error", f"Nilai harus antara {min_val} dan {max_val}.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    def kirim_data(self, tag, value):
        if self.ser.is_open:
            kirim = f"{tag}:{value}\n"
            self.ser.write(kirim.encode())

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
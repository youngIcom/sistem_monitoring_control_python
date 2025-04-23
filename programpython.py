import tkinter as tk
from tkinter import messagebox
import serial


# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor RPM, Servo dan Sensor")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self._setup_ui()

    def _setup_ui(self):
        header = tk.Label(self.root, text="SISTEM MONITORING", font=("Arial", 16), bg="#f0f0f0")
        header.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        #Frame kiri
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", padx=10, pady=10)

        self._create_input(left_frame, "RPM Motor Kanan", 0, 255)

    def _create_input(self, parent, label_text, min_val, max_val):
        label = tk.Label(parent, text=label_text, bg="#f0f0f0")
        label.pack()

        entry = tk.Entry(parent)
        entry.pack()

        button = tk.Button(parent, text="send", command=lambda: self._validate_input(entry, min_val, max_val))
        button.pack(pady=5)

    def _validate_input(self, entry, min_val, max_val):
        try:
            value = int(entry.get())
            if min_val <= value <= max_val:
                messagebox.showinfo("Input diterima", f"Value: {value}")
            else:
                messagebox.showerror("Error", f"Value must be between {min_val} and {max_val}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")


#jalankan program
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
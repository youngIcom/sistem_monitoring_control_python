import tkinter as tk
from tkinter import ttk, messagebox
import serial

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Monitor")
        self.root.geometry("900x450")
        self.root.configure(bg="#F0F4F8")

        self.judul = ["Motor", "Servo"]
        self.entries = []

        try:
            self.serial_conn = serial.Serial('COM3', 115200, timeout=1)
        except serial.SerialException as e:
            messagebox.showerror("Error", f"Tidak bisa membuka port COM3.\n{e}")
            self.serial_conn = None

        tk.Label(self.root, text="SISTEM MONITOR", font=("Segoe UI", 16, "bold"),
                 fg="#0aa1ff", bg="#F0F4F8").pack(pady=15)

        main_frame = tk.Frame(self.root, bg="#F0F4F8")
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(main_frame, bg="#F0F4F8")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        self.right_frame = tk.Frame(main_frame, bg="#F0F4F8")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))

        separator = ttk.Separator(main_frame, orient='vertical')
        separator.place(relx=0.5, rely=0, relheight=1)

        self.create_left_side()
        self.create_right_side()
        self.root.after(100, self.read_serial)

    def __del__(self):
        ...

    def update_sensor_value(self, index, value):
        ...

    def read_serial(self):
        ...

    def create_left_side(self):
        input_frame = tk.Frame(self.left_frame, bg="#F0F4F8")
        input_frame.pack(fill="x", pady=10)

        for i, label_text in enumerate(self.judul):
            label = tk.Label(input_frame, text=f"{i+1}. {label_text}",
                             font=("Segoe UI", 13, "bold"), fg="#0a75ff", bg="#F0F4F8")
            label.grid(row=i, column=0, sticky="w", pady=6, padx=5)
            entry = tk.Entry(input_frame, font=("Segoe UI", 13), width=18, bd=2, relief="groove")
            entry.grid(row=i, column=1, pady=6, padx=5)
            self.entries.append(entry)
            btn = tk.Button(input_frame, text="OK", font=("Segoe UI", 11, "bold"),
                            bg="#0a75ff", fg="white", width=4,
                            command=lambda e=entry, l=label_text: self.submit(e, l))
            btn.grid(row=i, column=2, padx=5, pady=6)

        map_nav_frame = tk.Frame(self.left_frame, bg="#FFFFFF", relief="ridge", bd=2)
        map_nav_frame.pack(pady=15, fill="both", expand=True)

        canvas_width = 350
        canvas_height = 160
        self.x_pos, self.y_pos, self.step = canvas_width // 2, canvas_height // 2, 10
        self.direction = "up"

        self.canvas = tk.Canvas(map_nav_frame, width=canvas_width, height=canvas_height, bg="#eef6ff")
        self.canvas.pack(pady=10)

        self.tracker = self.canvas.create_oval(self.x_pos-7, self.y_pos-7,
                                               self.x_pos+7, self.y_pos+7,
                                               fill="#007fff")

        btn_frame = tk.Frame(map_nav_frame, bg="#F0F4F8")
        btn_frame.pack(pady=8)

        btn_opts = {"width": 4, "height": 2, "bg": "#0a75ff", "fg": "white", "font": ("Segoe UI", 12, "bold")}

        tk.Button(btn_frame, text="↑", command=self.move_up, **btn_opts).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="←", command=self.move_left, **btn_opts).grid(row=1, column=0, padx=8)
        tk.Button(btn_frame, text="↓", command=self.move_down, **btn_opts).grid(row=1, column=1, padx=8)
        tk.Button(btn_frame, text="→", command=self.move_right, **btn_opts).grid(row=1, column=2, padx=8)

    def create_right_side(self):
        ...

    def move_tracker(self, dx, dy):
        new_x = self.x_pos + dx
        new_y = self.y_pos + dy

        if 0 < new_x < 350 and 0 < new_y < 160:
            self.canvas.move(self.tracker, dx, dy)
            self.x_pos = new_x
            self.y_pos = new_y

    def move_up(self):
        self.move_tracker(0, -self.step)
        self.direction = "up"

    def move_down(self):
        self.move_tracker(0, self.step)
        self.direction = "down"

    def move_left(self):
        self.move_tracker(-self.step, 0)
        self.direction = "left"

    def move_right(self):
        self.move_tracker(self.step, 0)
        self.direction = "right"

    def submit(self, entry, label):
        val = entry.get()
        if val.isdigit() and 0 <= int(val) <= 200:
            messagebox.showinfo("Sukses", f"{label} sebesar: {val}")
            if self.serial_conn and self.serial_conn.is_open:
                try:
                    self.serial_conn.write(f"{label}:{val}\n".encode())
                except serial.SerialException:
                    messagebox.showerror("Error", "Gagal mengirim data ke perangkat Serial.")
        else:
            messagebox.showwarning("Error", f"Input {label} harus angka 0-200.")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MonitorApp(root)
        root.mainloop()
    finally:
        del app
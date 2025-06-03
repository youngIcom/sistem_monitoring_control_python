import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
# from serial_interface import SerialInterface
# from motor_controller import MotorController
# from servo_controller import ServoController
import threading

class MotorControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP8266 Motor Controller")
        self.root.geometry("800x600")
        
        # Initialize components
        # self.serial_interface = SerialInterface()
        # self.motor_controller = MotorController(self.serial_interface)
        # self.servo_controller = ServoController(self.serial_interface)
        
        # Setup UI
        self.setup_ui()
        
        # Start serial monitor thread
        self.serial_monitor_active = True
        self.serial_monitor_thread = threading.Thread(target=self.serial_monitor, daemon=True)
        self.serial_monitor_thread.start()
        
        # Try to auto-connect
        self.auto_connect()

    def setup_ui(self):
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', padding=5)
        self.style.configure('Red.TButton', foreground='red')
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Connection frame
        self.connection_frame = ttk.LabelFrame(self.main_frame, text="Serial Connection", padding=10)
        self.connection_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Motor control frames
        self.motor_frame = ttk.LabelFrame(self.main_frame, text="Motor Control", padding=10)
        self.motor_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Servo control frame
        self.servo_frame = ttk.LabelFrame(self.main_frame, text="Servo Control", padding=10)
        self.servo_frame.grid(row=2, column=0, sticky="ew")
        
        # Console frame
        self.console_frame = ttk.LabelFrame(self.main_frame, text="Console", padding=10)
        self.console_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        
        # Setup all UI components
        self.setup_connection_ui()
        self.setup_motor_ui()
        self.setup_servo_ui()
        self.setup_console_ui()
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.console_frame.columnconfigure(0, weight=1)
        self.console_frame.rowconfigure(0, weight=1)

    def setup_connection_ui(self):
        # Port selection
        ttk.Label(self.connection_frame, text="Port:").grid(row=0, column=0, sticky="w")
        self.port_combobox = ttk.Combobox(self.connection_frame, values=self.serial_interface.get_available_ports())
        self.port_combobox.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Baud rate
        ttk.Label(self.connection_frame, text="Baud Rate:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.baud_combobox = ttk.Combobox(self.connection_frame, values=[9600, 19200, 38400, 57600, 115200])
        self.baud_combobox.set("115200")
        self.baud_combobox.grid(row=0, column=3, sticky="ew", padx=5)
        
        # Connect button
        self.connect_button = ttk.Button(self.connection_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.grid(row=0, column=4, padx=(10, 0))
        
        # Status indicator
        self.status_label = ttk.Label(self.connection_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=5, sticky="w", pady=(5, 0))
        
        # Configure grid weights
        for i in range(5):
            self.connection_frame.columnconfigure(i, weight=1 if i in [1, 3] else 0)

    def setup_motor_ui(self):
        # Motor 1 controls
        ttk.Label(self.motor_frame, text="Motor 1:").grid(row=0, column=0, sticky="w")
        
        self.motor1_speed = tk.IntVar(value=0)
        self.motor1_scale = ttk.Scale(self.motor_frame, from_=-100, to=100, variable=self.motor1_speed, command=lambda v: self.on_motor_change(1, float(v)))
        self.motor1_scale.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.motor1_label = ttk.Label(self.motor_frame, text="0% (Stopped)")
        self.motor1_label.grid(row=0, column=2, padx=5)
        
        # Motor 2 controls
        ttk.Label(self.motor_frame, text="Motor 2:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        
        self.motor2_speed = tk.IntVar(value=0)
        self.motor2_scale = ttk.Scale(
            self.motor_frame, from_=-100, to=100, variable=self.motor2_speed,
            command=lambda v: self.on_motor_change(2, float(v)))
        self.motor2_scale.grid(row=1, column=1, sticky="ew", padx=5, pady=(10, 0))
        
        self.motor2_label = ttk.Label(self.motor_frame, text="0% (Stopped)")
        self.motor2_label.grid(row=1, column=2, padx=5, pady=(10, 0))
        
        # Stop all button
        self.stop_button = ttk.Button(
            self.motor_frame, text="STOP ALL", style='Red.TButton',
            command=self.stop_all_motors)
        self.stop_button.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        # Configure grid weights
        self.motor_frame.columnconfigure(1, weight=1)

    def setup_servo_ui(self):
        # Servo angle control
        ttk.Label(self.servo_frame, text="Angle (0-180°):").grid(row=0, column=0, sticky="w")
        
        self.servo_angle = tk.IntVar(value=90)
        self.servo_scale = ttk.Scale(
            self.servo_frame, from_=0, to=180, variable=self.servo_angle,
            command=lambda v: self.on_servo_change(int(float(v))))
        self.servo_scale.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.servo_label = ttk.Label(self.servo_frame, text="90°")
        self.servo_label.grid(row=0, column=2, padx=5)
        
        # Preset buttons
        presets_frame = ttk.Frame(self.servo_frame)
        presets_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        angles = [0, 45, 90, 135, 180]
        for i, angle in enumerate(angles):
            ttk.Button(
                presets_frame, text=f"{angle}°",
                command=lambda a=angle: self.set_servo_angle(a)
            ).grid(row=0, column=i, sticky="ew", padx=2)
            presets_frame.columnconfigure(i, weight=1)
        
        # Configure grid weights
        self.servo_frame.columnconfigure(1, weight=1)

    def setup_console_ui(self):
        # Console text area
        self.console_text = tk.Text(self.console_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.console_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.console_frame, command=self.console_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.console_text.config(yscrollcommand=scrollbar.set)
        
        # Clear button
        ttk.Button(
            self.console_frame, text="Clear Console",
            command=self.clear_console
        ).grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="ew")

    def auto_connect(self):
        ports = self.serial_interface.get_available_ports()
        if ports:
            self.port_combobox.set(ports[0])
            self.toggle_connection()

    def toggle_connection(self):
        if self.serial_interface.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        port = self.port_combobox.get()
        baud = int(self.baud_combobox.get())
        
        if not port:
            messagebox.showerror("Error", "Please select a COM port")
            return
        
        if self.serial_interface.connect(port, baud):
            self.connect_button.config(text="Disconnect")
            self.status_label.config(text=f"Connected to {port} @ {baud} baud", foreground="green")
            self.log_message(f"Connected to {port} at {baud} baud")
        else:
            messagebox.showerror("Error", f"Failed to connect to {port}")
            self.log_message(f"Connection failed to {port}")

    def disconnect(self):
        self.motor_controller.stop_all_motors()
        self.serial_interface.disconnect()
        self.connect_button.config(text="Connect")
        self.status_label.config(text="Disconnected", foreground="red")
        self.log_message("Disconnected")

    def on_motor_change(self, motor_num, speed):
        speed = int(speed)
        direction = 'F' if speed >= 0 else 'R'
        abs_speed = abs(speed)
        
        # Update label
        if motor_num == 1:
            status = "Forward" if speed > 0 else "Reverse" if speed < 0 else "Stopped"
            self.motor1_label.config(text=f"{speed}% ({status})")
        else:
            status = "Forward" if speed > 0 else "Reverse" if speed < 0 else "Stopped"
            self.motor2_label.config(text=f"{speed}% ({status})")
        
        # Send command
        if self.serial_interface.connected:
            self.motor_controller.set_motor_speed(motor_num, direction, abs_speed)
            self.log_message(f"Motor {motor_num} set to {speed}% ({direction})")

    def stop_all_motors(self):
        self.motor1_speed.set(0)
        self.motor2_speed.set(0)
        self.motor1_label.config(text="0% (Stopped)")
        self.motor2_label.config(text="0% (Stopped)")
        
        if self.serial_interface.connected:
            self.motor_controller.stop_all_motors()
            self.log_message("All motors stopped")

    def on_servo_change(self, angle):
        self.servo_label.config(text=f"{angle}°")
        if self.serial_interface.connected:
            self.servo_controller.set_angle(angle)
            self.log_message(f"Servo set to {angle}°")

    def set_servo_angle(self, angle):
        self.servo_angle.set(angle)
        self.servo_label.config(text=f"{angle}°")
        if self.serial_interface.connected:
            self.servo_controller.set_angle(angle)
            self.log_message(f"Servo preset to {angle}°")

    def log_message(self, message):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.config(state=tk.DISABLED)
        self.console_text.see(tk.END)

    def clear_console(self):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)

    def serial_monitor(self):
        """Thread function to monitor serial input"""
        while self.serial_monitor_active:
            if self.serial_interface.connected:
                message = self.serial_interface.read_line()
                if message:
                    self.log_message(f"Device: {message}")
            self.root.update_idletasks()

    def on_closing(self):
        """Clean up when closing the application"""
        self.serial_monitor_active = False
        self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
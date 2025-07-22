import tkinter as tk
from tkinter import messagebox
import threading
import time

class ProductivityTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Tracker Timer")

        self.paused = False
        self.main_clock_done = False
        self.input_time = 0  # in minutes

        # UI Elements
        tk.Label(root, text="Enter total time (minutes):").pack()

        self.time_entry = tk.Entry(root)
        self.time_entry.pack()

        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.downclock_label = tk.Label(root, text="DownClock: --:--", font=("Helvetica", 16))
        self.downclock_label.pack(pady=10)

        self.upclock_label = tk.Label(root, text="UpClock (productive): --:--", font=("Helvetica", 16))
        self.upclock_label.pack(pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.pack(side="left", padx=20)

        self.resume_button = tk.Button(root, text="Resume", command=self.resume_timer, state="disabled")
        self.resume_button.pack(side="right", padx=20)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=10)

    def start_timer(self):
        try:
            self.input_time = int(self.time_entry.get())
            if self.input_time <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a positive integer for time in minutes.")
            return

        self.time_entry.config(state="disabled")
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")

        self.paused = False
        self.main_clock_done = False

        self.down_thread = threading.Thread(target=self.run_downclock, daemon=True)
        self.up_thread = threading.Thread(target=self.run_upclock, daemon=True)

        self.down_thread.start()
        self.up_thread.start()

    def run_downclock(self):
        secs = self.input_time * 60
        while secs >= 0 and not self.main_clock_done:
            mins, sec = divmod(secs, 60)
            timer_text = f"DownClock: {mins:02d}:{sec:02d}"
            self.update_label(self.downclock_label, timer_text)

            if secs == 0:
                self.main_clock_done = True
                self.update_label(self.status_label, "Time's up !!!")
                self.enable_restart()
                break

            secs -= 1
            time.sleep(1)

    def run_upclock(self):
        secs = 0
        total_secs = self.input_time * 60
        while secs <= total_secs and not self.main_clock_done:
            if self.paused:
                time.sleep(0.1)
                continue

            mins, sec = divmod(secs, 60)
            timer_text = f"UpClock (productive): {mins:02d}:{sec:02d}"
            self.update_label(self.upclock_label, timer_text)

            secs += 1
            time.sleep(1)

    def update_label(self, label, text):
        def task():
            label.config(text=text)
        self.root.after(0, task)

    def pause_timer(self):
        if not self.main_clock_done:
            self.paused = True
            self.status_label.config(text="Paused ⏸️")
            self.pause_button.config(state="disabled")
            self.resume_button.config(state="normal")

    def resume_timer(self):
        if not self.main_clock_done:
            self.paused = False
            self.status_label.config(text="Resumed ▶️")
            self.pause_button.config(state="normal")
            self.resume_button.config(state="disabled")

    def enable_restart(self):
        def task():
            self.pause_button.config(state="disabled")
            self.resume_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.time_entry.config(state="normal")
        self.root.after(0, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityTimer(root)
    root.mainloop()

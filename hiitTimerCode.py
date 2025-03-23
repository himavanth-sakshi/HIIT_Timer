import tkinter as tk
from tkinter import messagebox
import threading
from playsound import playsound
import os

class HIITTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HIIT Timer")
        self.root.resizable(True, True)
        self.running = False
        self.paused = False
        self.round = 0
        self.remaining_time = 0
        self.current_callback = None
        self.current_phase = ""

        # Paths to your sound files
        self.start_sound = "sounds/gong-sound-effect-308757.mp3"
        self.beep_sound = "sounds/gong-sound-effect-308757.mp3"
        self.final_12_sound = "sounds/The most motivational 10 seconds of video ever.mp3"

        # UI elements
        tk.Label(root, text="Work Duration (sec):").grid(row=0, column=0, pady=5, sticky='e')
        self.work_entry = tk.Entry(root)
        self.work_entry.grid(row=0, column=1, sticky='ew')

        tk.Label(root, text="Rest Duration (sec):").grid(row=1, column=0, pady=5, sticky='e')
        self.rest_entry = tk.Entry(root)
        self.rest_entry.grid(row=1, column=1, sticky='ew')

        tk.Label(root, text="Number of Rounds:").grid(row=2, column=0, pady=5, sticky='e')
        self.rounds_entry = tk.Entry(root)
        self.rounds_entry.grid(row=2, column=1, sticky='ew')

        self.timer_label = tk.Label(root, text="Ready", font=("Helvetica", 32), anchor="center")
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=15, sticky="nsew")

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.grid(row=4, column=0, pady=10, sticky="ew")

        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause, state="disabled")
        self.pause_button.grid(row=4, column=1, pady=10, sticky="ew")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # Make rows and columns resizable
        for i in range(6):  # Total rows
            root.grid_rowconfigure(i, weight=1)
        for i in range(2):  # 2 columns
            root.grid_columnconfigure(i, weight=1)

    def play_sound(self, path):
        if os.path.exists(path):
            threading.Thread(target=playsound, args=(path,), daemon=True).start()

    def start_timer(self):
        try:
            self.work_duration = int(self.work_entry.get())
            self.rest_duration = int(self.rest_entry.get())
            self.total_rounds = int(self.rounds_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        if self.work_duration <= 0 or self.rest_duration <= 0 or self.total_rounds <= 0:
            messagebox.showerror("Input Error", "Values must be greater than 0.")
            return

        self.running = True
        self.paused = False
        self.pause_button.config(state="normal", text="Pause")
        self.start_button.config(state="disabled")
        self.round = 1
        self.run_work()

    def stop_timer(self):
        self.running = False
        self.paused = False
        self.pause_button.config(state="disabled", text="Pause")
        self.start_button.config(state="normal")
        self.timer_label.config(text="Stopped")

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.countdown(self.remaining_time, self.current_callback, self.current_phase)

    def run_work(self):
        if not self.running or self.round > self.total_rounds:
            self.timer_label.config(text="Workout Complete!")
            self.pause_button.config(state="disabled")
            self.start_button.config(state="normal")
            return
        self.play_sound(self.start_sound)
        self.timer_label.config(text=f"Work: Round {self.round}")
        self.countdown(self.work_duration, self.run_rest, phase="Work")

    def run_rest(self):
        if not self.running:
            return
        self.timer_label.config(text=f"Rest: Round {self.round}")
        self.countdown(self.rest_duration, self.next_round, phase="Rest")

    def next_round(self):
        self.round += 1
        self.run_work()

    def countdown(self, remaining, callback, phase):
        if not self.running:
            return

        if self.paused:
            self.remaining_time = remaining
            self.current_callback = callback
            self.current_phase = phase
            return

        self.remaining_time = remaining
        self.current_callback = callback
        self.current_phase = phase

        mins, secs = divmod(remaining, 60)
        self.timer_label.config(
            text=f"{phase}: Round {self.round} of {self.total_rounds} - {mins:02d}:{secs:02d}"
        )

        # Play sounds at specific times
        if remaining in [3, 2, 1]:
            self.play_sound(self.beep_sound)
        if remaining == 12:
            self.play_sound(self.final_12_sound)

        if remaining > 0:
            self.root.after(1000, lambda: self.countdown(remaining - 1, callback, phase))
        else:
            callback()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = HIITTimerApp(root)
    root.mainloop()

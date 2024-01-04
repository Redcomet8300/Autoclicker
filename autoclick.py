import tkinter as tk
import pyautogui
import threading
import time

class AutoClickerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("AutoClicker")
        self.master.geometry("300x150")

        self.click_rate_label = tk.Label(master, text="Click Rate (cps):")
        self.click_rate_label.pack()

        self.click_rate_entry = tk.Entry(master)
        self.click_rate_entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_autoclick)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_autoclick, state=tk.DISABLED)
        self.stop_button.pack()

        self.autoclicking = False
        self.thread = None

        # Bind F5 key press to start and stop functions
        self.master.bind("<F5>", lambda event: self.toggle_autoclick())

        # Bind focus events to start and stop functions
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind("<FocusOut>", self.on_focus_out)
        self.master.bind("<FocusIn>", self.on_focus_in)

    def on_closing(self):
        self.master.destroy()

    def on_focus_out(self, event):
        if self.autoclicking:
            self.stop_autoclick()

    def on_focus_in(self, event):
        pass  # You can add specific behavior when the window gains focus if needed

    def start_autoclick(self):
        click_rate = float(self.click_rate_entry.get())
        self.autoclicking = True
        self.thread = threading.Thread(target=self.autoclick, args=(click_rate,))
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_autoclick(self):
        self.autoclicking = False
        if self.thread:
            self.thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def toggle_autoclick(self):
        if self.autoclicking:
            self.stop_autoclick()
        else:
            self.start_autoclick()

    def autoclick(self, click_rate):
        while self.autoclicking:
            pyautogui.click()
            time.sleep(1 / click_rate)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.mainloop()

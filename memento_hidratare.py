import tkinter as tk
from tkinter import messagebox
import time
import threading

class HydrationReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memento Hidratare")
        self.root.geometry("400x500")  # Dimensiunea ferestrei

        self.label = tk.Label(root, text="Setează intervalul de hidratare:")
        self.label.pack(pady=10)

        # Câmpuri pentru ore, minute și secunde
        self.hours_label = tk.Label(root, text="Ore:")
        self.hours_label.pack()
        self.hours_entry = tk.Entry(root)
        self.hours_entry.pack(pady=5)

        self.minutes_label = tk.Label(root, text="Minute:")
        self.minutes_label.pack()
        self.minutes_entry = tk.Entry(root)
        self.minutes_entry.pack(pady=5)

        self.seconds_label = tk.Label(root, text="Secunde:")
        self.seconds_label.pack()
        self.seconds_entry = tk.Entry(root)
        self.seconds_entry.pack(pady=5)

        # Butonul de început
        self.start_button = tk.Button(root, text="Începe", command=self.start_reminder)
        self.start_button.pack(pady=10)

        # Butonul de oprire
        self.stop_button = tk.Button(root, text="Oprește", command=self.stop_reminder)
        self.stop_button.pack(pady=10)

        # Label pentru cronometru
        self.timer_label = tk.Label(root, text="Timp rămas: 00:00", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        # Zonă pentru istoric
        self.history_label = tk.Label(root, text="Istoric notificări:")
        self.history_label.pack(pady=5)
        self.history_text = tk.Text(root, height=10, width=45, state=tk.DISABLED)
        self.history_text.pack(pady=10)

        self.reminder_thread = None
        self.running = False
        self.time_left = 0

    def start_reminder(self):
        try:
            # Obținem valorile introduse de utilizator
            hours = int(self.hours_entry.get()) if self.hours_entry.get() else 0
            minutes = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
            seconds = int(self.seconds_entry.get()) if self.seconds_entry.get() else 0

            # Calculăm intervalul total în secunde
            total_seconds = hours * 3600 + minutes * 60 + seconds

            if total_seconds <= 0:
                messagebox.showerror("Eroare", "Introdu un interval valid!")
                return

            self.running = True
            self.time_left = total_seconds  # Setăm timpul rămas
            self.reminder_thread = threading.Thread(target=self.reminder, args=(total_seconds,))
            self.reminder_thread.start()

            # Actualizăm cronometru
            self.update_timer()

        except ValueError:
            messagebox.showerror("Eroare", "Introdu un număr valid!")

    def reminder(self, interval):
        while self.running:
            time.sleep(interval)
            if self.running:
                self.show_reminder()

    def show_reminder(self):
        messagebox.showinfo("Hidratare", "Este timpul să bei apă!")

        # Adăugă notificarea în istoric
        self.add_to_history("Notificare de hidratare: " + time.strftime("%H:%M:%S"))

    def stop_reminder(self):
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join()

    def update_timer(self):
        if self.running and self.time_left > 0:
            minutes, seconds = divmod(self.time_left, 60)
            self.timer_label.config(text=f"Timp rămas: {minutes:02}:{seconds:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)  # Actualizăm la fiecare secundă

    def add_to_history(self, message):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, message + "\n")
        self.history_text.see(tk.END)  # Derulează automat la final
        self.history_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = HydrationReminderApp(root)
    root.mainloop()

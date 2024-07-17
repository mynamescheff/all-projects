import tkinter as tk
from tkinter import messagebox, BooleanVar, Frame, Label, Checkbutton, Button, Text
import sys
import queue
import threading
import time
import pythoncom
import os

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()

    def write(self, message):
        self.queue.put(message)

    def flush(self):
        pass

    def clear(self):
        self.queue = queue.Queue()

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Processing Hub")
        self.root.geometry("400x450")
        self.root.minsize(400, 450)
        self.root.maxsize(800, 600)

        frame = Frame(root)
        frame.pack(pady=20)

        self.label = Label(frame, text="Excel Processing Hub", font=("Arial", 18))
        self.label.pack(pady=10)
        self.label.bind("<Button-1>", self.check_hidden_popup)

        self.click_counter = 0
        self.click_time = 0

        self.mark_as_read_var = BooleanVar()
        self.mark_as_read_checkbox = Checkbutton(frame, text="Mark Emails as Read", variable=self.mark_as_read_var)
        self.mark_as_read_checkbox.pack(pady=5)

        self.email_button = Button(frame, text="Download Email Attachments", command=self.run_email_dl_task)
        self.email_button.pack(pady=5)

        self.kejsar_button = Button(frame, text="Process Cases", command=self.run_kejsar_task)
        self.kejsar_button.pack(pady=5)

        self.notes_button = Button(frame, text="Notes", command=self.create_notes_window)
        self.notes_button.pack(pady=5)

        self.instructions_button = Button(frame, text="Instructions", command=self.create_instructions_window)
        self.instructions_button.pack(pady=5)

        self.debug_text = Text(frame, wrap="word", height=10, width=50, state='disabled')
        self.debug_text.pack(pady=5)

        self.debug_output = TextRedirector(self.debug_text)
        sys.stdout = self.debug_output
        sys.stderr = self.debug_output

        self.update_debug_text()

    def update_debug_text(self):
        while not self.debug_output.queue.empty():
            message = self.debug_output.queue.get()
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert("end", message)
            self.debug_text.see("end")
            self.debug_text.config(state=tk.DISABLED)
        self.root.after(500, self.update_debug_text)

    def update_gui_from_queue(self, q, text_widget):
        try:
            while not q.empty():
                message_type, message = q.get_nowait()
                if message_type == 'output' and message:
                    text_widget.config(state=tk.NORMAL)
                    text_widget.insert(tk.END, message)
                    text_widget.see(tk.END)  # Scroll to the end to show the latest message
                    text_widget.config(state=tk.DISABLED)
                elif message_type == 'error' and message:
                    text_widget.config(state=tk.NORMAL)
                    text_widget.insert(tk.END, "Error: " + message)
                    text_widget.see(tk.END)  # Scroll to the end to show the latest message
                    text_widget.config(state=tk.DISABLED)
                elif message_type == 'done' and message:
                    text_widget.config(state=tk.NORMAL)
                    text_widget.insert(tk.END, message)
                    text_widget.see(tk.END)  # Scroll to the end to show the latest message
                    text_widget.config(state=tk.DISABLED)
        except queue.Empty:
            pass
        finally:
            text_widget.after(1000, lambda: self.update_gui_from_queue(q, text_widget))  # Check the queue every second

    def print(self, message):
        self.debug_output += message + "\n"
        print(message)
        self.update_debug_text()

    def run_long_running_task(self, task_func, *args):
        task_thread = threading.Thread(target=task_func, args=args, daemon=True)
        task_thread.start()

    def run_email_dl_task(self):
        q = queue.Queue()
        self.run_long_running_task(self.run_email_dl, q)
        self.update_gui_from_queue(q, self.debug_text)

    def run_kejsar_task(self):
        q = queue.Queue()
        self.run_long_running_task(self.run_kejsar, q)
        self.update_gui_from_queue(q, self.debug_text)

    def run_email_dl(self, q=None):
        threading.Thread(target=self._run_email_dl, args=(q,)).start()

    def _run_email_dl(self, q=None):
        # Initialize COM library in this thread
        pythoncom.CoInitialize()
        # function logic here

    def run_kejsar(self, q):
        # Get the absolute path of the script
        script_path = os.path.dirname(os.path.abspath(__file__))
        processor = KejsarProcessor(script_path)
        processor.run()
        messagebox.showinfo("Info", "Kejsar processing completed.")

    def create_notes_window(self):
        global notes_window, notes_content, notes_first_time
        if not notes_window or not tk.Toplevel.winfo_exists(notes_window):
            notes_window = tk.Toplevel()
            notes_window.title("Notes")
            notes_window.geometry("300x200+200+50")
            notes_window.resizable(True, True)
            notes_window.minsize(150, 100)
            notes_window.maxsize(600, 400)
            text_widget = tk.Text(notes_window, wrap=tk.WORD)
            text_widget.grid(row=0, column=0, sticky='nsew')
            notes_window.grid_rowconfigure(0, weight=1)
            notes_window.grid_columnconfigure(0, weight=1)
            text_widget.insert(tk.END, notes_content)

            def on_closing():
                global notes_window, notes_content
                notes_content = text_widget.get("1.0", tk.END)
                notes_window.destroy()
                notes_window = None

            notes_window.bind("<Escape>", lambda event: on_closing())
            notes_window.protocol("WM_DELETE_WINDOW", on_closing)
            notes_window.focus_set()

            if notes_first_time:
                notes_window.after(1000, lambda: messagebox.showinfo("Note", 
                    "Please note that any notes you make will disappear when closing the program."))
                notes_first_time = False

    def create_instructions_window(self):
        global instructions_window
        if not instructions_window or not tk.Toplevel.winfo_exists(instructions_window):
            instructions_window = tk.Toplevel()
            instructions_window.title("Instructions")
            instructions_window.geometry("300x200")
            text_widget = tk.Text(instructions_window, height=10, width=30, wrap=tk.WORD)
            text_widget.pack(padx=10, pady=10)
            text_widget.insert(tk.END, "Follow these instructions...\n1. Do X\n2. Do Y\n3. Don't forget Z")
            text_widget.config(state=tk.DISABLED)

            def on_closing():
                global instructions_window
                instructions_window.destroy()
                instructions_window = None

            instructions_window.bind("<Escape>", lambda event: on_closing())

            instructions_window.protocol("WM_DELETE_WINDOW", on_closing)

            instructions_window.focus_set()

    def check_hidden_popup(self, event):
        current_time = time.time()
        if current_time - self.click_time > 3:
            self.click_counter = 0
        self.click_time = current_time
        self.click_counter += 1
        if self.click_counter == 7:
            self.show_hidden_popup()
            self.click_counter = 0

    def show_hidden_popup(self):
        hidden_popup = tk.Toplevel(self.root)
        hidden_popup.title("Hidden Section")
        hidden_popup.geometry("300x200")
        text_widget = tk.Text(hidden_popup, height=10, width=30, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, "This is the hidden section.\nCongratulations!")
        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()

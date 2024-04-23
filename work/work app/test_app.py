import tkinter as tk
from tkinter import messagebox
import threading

# Import your script's main functionality
# from your_script import main_functionality

def run_script():
    try:
        # Check the state of the checkboxes and run parts of the script accordingly
        if option1_var.get():
            threading.Thread(target=part1_functionality).start()
        if option2_var.get():
            threading.Thread(target=part2_functionality).start()
        
        messagebox.showinfo("Success", "Selected script parts are running in the background!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def part1_functionality():
    # Implement the functionality for part 1
    pass

def part2_functionality():
    # Implement the functionality for part 2
    pass

def create_notes_window():
    # Create a new top-level window for notes
    notes_window = tk.Toplevel()
    notes_window.title("Notes")
    notes_window.geometry("300x200")  # Width x Height
    notes_window.resizable(True, True)  # Allow resizing

    # Add a text widget for notes
    text_widget = tk.Text(notes_window, height=10, width=30)
    text_widget.pack(padx=10, pady=10)

    # Insert any default text or load notes from a file if necessary
    text_widget.insert(tk.END, "Place your notes here...")

def create_instructions_window():
    # Create a new top-level window for instructions
    instructions_window = tk.Toplevel()
    instructions_window.title("Instructions")
    instructions_window.geometry("300x200")  # Width x Height
    instructions_window.resizable(False, False)  # Disable resizing

    # Add a text widget for instructions, make it read-only
    text_widget = tk.Text(instructions_window, height=10, width=30, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)
    text_widget.insert(tk.END, "Follow these instructions...\n1. Do X\n2. Do Y\n3. Don't forget Z")
    text_widget.config(state=tk.DISABLED)  # Make the text widget non-editable

def create_ui():
    global option1_var, option2_var
    root = tk.Tk()
    root.title("Email Attachment Downloader")

    # Configure the main window
    root.geometry("400x350")  # Width x Height
    root.resizable(False, False)  # Disable resizing

    # Variables to track checkbox states
    option1_var = tk.BooleanVar()
    option2_var = tk.BooleanVar()

    # Add checkboxes to control parts of the script
    option1_checkbox = tk.Checkbutton(root, text="Run Part 1", variable=option1_var)
    option1_checkbox.pack(pady=5)

    option2_checkbox = tk.Checkbutton(root, text="Run Part 2", variable=option2_var)
    option2_checkbox.pack(pady=5)

    # Add a button to run the script
    run_button = tk.Button(root, text="Download Attachments", command=run_script)
    run_button.pack(pady=20)

    # Button to open notes window
    notes_button = tk.Button(root, text="Open Notes", command=create_notes_window)
    notes_button.pack(pady=10)

    # Button to open instructions window
    instructions_button = tk.Button(root, text="Open Instructions", command=create_instructions_window)
    instructions_button.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_ui()

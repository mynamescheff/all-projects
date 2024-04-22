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

def create_ui():
    root = tk.Tk()
    root.title("Email Attachment Downloader")

    # Configure the main window
    root.geometry("400x250")  # Width x Height
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

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_ui()

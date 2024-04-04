import tkinter as tk
from tkinter import messagebox
import threading

# Import your script's main functionality
# from your_script import main_functionality

def run_script():
    try:
        # Assuming you encapsulate your script's functionality in this function
        # This is a placeholder, replace it with the actual call to your script's functionality
        threading.Thread(target=main_functionality).start()
        messagebox.showinfo("Success", "Script is running in the background!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main_functionality():
    # Place your script's main functionality here, or import it from your script file
    pass

def create_ui():
    root = tk.Tk()
    root.title("Email Attachment Downloader")

    # Configure the main window
    root.geometry("400x200")  # Width x Height
    root.resizable(False, False)  # Disable resizing

    # Add a button to run the script
    run_button = tk.Button(root, text="Download Attachments", command=run_script)
    run_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_ui()
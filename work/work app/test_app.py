import tkinter as tk
from tkinter import messagebox
import threading

from charges_checker import check_file_conditions
from email_dl import setup_outlook_session, download_attachments_and_save_as_msg
from acc_checker import ExcelComparator
from case_checker import CaseList

notes_window = None
instructions_window = None
notes_content = ""

def process_all_cases():
    threading.Thread(target=run_case_list).start()
    threading.Thread(target=check_conditions).start()
    threading.Thread(target=run_comparator).start()

def run_case_list():
    excel_folder = "path_to_excel_folder"
    list_folder = "path_to_list_folder"
    case_list = CaseList(excel_folder, list_folder)
    duplicates, unique_values, errors = case_list.process_excel_files()

    if errors:
        messagebox.showerror("Error", "\n".join(errors))
    if duplicates:
        messagebox.showinfo("Duplicates Found", f"Duplicate values found: {len(duplicates)}")
    else:
        messagebox.showinfo("Success", "No duplicates found. All unique values processed successfully.")

def check_conditions():
    result, mismatch = check_file_conditions("example.xlsx", 18, "GBP")
    if result:
        messagebox.showinfo("Success", "Conditions met.")
    else:
        messagebox.showinfo("Mismatch", f"Mismatch found: {mismatch}")

def run_comparator():
    combined_file = "path_to_combined_file.xlsx"
    sprawdzacz_file = "path_to_sprawdzacz_file.xlsx"
    output_path = "C:/IT project/mismatch"
    comparator = ExcelComparator(combined_file, sprawdzacz_file, output_path)
    non_matching_values, message = comparator.compare_and_append()

    if non_matching_values:
        messagebox.showinfo("Results", f"Mismatches found: {len(non_matching_values)}")
    else:
        messagebox.showinfo("Results", "No mismatches found.")
    messagebox.showinfo("Log", message)

def create_notes_window():
    global notes_window, notes_content  # Ensure notes_window is declared as global
    if not notes_window or not tk.Toplevel.winfo_exists(notes_window):
        notes_window = tk.Toplevel()
        notes_window.title("Notes")
        notes_window.geometry("300x200")
        notes_window.resizable(True, True)

        text_widget = tk.Text(notes_window, height=10, width=30)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, notes_content)

        # Function to call when the window is to be closed
        def on_closing():
            global notes_window, notes_content  # Declare as global within the function
            notes_content = text_widget.get("1.0", tk.END)  # Update the stored notes content
            notes_window.destroy()
            notes_window = None  # Reset the global variable to None after destruction

        # Bind the Escape key to the on_closing function
        notes_window.bind("<Escape>", lambda event: on_closing())

        notes_window.protocol("WM_DELETE_WINDOW", on_closing)
        notes_window.focus_set()  # Set focus on the Notes window

def create_instructions_window():
    global instructions_window
    if not instructions_window or not tk.Toplevel.winfo_exists(instructions_window):
        instructions_window = tk.Toplevel()
        instructions_window.title("Instructions")
        instructions_window.geometry("300x200")
        text_widget = tk.Text(instructions_window, height=10, width=30, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, "Follow these instructions...\n1. Do X\n2. Do Y\n3. Don't forget Z")
        text_widget.config(state=tk.DISABLED)

        # Function to handle window closure
        def on_closing():
            global instructions_window
            instructions_window.destroy()
            instructions_window = None  # Reset the global variable to None after destruction

        # Bind the Escape key to the on_closing function
        instructions_window.bind("<Escape>", lambda event: on_closing())

        instructions_window.protocol("WM_DELETE_WINDOW", on_closing)

        instructions_window.focus_set()  # Set focus on the Instructions window
        
def create_ui():
    root = tk.Tk()
    root.title("Operations Dashboard")
    root.minsize(300, 250)
    root.geometry("300x250")
    root.resizable(True, True)

    # Checkbox for marking emails as read
    mark_as_read_var = tk.BooleanVar(value=False)
    mark_as_read_checkbox = tk.Checkbutton(root, text="Mark emails as read", variable=mark_as_read_var)
    mark_as_read_checkbox.pack(pady=10)

    # Button for downloading emails
    def download_emails():
        email_address = "your_email@example.com"
        shared_mailbox_email = "shared_mailbox@example.com"
        category = "Universities"
        target_senders = ['sender1@example.com', 'sender2@example.com']
        save_confirmation = True

        outlook = setup_outlook_session(email_address)
        saved_emails, saved_attachments, error = download_attachments_and_save_as_msg(
            outlook, shared_mailbox_email, category, target_senders, save_confirmation, mark_as_read_var.get())
        
        if error:
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Success", f"{saved_emails} emails processed and {saved_attachments} attachments saved.")

    # Set a minimum size for the window to prevent making it too small.
    min_width, min_height = 300, 250
    root.minsize(min_width, min_height)
    
    # Set a maximum size for the window to prevent making it too large.
    max_width, max_height = 600, 500
    root.maxsize(max_width, max_height)
    
    # The geometry method sets the initial size of the window.
    # Adjusting it to start within the min and max size constraints.
    initial_width, initial_height = 400, 350
    root.geometry(f"{initial_width}x{initial_height}")
    root.resizable(True, True)  # Allow resizing but within the restrictions set by minsize and maxsize

    download_button = tk.Button(root, text="Download Emails", command=download_emails)
    download_button.pack(pady=10)

    process_button = tk.Button(root, text="Process All Cases", command=process_all_cases)
    process_button.pack(pady=10)

    notes_button = tk.Button(root, text="Open Notes", command=create_notes_window)
    notes_button.pack(pady=10)

    instructions_button = tk.Button(root, text="Open Instructions", command=create_instructions_window)
    instructions_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_ui()

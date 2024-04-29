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

def download_emails():
    email_address = "your_email@example.com"
    shared_mailbox_email = "shared_mailbox@example.com"
    category = "Universities"
    target_senders = ['sender1@example.com', 'sender2@example.com']
    save_confirmation = True

    outlook = setup_outlook_session(email_address)
    saved_emails, saved_attachments, error = download_attachments_and_save_as_msg(outlook, shared_mailbox_email, category, target_senders, save_confirmation)
    
    if error:
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Success", f"{saved_emails} emails processed and {saved_attachments} attachments saved.")

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
    global notes_window
    if not notes_window or not tk.Toplevel.winfo_exists(notes_window):
        notes_window = tk.Toplevel()
        notes_window.title("Notes")
        notes_window.geometry("300x200")
        text_widget = tk.Text(notes_window, height=10, width=30)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, notes_content)
        def on_closing():
            global notes_content
            notes_content = text_widget.get("1.0", tk.END)
            notes_window.destroy()
        notes_window.protocol("WM_DELETE_WINDOW", on_closing)

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
        instructions_window.protocol("WM_DELETE_WINDOW", instructions_window.destroy)

def create_ui():
    root = tk.Tk()
    root.title("Operations Dashboard")
    
    # Set a minimum size for the window to prevent making it too small.
    min_width, min_height = 300, 250
    root.minsize(min_width, min_height)
    
    # The geometry method sets the initial size of the window.
    # If you want to start with the minimum size, you can skip this line.
    root.geometry(f"{min_width}x{min_height}")
    root.resizable(True, True)  # Allow resizing but with restrictions set by minsize

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

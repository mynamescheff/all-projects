import tkinter as tk
from tkinter import messagebox
import threading
from charges_checker import check_file_conditions
from email_dl import setup_outlook_session, download_attachments_and_save_as_msg
from acc_checker import ExcelComparator
from case_checker import CaseList

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

def download_emails():
    email_address = "your_email@example.com"  # Get this from GUI input
    shared_mailbox_email = "shared_mailbox@example.com"  # Get this from GUI input
    category = "Universities"
    target_senders = ['sender1@example.com', 'sender2@example.com']
    save_confirmation = True  # Controlled by a GUI checkbox or similar

    outlook = setup_outlook_session(email_address)
    saved_emails, saved_attachments, error = download_attachments_and_save_as_msg(outlook, shared_mailbox_email, category, target_senders, save_confirmation)
    
    if error:
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Success", f"{saved_emails} emails processed and {saved_attachments} attachments saved.")


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

def part1_functionality():
    # Directly use the imported function
    result, mismatch = check_file_conditions("example.xlsx", 18, "GBP")
    if result:
        print("Conditions met.")
    else:
        print(f"Mismatch found: {mismatch}")

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

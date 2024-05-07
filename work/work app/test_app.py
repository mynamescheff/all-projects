import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import queue
from tkinter import simpledialog, scrolledtext
from charges_checker import check_file_conditions
from email_dl import setup_outlook_session, download_attachments_and_save_as_msg
from acc_checker import ExcelComparator
from case_checker import CaseList

# Global variable to track if the notes window is opened for the first time
notes_first_time = True

notes_window = None
instructions_window = None
notes_content = ""

def run_kejser(q):
    script_path = "kejser.py"  # Specify the correct path to your script
    try:
        # Run the script and capture its output and errors
        result = subprocess.run(["python", script_path], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            print("Output from kejser.py:", result.stdout)
            q.put(('done', 'Kejser.py completed successfully.\n'))
        if result.stderr:
            print("Errors from kejser.py:", result.stderr)
            q.put(('error', f"Kejser.py encountered errors:\n{result.stderr}"))
    except Exception as e:
        print("Exception in running kejser.py:", e)
        q.put(('error', f"Exception occurred: {str(e)}"))

def notify_completion(q):
    while not q.empty():
        message_type, message = q.get()
        if message_type == 'done':
            messagebox.showinfo("Notification", message)
        elif message_type == 'error':
            messagebox.showerror("Error", message)

def process_all_cases():
    q = queue.Queue()
    # Run kejser.py in a separate thread and wait for it to finish
    kejser_thread = threading.Thread(target=run_kejser, args=(q,))
    kejser_thread.start()
    kejser_thread.join()  # Ensure kejser.py completes before starting other tasks

    # Start other processing functions in separate threads
    threading.Thread(target=run_case_list).start()
    threading.Thread(target=check_conditions).start()
    threading.Thread(target=run_comparator).start()

    # Start a thread to notify the user upon completion or errors
    threading.Thread(target=notify_completion, args=(q,)).start()

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
    global notes_window, notes_content, notes_first_time
    if not notes_window or not tk.Toplevel.winfo_exists(notes_window):
        notes_window = tk.Toplevel()
        notes_window.title("Notes")
        
        # Set the position of the notes window relative to the main window
        # You can adjust '200+50' to control the position more precisely as needed
        notes_window.geometry("300x200+200+50")
        
        notes_window.resizable(True, True)
        notes_window.minsize(150, 100)  # Set minimum size
        notes_window.maxsize(600, 400)  # Set maximum size

        text_widget = tk.Text(notes_window, wrap=tk.WORD)  # Wrap text at word boundaries
        text_widget.grid(row=0, column=0, sticky='nsew')  # Make text widget expandable

        # Configure the grid layout to expand the text area proportionally with the window
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
        notes_window.focus_set()  # Set focus on the Notes window

        # Delay the popup message about the notes
        if notes_first_time:
            notes_window.after(2000, lambda: messagebox.showinfo("Note", 
                "Please note that any notes you make will disappear when closing the program."))
            notes_first_time = False  # Set the flag to False so it won't show again


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

def get_user_input():
    result = simpledialog.askstring("Input Required", "Do you want to proceed? (Y/N)")
    if result is not None and result.upper() in ['Y', 'N']:
        return result.upper()
    return None

def run_script(user_input, q):
    script_path = "path_to_your_script.py"  # Adjust the path as necessary
    try:
        process = subprocess.Popen(["python", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        # Send the user input to the script's stdin
        stdout_data, stderr_data = process.communicate(input=user_input)
        q.put(('output', stdout_data))  # Push output to the queue
        if stderr_data:
            q.put(('error', stderr_data))  # Push errors to the queue
    except Exception as e:
        q.put(('error', str(e)))
    q.put(('done', None))  # Signal that the process is done

def download_emails(q):
    user_input = get_user_input()
    if user_input:
        threading.Thread(target=run_script, args=(user_input, q), daemon=True).start()

def update_gui_from_queue(q, text_widget):
    while not q.empty():
        message_type, message = q.get()
        if message_type == 'output' and message:
            text_widget.insert(tk.END, message + "\n")
        elif message_type == 'error' and message:
            text_widget.insert(tk.END, "Error: " + message + "\n")
        elif message_type == 'done':
            text_widget.insert(tk.END, "Process Completed!\n")
    text_widget.after(100, update_gui_from_queue, q, text_widget)  # schedule the function to check the queue again


def create_ui():
    root = tk.Tk()
    root.title("Operations Dashboard")
    root.minsize(300, 250)
    root.geometry("300x250")
    root.resizable(True, True)
    text_widget = scrolledtext.ScrolledText(root, height=10)
    text_widget.pack(pady=10, padx=10)
    
    # Checkbox for marking emails as read
    mark_as_read_var = tk.BooleanVar(value=False)
    mark_as_read_checkbox = tk.Checkbutton(root, text="Mark emails as read", variable=mark_as_read_var)
    mark_as_read_checkbox.pack(pady=10)

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

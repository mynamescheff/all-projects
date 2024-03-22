import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re
import win32com.client
import time
from character_map import transform_to_swift_accepted_characters

# Outlook credentials
your_email = ''
shared_mailbox_email = ''

# Outlook category to filter emails
category_to_download = ''

# Target email addresses (replace with actual email addresses)
target_senders = ['', '', '']

# Get the absolute path of the script
script_path = os.path.dirname(os.path.abspath(__file__))

# Path to save attachments
attachment_save_path = os.path.join(script_path, 'outlook/excel')

# Path to save Outlook messages (.msg)
msg_save_path = os.path.join(script_path, 'outlook/msg')

# Create directories if they don't exist
os.makedirs(attachment_save_path, exist_ok=True)
os.makedirs(msg_save_path, exist_ok=True)

def list_unread_emails(outlook, category):
    namespace = outlook.GetNamespace("MAPI")
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()

    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # 6 corresponds to the Inbox folder
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")
        num_unread_emails = len([email for email in unread_emails])  # Convert to list and get the length
        print(f"Number of unread emails in the '{category}' category: {num_unread_emails}")

def get_unique_filename(base_path, original_filename, extension):
    counter = 2
    new_filename = original_filename
    while os.path.exists(os.path.join(base_path, f"{new_filename}{extension}")):
        new_filename = f"{original_filename} {counter}"
        counter += 1
    return new_filename

def download_attachments_and_save_as_msg(outlook, category, target_senders):
    namespace = outlook.GetNamespace("MAPI")
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()

    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # Inbox
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")
        emails_to_process = [email for email in unread_emails]

        save_confirmation = input("Do you want to save these emails? (Y/N): ").strip().lower()

        if save_confirmation == 'y':
            saved_emails = 0
            saved_attachments = 0
            not_saved_subjects = []

            for item in emails_to_process:
                email_is_correct = False  # Assume email is incorrect initially
                try:
                    sender_name_match = re.search(r'\/O=EXCHANGELABS\/OU=EXCHANGE ADMINISTRATIVE GROUP.*?-([A-Za-z]+)', item.SenderEmailAddress)
                    sender_name = sender_name_match.group(1) if sender_name_match else item.SenderEmailAddress
                    if sender_name.lower() in [sender.lower() for sender in target_senders]:
                        if item.Attachments.Count > 0:
                            for attachment in item.Attachments:
                                if attachment.FileName.lower().endswith('.xlsx'):
                                    new_filename = extract_filename_from_subject(item.Subject)
                                    new_filename = transform_to_swift_accepted_characters([new_filename])[0]
                                    new_filename = re.sub(r'[\/:*?"<>|\t]', ' ', new_filename)
                                    new_filename = re.sub(r'[^A-Za-z0-9\s\-\–;]', '', new_filename)
                                    if ';' in new_filename or ';' in item.Subject:
                                        email_is_correct = True
                                        unique_attachment_filename = get_unique_filename(attachment_save_path, new_filename, '.xlsx')
                                        attachment_path = os.path.join(attachment_save_path, f"{unique_attachment_filename}.xlsx")
                                        attachment.SaveAsFile(attachment_path)
                                        saved_attachments += 1
                except Exception as e:
                    print(f"Error processing email: {e}")
                    not_saved_subjects.append(item.Subject)

                if email_is_correct:
                    item.UnRead = False
                    item.Save()
                    saved_emails += 1
                else:
                    print(f"Email from '{sender_name}' with subject '{item.Subject}' deemed incorrect and left unread.")

            print(f"Saved emails: {saved_emails}")
            print(f"Saved attachments: {saved_attachments}")
            if not_saved_subjects:
                print("Emails not saved:")
                for subject in not_saved_subjects:
                    print(subject)
        else:
            print("No emails were saved.")
    else:
        print(f"Could not resolve the recipient: {shared_mailbox_email}")

def extract_filename_from_subject(subject):
    match = re.search(r';\s*(.*)', subject)
    if match:
        return match.group(1)
    else:
        return subject

def count_files_in_directory(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

if __name__ == "__main__":
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    namespace.Logon(your_email)

    initial_file_count = count_files_in_directory(attachment_save_path)
    print(f"Initial number of files in '{attachment_save_path}': {initial_file_count}")

    list_unread_emails(outlook, category_to_download)
    download_attachments_and_save_as_msg(outlook, category_to_download, target_senders)

    final_file_count = count_files_in_directory(attachment_save_path)
    print(f"Final number of files in '{attachment_save_path}': {final_file_count}")

    if final_file_count > initial_file_count:
        print(f"New files downloaded: {final_file_count - initial_file_count}")
    else:
        print("No new files were downloaded or some files might not have been saved correctly.")
import os
import re
import win32com.client
from character_map import transform_to_swift_accepted_characters
import argparse
import sys


# Email address of the shared mailbox
shared_mailbox_email = ""

# Category of emails to download
category_to_download = "Universities"
# List of email addresses to process
target_senders = []

## Get the absolute path of the script
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
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # Inbox
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")
        return len([email for email in unread_emails])  # Convert to list and get the length

def get_unique_filename(base_path, original_filename, extension):
    """
    Generates a unique filename by adding a consecutive number at the end 
    if a file with the same name already exists.
    """
    counter = 2
    new_filename = original_filename
    while os.path.exists(os.path.join(base_path, f"{new_filename}{extension}")):
        new_filename = f"{original_filename} {counter}"
        counter += 1
    return new_filename

def get_arguments():
    """Attempt to retrieve and parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Download emails and manage attachments.')
    parser.add_argument('--mark-as-read', type=lambda x: (str(x).lower() in ['true', 'yes', '1', 't']), nargs='?', const=True, default=False, help='Mark emails as read after processing.')
    args, unknown = parser.parse_known_args()
    return args


def download_attachments_and_save_as_msg(outlook, category, target_senders, save_emails, mark_as_read):
    namespace = outlook.GetNamespace("MAPI")
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()

    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # Inbox
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")
        emails_to_process = [email for email in unread_emails]

        print(f"Found {len(emails_to_process)} emails to process under category '{category}' with 'UnRead' = True.")

        if save_emails:
            saved_emails = 0
            saved_attachments = 0
            not_saved_subjects = []

            for item in emails_to_process:
                try:
                    sender_email = item.SenderEmailAddress
                    sender_name_match = re.search(r'/O=EXCHANGELABS/OU=EXCHANGE ADMINISTRATIVE GROUP.*?-([A-Za-z]+)', sender_email)
                    sender_name = sender_name_match.group(1) if sender_name_match else sender_email

                    print(f"Processing email from: {sender_name}")

                    if sender_name.lower() in [sender.lower() for sender in target_senders]:
                        if mark_as_read:
                            item.UnRead = False
                            item.Save()
                            print("Marked email as read.")

                        if item.Attachments.Count > 0:
                            for attachment in item.Attachments:
                                if attachment.FileName.lower().endswith('.xlsx'):
                                    new_filename = extract_filename_from_subject(item.Subject)
                                    new_filename = transform_to_swift_accepted_characters([new_filename])[0]
                                    new_filename = re.sub(r'[\/:*?"<>|\t]', ' ', new_filename)
                                    new_filename = re.sub(r'[^A-Za-z0-9\s\-\–;]', '', new_filename)

                                    if ';' not in new_filename and ';' not in item.Subject:
                                        print(f"Invalid filename generated from subject: {new_filename}")
                                        continue

                                    unique_attachment_filename = get_unique_filename(attachment_save_path, new_filename, '.xlsx')
                                    attachment_path = os.path.join(attachment_save_path, f"{unique_attachment_filename}.xlsx")
                                    attachment.SaveAsFile(attachment_path)
                                    print(f"Saved attachment: {attachment_path}")
                                    saved_attachments += 1

                                    unique_msg_filename = get_unique_filename(msg_save_path, new_filename, ' approval.msg')
                                    approval_msg_path = os.path.join(msg_save_path, f"{unique_msg_filename} approval.msg")
                                    item.SaveAs(approval_msg_path)
                                    print(f"Saved Outlook message: {approval_msg_path}")

                            saved_emails += 1

                except Exception as e:
                    print(f"Error processing email from {sender_email}: {str(e)}")
                    not_saved_subjects.append(item.Subject)

            print(f"Total saved emails: {saved_emails}")
            print(f"Total saved attachments: {saved_attachments}")
            if not_saved_subjects:
                print("Emails not saved due to errors:")
                for subject in not_saved_subjects:
                    print(subject)
        else:
            print("Email saving is disabled. No emails were saved.")
    else:
        print(f"Could not resolve the recipient: {shared_mailbox_email}")
        
def extract_filename_from_subject(subject):
    # Extract filename after the first ";" character in the subject
    match = re.search(r';\s*(.*)', subject)
    if match:
        return match.group(1)
    else:
        # If no ";" found, use the entire subject
        return subject
    
def count_files_in_directory(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def get_arguments():
    """Retrieve and parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Download emails and manage attachments.')
    parser.add_argument('--your-email', required=True, help='Email address to log into Outlook.')
    parser.add_argument('--save-emails', action='store_true', help='Save emails to disk.')
    parser.add_argument('--mark-as-read', action='store_true', help='Mark emails as read after processing.')
    return parser.parse_args()

def main():
    args = get_arguments()
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    namespace.Logon(args.your_email, '', False, True)
    
    initial_file_count = count_files_in_directory(attachment_save_path)
    num_unread_emails = list_unread_emails(outlook, category_to_download)
    print(f"Initial file count: {initial_file_count}, Unread emails: {num_unread_emails}")

    if num_unread_emails > 0:
        download_attachments_and_save_as_msg(outlook, category_to_download, target_senders, args.save_emails, args.mark_as_read)
    else:
        print("No unread emails to process.")

if __name__ == "__main__":
    main()
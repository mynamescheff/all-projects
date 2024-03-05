import os
import re
import time
import win32com.client

# Outlook credentials
your_email = 'your_email@example.com'
shared_mailbox_email = 'shared_mailbox@example.com'

# Outlook category to filter emails
category_to_download = 'YourCategory'

# Target sender names (replace with actual names)
target_senders = ['Sender1', 'Sender2', 'Sender3']

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

    # Resolve the shared mailbox recipient
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()

    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # 6 corresponds to the Inbox folder

        # Get all unread emails in the specified category
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")

        print(f"Unread emails in the '{category}' category:")
        for item in unread_emails:
            # Extract sender name from the complex sender information
            sender_name_match = re.search(r'\/O=EXCHANGELABS\/OU=EXCHANGE ADMINISTRATIVE GROUP.*?-([A-Za-z]+)', item.SenderEmailAddress)
            sender_name = sender_name_match.group(1) if sender_name_match else item.SenderEmailAddress

            print(f"Sender: {sender_name}, Subject: {item.Subject}")

def download_attachments_and_save_as_msg(outlook, category, target_senders):
    namespace = outlook.GetNamespace("MAPI")

    # Resolve the shared mailbox recipient
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()

    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # 6 corresponds to the Inbox folder

        # Get all unread emails in the specified category
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")

        # Prompt the user to confirm saving emails
        save_confirmation = input("Do you want to save these emails? (Y/N): ").strip().lower()

        if save_confirmation == 'y':
            # Initialize counters for saved emails and attachments
            saved_emails = 0
            saved_attachments = 0

            # List to store subjects of emails that were not saved
            not_saved_subjects = []

            for item in unread_emails:
                try:
                    # Extract sender name from the complex sender information
                    sender_name_match = re.search(r'\/O=EXCHANGELABS\/OU=EXCHANGE ADMINISTRATIVE GROUP.*?-([A-Za-z]+)', item.SenderEmailAddress)
                    sender_name = sender_name_match.group(1) if sender_name_match else item.SenderEmailAddress

                    # Check if the sender is in the target_senders list
                    if sender_name.lower() in [sender.lower() for sender in target_senders]:
                        # Mark the email as read
                        item.UnRead = False
                        item.Save()

                        # Wait for 5 seconds before saving the next email
                        time.sleep(5)

                        # Check if the email has attachments
                        if item.Attachments.Count > 0:
                            # Process each attachment
                            for attachment in item.Attachments:
                                # Check if the attachment has .xlsx extension
                                if attachment.FileName.lower().endswith('.xlsx'):
                                    # Extract new filename from subject
                                    new_filename = extract_filename_from_subject(item.Subject)

                                    # Replace characters that might interfere with file paths
                                    new_filename = re.sub(r'[\/:*?"<>|]', ' ', new_filename)

                                    # Check for allowed characters in the filename
                                    new_filename = re.sub(r'[^A-Za-z0-9\s\-\–;]', '', new_filename)

                                    # If ";" is not present in the subject or filename, print as invalid
                                    if ';' not in new_filename and ';' not in item.Subject:
                                        print(f"Invalid filename: {new_filename}")
                                        continue

                                    # Save attachment with sanitized filename
                                    attachment_path = os.path.join(attachment_save_path, f"{new_filename}.xlsx")
                                    try:
                                        attachment.SaveAsFile(attachment_path)
                                        saved_attachments += 1

                                        # Save the entire email with " approval" suffix
                                        approval_msg_path = os.path.join(msg_save_path, f"{new_filename} approval.msg")
                                        try:
                                            item.SaveAs(approval_msg_path)
                                        except Exception as msg_error:
                                            print(f"Error saving approval message: {msg_error}")
                                            print(f"Approval message path: {approval_msg_path}")
                                    except Exception as attachment_error:
                                        print(f"Error saving attachment: {attachment_error}")
                                        print(f"Attachment path: {attachment_path}")

                            # Increment saved emails count after processing all attachments
                            saved_emails += 1

                except Exception as e:
                    print(f"Error processing email with subject: {item.Subject}")
                    print(f"Error details: {e}")

                    # Add the subject to the list of not saved emails
                    not_saved_subjects.append(item.Subject)

            # Print the number of saved emails and attachments
            print(f"Saved emails: {saved_emails}")
            print(f"Saved attachments: {saved_attachments}")

            # Print subjects of emails that were not saved
            print("Emails not saved:")
            for subject in not_saved_subjects:
                print(subject)

        else:
            print("No emails were saved.")
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

if __name__ == "__main__":
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    namespace.Logon(your_email)

    list_unread_emails(outlook, category_to_download)

    download_attachments_and_save_as_msg(outlook, category_to_download, target_senders)

    print("Attachments downloaded and emails processed.")

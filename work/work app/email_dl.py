import os
import re
import win32com.client
from character_map import transform_to_swift_accepted_characters

# Assume these paths are set up where the script is initialized
script_path = os.path.dirname(os.path.abspath(__file__))
attachment_save_path = os.path.join(script_path, 'outlook/excel')
msg_save_path = os.path.join(script_path, 'outlook/msg')
os.makedirs(attachment_save_path, exist_ok=True)
os.makedirs(msg_save_path, exist_ok=True)

def setup_outlook_session(email_address):
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    namespace.Logon(email_address)
    return outlook

def list_unread_emails(outlook, shared_mailbox_email, category):
    namespace = outlook.GetNamespace("MAPI")
    recipient = namespace.CreateRecipient(shared_mailbox_email)
    recipient.Resolve()
    if recipient.Resolved:
        shared_mailbox = namespace.GetSharedDefaultFolder(recipient, 6)  # Inbox
        unread_emails = shared_mailbox.Items.Restrict(f"[Categories] = '{category}' AND [UnRead] = True")
        return unread_emails, None
    return None, "Could not resolve the recipient."

def download_attachments_and_save_as_msg(outlook, shared_mailbox_email, category, target_senders, save_confirmation, mark_as_read):
    try:
        emails, error = list_unread_emails(outlook, shared_mailbox_email, category)
        if error:
            return 0, 0, error

        saved_emails = 0
        saved_attachments = 0
        for email in emails:
            sender_email = email.SenderEmailAddress.lower()
            if sender_email in [sender.lower() for sender in target_senders]:
                for attachment in email.Attachments:
                    if attachment.FileName.lower().endswith('.xlsx'):
                        attachment_path = os.path.join(attachment_save_path, attachment.FileName)
                        attachment.SaveAsFile(attachment_path)
                        saved_attachments += 1
                if mark_as_read:
                    email.UnRead = False
                    email.Save()
                    saved_emails += 1
        return saved_emails, saved_attachments, None
    except Exception as e:
        return 0, 0, f"Error processing emails: {str(e)}"

# This setup allows for the functions to be directly called from a GUI handler

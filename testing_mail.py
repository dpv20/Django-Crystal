email_user = 'backoperaciones@crystal-lagoons.com'
email_password = 'rakb zwvz sokv raxt'
imap_url = 'imap.gmail.com'

import os
import imaplib
import email
from email import policy
from datetime import datetime
import re

email_user = 'backoperaciones@crystal-lagoons.com'
email_password = 'rakb zwvz sokv raxt'
imap_url = 'imap.gmail.com'

# Connect to the email server
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(email_user, email_password)
mail.select('inbox')

# Set up local directory for saving attachments
base_attachment_dir = 'fotos_mail'
if not os.path.exists(base_attachment_dir):
    os.makedirs(base_attachment_dir)

# Search for emails received today in Chile GMT-4
date = datetime.now().strftime("%d-%b-%Y")
typ, data = mail.search(None, '(ON "{}")'.format(date))

# Process emails
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1], policy=policy.default)

    # Get email subject and sanitize it for use as a folder name
    subject = msg['subject'] or 'NoSubject'
    sanitized_subject = re.sub(r'[^\w\s-]', '', subject).strip().replace(' ', '_')

    # Create a directory for the subject if it doesn't exist
    subject_dir = os.path.join(base_attachment_dir, sanitized_subject)
    if not os.path.exists(subject_dir):
        os.makedirs(subject_dir)

    # Initialize attachment number counter
    attachment_number = 1

    # Check if there are any attachments
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        
        filename = part.get_filename()
        if filename and filename.lower().endswith('.jpg'):
            filepath = os.path.join(subject_dir, f"{attachment_number}.jpg")
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            print(f'Saved {attachment_number}.jpg to {subject_dir}')
            attachment_number += 1

# Close the connection
mail.close()
mail.logout()

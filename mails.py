import imaplib
import email
from email.header import decode_header
import os
import pytz
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from main.models import Laguna, LagunaImage

def get_id_laguna_from_subject(subject):
    parts = subject.split()
    for part in parts:
        if Laguna.objects.filter(idLagunas=part).exists():
            return part
    return None

email_sender = 'dpavez@crystal-lagoons.com'
email_password = 'wzda cjzm ursc whld'


#'backoperaciones@crystal-lagoons.com'
#'rakb zwvz sokv raxt'

# Set up the email connection
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_sender, email_password)
mail.select('inbox')

# Search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split(b' ')

base_media_directory = os.path.join('C:/code/Djangopage/mysite', 'media')

# Process each email
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                try:
                    subject = subject.decode('utf-8')
                except UnicodeDecodeError:
                    subject = subject.decode('ISO-8859-1')
            
            email_date = email.utils.parsedate_to_datetime(msg["Date"])
            print(f"Processing email with Subject: '{subject}' and Date: {email_date}")

            id_laguna = get_id_laguna_from_subject(subject)

            if not id_laguna:
                sender = email.utils.parseaddr(msg['From'])[1]
                try:
                    laguna = Laguna.objects.get(mailcontacto=sender)
                    id_laguna = laguna.idLagunas
                except Laguna.DoesNotExist:
                    try:
                        laguna = Laguna.objects.get(mailcontacto2=sender)
                        id_laguna = laguna.idLagunas
                    except Laguna.DoesNotExist:
                        continue

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get_content_maintype() == 'text':
                    continue
                filename = part.get_filename()
                if not filename:
                    continue
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    counter = 1
                    filepath = os.path.join(base_media_directory, filename)
                    while os.path.exists(filepath):
                        name, ext = os.path.splitext(filename)
                        filepath = os.path.join(base_media_directory, f"{name}_{counter}{ext}")
                        counter += 1

                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    laguna_image = LagunaImage(
                        laguna_id=id_laguna,
                        photo=filepath,
                        date=email_date.date(),
                        selected=False
                    )
                    laguna_image.save()

mail.logout()

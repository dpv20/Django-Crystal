from django.db.models import Q
import email.utils
from email import policy
from datetime import datetime, timedelta
import imaplib
import pytz
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from main.models import Laguna, LagunaImage
from django.core.files.base import ContentFile
from PIL import Image
import io


class Command(BaseCommand):
    help = "Process emails to save images based on Laguna specifications"

    def handle(self, *args, **options):
        print("Starting to process emails...")

        # Email server credentials
        email_user = 'backoperaciones@crystal-lagoons.com'
        email_password = 'rakb zwvz sokv raxt'
        imap_url = 'imap.gmail.com'

        # Connect to the email server
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(email_user, email_password)
        mail.select('inbox')

        # Fetch emails received today in Chile GMT-4
        chile_tz = pytz.timezone('America/Santiago')
        date_today = datetime.now(chile_tz).strftime("%d-%b-%Y")


        ##########################################
        modificar_date = 0
        if modificar_date == 1:
            chile_tz = pytz.timezone('America/Santiago')
            now_in_chile = datetime.now(chile_tz)
            yesterday = now_in_chile - timedelta(days=1)
            date_yesterday = yesterday.strftime("%d-%b-%Y")
            date_today = date_yesterday


        print("8888888888888888888888888")
        print(date_today)
        print("8888888888888888888888888")
        ##########################################
        #18-Apr-2024
        typ, data = mail.search(None, f'(ON "{date_today}")')

        # Prepare a list of all 'subjectr' values (distinct and lowered)
        subjectr_values = set(Laguna.objects.exclude(subjectr__isnull=True).exclude(subjectr='').values_list('subjectr', flat=True))
        subjectr_values = {subj.lower().strip() for subj in subjectr_values}

        for num in data[0].split():
            typ, msg_data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1], policy=policy.default)
            
            email_subject = msg['subject'].lower()
            email_sender = email.utils.parseaddr(msg['from'])[1]

            # Check each word in subject against all 'subjectr' values
            matching_lagunas = set()
            for word in email_subject.split():
                matching_lagunas.update(Laguna.objects.filter(subjectr__iexact=word))

            # Check sender email
            matching_lagunas.update(Laguna.objects.filter(Q(mailcontacto=email_sender) | Q(mailcontacto2=email_sender)))

            print(f"Sender Email: {email_sender}")
            print(f"Email Subject: {email_subject}")
            print(f"Lagunas Matched: {len(matching_lagunas)}")
            
            for laguna in matching_lagunas:
                print(f"Processing attachments for Laguna ID: {laguna.idLagunas}")
                self.save_attachments(laguna, msg)
            print("#############################################")
        
        mail.logout()


    
    def save_attachments(self, laguna, msg):
        print("Processing attachments...")
        chile_tz = pytz.timezone('America/Santiago')
        upload_date = datetime.now(chile_tz) #- timedelta(days=1)

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.JPG']):
                file_content = ContentFile(part.get_payload(decode=True))
                img = Image.open(io.BytesIO(file_content.read()))

                #
                temp_io = io.BytesIO()
                img.save(temp_io, format=img.format, quality=100)
                #temp_io.seek(0)
                size_kb = temp_io.tell() / 1024
                print(f"Image size before final save: {size_kb:.2f} KB")
                temp_io.seek(0)
                if size_kb > 10000:  # More than 10 MB
                    quality = 10
                elif size_kb > 5000:  # Between 5 MB and 10 MB
                    quality = 25
                elif size_kb > 1000:  # Between 1 MB and 5 MB
                    quality = 50
                else:  # Less than 1 MB
                    quality = 85




                # Convert image back to ContentFile for saving
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=img.format, quality=quality)
                img_byte_arr.seek(0)  # Important: move back to the start of the BytesIO stream

                file_content = ContentFile(img_byte_arr.read())  # Read bytes from io.BytesIO and create ContentFile

                # File path and saving logic as previously defined
                formatted_filename = f"{upload_date.strftime('%Y-%m-%d')}-{filename}"
                base_dir = self.get_base_directory(laguna.idLagunas)
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                file_path = os.path.join(base_dir, formatted_filename)

                # Save the modified image content to disk
                with open(file_path, 'wb') as f:
                    f.write(file_content.read())  # Write the bytes to the file

                # Create and save the LagunaImage model instance
                laguna_image = LagunaImage(
                    laguna=laguna,
                    photo=file_path,  # Set the path to the modified image
                    date=upload_date.date(),
                    selected=False
                )
                laguna_image.save()

                print(f"Image saved as {formatted_filename} for Laguna ID: {laguna.idLagunas}")



    def generate_filepath(self, base_dir, filename, idLagunas):
        print("holi def generate_filepath")

        # Isolate the base part of the filename without extension
        base_filename = os.path.splitext(filename)[0]

        # Ensure the directory exists (create if it doesn't)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Format the date for the filename
        today_date = datetime.now().strftime("%Y-%m-%d")


        #################
        #modificacion fecha
        #today_date = "2024-04-17"
        ##################

        
        # Initialize the count based on existing files
        # This pattern assumes you want to count all files for today with the given idLagunas
        pattern = f"{today_date}-{idLagunas}-*.jpg"
        existing_files = [fn for fn in os.listdir(base_dir) if fn.endswith('.jpg') and fn.startswith(f"{today_date}-{idLagunas}")]
        count = len(existing_files) + 1
    
        # Create the new filename with today's date, idLagunas, and the new count
        new_filename = f"{today_date}-{idLagunas}-{count}.jpg"
        
        return os.path.join(base_dir, new_filename)

    

    def get_base_directory(self, idLagunas):
        if idLagunas.lower() == "con":
            return os.path.join(settings.MEDIA_ROOT, 'laguna_images/condores')
        else:
            return os.path.join(settings.MEDIA_ROOT, f'laguna_images/{idLagunas}')
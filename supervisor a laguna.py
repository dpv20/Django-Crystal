import os
import csv
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Replace 'your_project.settings' with your Django project's settings
django.setup()

# Import your models after setting up Django
from main.models import Laguna, AditivosLaguna  # Replace 'your_app.models' with the actual path to your models

def import_csv_data(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proyecto_id = row['Proyecto']
            try:
                laguna = Laguna.objects.get(idLagunas=proyecto_id)
                AditivosLaguna.objects.create(
                    proyecto=laguna,
                    leadtime=row['Leadtime'],
                    ddaDiaLts_AP2=row['DdaDiaLts_AP2'],
                    ddaDiaLts_FH1=row['DdaDiaLts_FH1']
                )
                print(f"Data imported for Laguna {laguna}")
            except Laguna.DoesNotExist:
                print(f"Laguna with idLagunas '{proyecto_id}' not found")

if __name__ == '__main__':
    file_name = "datos_aditivos_Diego.csv"  # Name of your CSV file
    import_csv_data(file_name)

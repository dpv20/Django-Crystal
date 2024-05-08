import csv
from django.core.management.base import BaseCommand
from main.models import Laguna_Stock, Laguna
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports data from CSV into Laguna_Stock model'

    def handle(self, *args, **options):
        with open('Datos aditivos_TM.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Find the corresponding Laguna instance
                try:
                    laguna = Laguna.objects.get(idLagunas=row['Proyecto'])
                except Laguna.DoesNotExist:
                    # If the Laguna does not exist, skip to next row or handle appropriately
                    self.stdout.write(self.style.WARNING(
                        f"Laguna with id {row['Proyecto']} not found."
                    ))
                    continue

                # Convert date from MM/DD/YYYY to date object
                date_obj = datetime.strptime(row['Fecha'], '%m/%d/%Y').date()

                # Create a new Laguna_Stock instance
                laguna_stock = Laguna_Stock(
                    date=date_obj,
                    laguna=laguna,
                    stock_or_supply='stock',
                    cl_ap2hi_tank=0,
                    cl_ap2hi_storage=row['AP2_T'],
                    cl_fh1lo_tank=0,
                    cl_fh1lo_storage=row['FH1_T'],
                    cl_flo12_tank=0,
                    cl_flo12_storage=row['FLO_T'],
                    cl_cotflo_tank=0,
                    cl_cotflo_storage=row['COT_T'],
                    cl_mb010_tank=0,
                    cl_mb010_storage=row['MB_T'],
                )

                # Save the instance
                laguna_stock.save()
                # Optionally, output success message
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported data for Laguna {laguna.Nombre} on {row["Fecha"]}'
                ))

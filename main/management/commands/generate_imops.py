import csv
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from main.models import Laguna, IMOP, Laguna_Stock, AditivosLaguna
from decimal import Decimal


#csv deberia tener las columnas 
#Fecha_Visita,Nota_Final,idLagunas
#DD/MM/YYYY,float,Lagunas.idLagunas
#ej: 31/12/2024,2.7,Me1

class Command(BaseCommand):
    help = 'Imports IMOP data from a CSV file'

    def handle(self, *args, **options):
        with open('Datos_notas_TM.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Attempt to retrieve the related Laguna instance
                    laguna = Laguna.objects.get(idLagunas=row['idLagunas'])
                    aditivos = AditivosLaguna.objects.filter(proyecto=laguna).first()

                    # Parse the date and adjust to the last day of the month
                    date = parse_date(datetime.strptime(row['Fecha_Visita'], '%d/%m/%Y').strftime('%Y-%m-%d'))
                    last_day = date.replace(day=28) + timedelta(days=4)
                    last_day -= timedelta(days=last_day.day)
                    
                    latest_stock = Laguna_Stock.objects.filter(
                        laguna=laguna,
                        date__year=last_day.year,
                        date__month=last_day.month
                    ).order_by('-date').first()

                    if latest_stock:
                        total_ap2 = latest_stock.cl_ap2hi_tank + latest_stock.cl_ap2hi_storage
                        total_fh1 = latest_stock.cl_fh1lo_tank + latest_stock.cl_fh1lo_storage
                    else:
                        total_ap2 = total_fh1 = Decimal('0')

                    if aditivos:
                        dda_ap2 = Decimal(aditivos.ddaDiaLts_AP2)
                        dda_fh1 = Decimal(aditivos.ddaDiaLts_FH1)
                        var_AP2HI = (total_ap2 / dda_ap2).quantize(Decimal('0.00'))
                        var_FH1LO = (total_fh1 / dda_fh1).quantize(Decimal('0.00'))
                    else:
                        var_AP2HI = 0
                        var_FH1LO = 0

                    # Create the IMOP instance
                    imop = IMOP(
                        laguna=laguna,
                        date=last_day,
                        resumen_ejecutivo="resumen ejecutivo placeholder",
                        resumen_ejecutivo_date=last_day,
                        recomendaciones="recomendaciones placeholder",
                        recomendaciones_date=last_day,
                        temas_pendientes="temas pendientes placeholder",
                        temas_pendientes_date=last_day,
                        is_completed=True,
                        nota_final=row['Nota_Final'],
                        var_FH1LO=var_FH1LO,
                        var_AP2HI=var_AP2HI,
                        PER="PER placeholder",
                        BC="BC placeholder",
                        MC="MC placeholder",
                        FIL="FIL placeholder",
                        DOS="DOS placeholder",
                        REC="REC placeholder",
                        TEL="TEL placeholder",
                        SKI="SKI placeholder",
                        ULT="ULT placeholder",
                        INF="INF placeholder",
                        LIN="LIN placeholder",
                        VISUAL="VISUAL placeholder",
                        WAT="WAT placeholder",
                        LVL="LVL placeholder",
                        ENV="ENV placeholder"
                    )

                    # Save the IMOP instance
                    imop.save()
                    imop.generate_id()  # Generate the custom ID after saving once

                    self.stdout.write(self.style.SUCCESS(f'Successfully imported IMOP for Laguna {laguna.idLagunas}'))

                except Laguna.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Skipped: Laguna with ID {row["idLagunas"]} does not exist.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
import csv
import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from main.models import Laguna

def int_or_none(value):
    try:
        return int(float(value))  # Convert to float first to handle numbers like "5.0"
    except ValueError:
        return None

def is_valid_time_format(time_str):
    if not time_str or time_str.strip() == "":
        return False
    return re.match(r'^\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?$', time_str)

def load_data_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as csv_file:  # added encoding to handle BOM
        csv_reader = csv.DictReader(csv_file)
        
        # Print the first row's keys
        first_row = next(csv_reader)
        print("Keys in the first row:", first_row.keys())
        
        # To continue reading the rest of the rows, we append the first row back
        all_rows = [first_row] + list(csv_reader)
        
        for row in all_rows:
            horario_corte_value = row.get('horariocorte', None)
            if not is_valid_time_format(horario_corte_value):
                horario_corte_value = None
            
            laguna = Laguna(
                idLagunas=row['idLagunas'],
                Nombre=row['Nombre'],
                Codigo=row['Codigo'],
                Identificador=int_or_none(row.get('Identificador', None)),
                Estado=row.get('Estado', None) and (row['Estado'].lower() == 'true'),
                Rend=row.get('Rend', None) and (row['Rend'].lower() == 'true'),
                Nombre_Proyecto=row['Nombre_Proyecto'],
                idplatanus=int_or_none(row.get('idplatanus', None)),
                ranking=int_or_none(row.get('ranking', None)),
                idioma=row['idioma'],
                mailcontacto=row['mailcontacto'],
                subjectr=row['subjectr'],
                mailcontacto2=row['mailcontacto2'],
                horariocorte=horario_corte_value,
                Water_analysis=row.get('Water_analysis', None) and (row['Water_analysis'].lower() == 'true'),
                Region=int_or_none(row.get('Region', None)),
                filtroreporte=row['filtroreporte']
            )
            
            laguna.save()

if __name__ == '__main__':
    load_data_from_csv('lagunas.csv')

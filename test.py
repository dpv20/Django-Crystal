from main.models import Laguna
for laguna in Laguna.objects.all():
    print(f"'{laguna.subjectr}'")  # Outputs the subjectr values with quotes to show spaces

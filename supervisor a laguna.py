import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Replace 'mysite.settings' with your Django project's settings
django.setup()

# Import your models after setting up Django
from main.models import Laguna, Supervisor, SupervisorLaguna  # Adjust the import path as necessary

def associate_lagunas_with_supervisors():
    for laguna in Laguna.objects.all():
        if laguna.filtroreporte:
            try:
                supervisor = Supervisor.objects.get(name=laguna.filtroreporte)
                SupervisorLaguna.objects.get_or_create(supervisor=supervisor, laguna=laguna)
                print(f'Successfully associated Laguna {laguna} with Supervisor {supervisor}')
            except Supervisor.DoesNotExist:
                print(f'Supervisor named "{laguna.filtroreporte}" not found for Laguna {laguna}')

if __name__ == '__main__':
    associate_lagunas_with_supervisors()

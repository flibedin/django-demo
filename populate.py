import os

# setup del ambiente necesario para acceder a Django
os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'ProTwo.settings')
import django
django.setup()

# ahora lo necesario para acceder al modelo y a la lib Faker
import random
from AppTwo.models import User
from faker import Faker

fakegen = Faker()


def populate( N = 5 ):

    for entry in range(N):

        # creo la fake data
        fake_first = fakegen.first_name()
        fake_last = fakegen.last_name()
        fake_email = fakegen.email()

        # creo el User
        webpg = User.objects.get_or_create( first_name = fake_first, last_name = fake_last,email = fake_email)[0]


if __name__ == '__main__':
    print( "Populating data")
    populate(20)
    print( "Listo!")

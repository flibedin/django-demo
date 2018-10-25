import os

# setup del ambiente necesario para acceder a Django
os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'ProTwo.settings')
import django
import random
import datetime
django.setup()

# ahora lo necesario para acceder al modelo y a la lib Faker
import random
from school.models import  School, Student
from AppTwo.models import Cliente
from banco.models import Cliente as Clt, Transaccion
from faker import Faker

fakegen = Faker()

# pueblo la lista de cliente
def populate_users( N = 5 ):

    for entry in range(N):

        # creo la fake data
        fake_first = fakegen.first_name()
        fake_last = fakegen.last_name()
        fake_email = fakegen.email()

        # creo el Cliente
        webpg = Cliente.objects.get_or_create( first_name = fake_first, last_name = fake_last,email = fake_email)[0]


def populate_schools( N = 5, students = 10 ):

    for entry in range(N):

        # creo la escuela
        fake_school_name = "School " + str(entry)
        fake_principal = fakegen.first_name() + " " + fakegen.last_name()
        fake_location = fakegen.address();

        # creo el colegio
        school_id = School.objects.get_or_create( name = fake_school_name, principal = fake_principal,location = fake_location)[0]

        for st in range( students ):
            fake_name = fakegen.first_name() + " " + fakegen.last_name()
            age = random.randint(7,18)
            Student.objects.get_or_create( name = fake_name, age = age, school = school_id)

def populate_banco( N = 5, transac = 10 ):

    for entry in range(N):

        # creo el cliente
        fake_nombre = fakegen.first_name()
        fake_apellido =  fakegen.last_name()
        fake_sexo = random.choice( ['H', 'M'])
        fake_direccion = fakegen.address()
        fake_sucursal = random.choice( ['01', '02', '03', '04'])

        # creo el cliente
        cliente_id = Clt.objects.get_or_create( nombre = fake_nombre, apellido = fake_apellido,
                    direccion = fake_direccion, sexo = fake_sexo, sucursal = fake_sucursal)[0]

        for st in range( random.randint(0, transac) ):
            fake_fecha = fakegen.date_between_dates( datetime.date(2018, 10, 1), datetime.date(2018, 10, 30))
            fake_monto = random.randint(1000,10000000)
            fake_tipo = random.choice( ['A', 'R'])
            Transaccion.objects.get_or_create( cliente = cliente_id, fecha = fake_fecha,
                            monto = fake_monto, tipo = fake_tipo )


if __name__ == '__main__':
    print( "Populating data")
    # populate_users(20)
    populate_schools(10, 50)
    # populate_banco( 100, 20 )
    print( "Listo!")

from django.db import models
from django.core.exceptions import ValidationError

Sucursales = ( ('01', 'Alameda'), ('02', 'Providencia'), ('03', 'Las Condes'), ('04', 'Vitacura'))


# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)

    direccion = models.CharField(max_length=256)
    sucursal = models.CharField(max_length=2,choices=Sucursales)
    sexo = models.CharField(max_length=1,choices=( ('H', 'Hombre'), ('M', 'Mujer')))

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

    class Meta:
        ordering = ['nombre']


class Transaccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.PositiveIntegerField()
    tipo = models.CharField(max_length=1,choices=( ('A', 'Abono'), ('R', 'Retiro')))

    def __str__(self):
        return "TX {} {}".format(self.fecha, self.pk)


class Hipotecario(models.Model):
    tipo_propiedad = (
        ('D', 'Departamento'),
        ('C', 'Casa'),
        ('O', 'Oficina'),
        ('S', 'Sitio'),
    )

    tipo_moneda = (
        ('U', 'UF'),
        ('$', 'Pesos')

    )

    # meses de gracia 0-11
    mes_gracia = [(i, i) for i in range(12)]

    # plazo
    plazo_credito = ( (5, '5'), (8, '8'), (10, '10'), (12, '12'), (15, '15'), (20, '20'))

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    propiedad = models.CharField(max_length=1,choices=tipo_propiedad, default=None)
    valor = models.PositiveIntegerField()
    pie = models.PositiveIntegerField()
    credito = models.PositiveIntegerField()
    plazo = models.PositiveIntegerField(choices=plazo_credito)
    gracia = models.PositiveIntegerField(choices=mes_gracia, default=0)
    moneda = models.CharField(max_length=1,choices=tipo_moneda, default='U')
    tasa = models.DecimalField(max_digits=4, decimal_places=2)
    fecha = models.DateField()
    cuota = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "HIP {} {}".format(self.cliente, self.fecha)

    # este metodo ilustra una validación a nivel de modelo de datos
    def save(self, *args, **kwargs):
        if self.pie + self.credito != self.valor:
            raise ValidationError('La suma del credito mas el pie debe ser igual al valor de la propiedad')
        else:
            super(Hipotecario, self).save(*args, **kwargs)



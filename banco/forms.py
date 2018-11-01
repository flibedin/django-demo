from django import forms
from banco.models import Transaccion, Hipotecario

# este form lo utilizo para la consulta de transacciones
class TransaccionForm(forms.ModelForm):

    class Meta():
        model = Transaccion
        fields = ( 'cliente', 'fecha', 'tipo' )
        widgets = {'fecha': forms.DateInput(attrs={'id': 'datepicker'})}


    def __init__(self, *args, **kwargs):
        super(TransaccionForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].required = False
        self.fields['fecha'].required = False
        self.fields['tipo'].required = False


class HipotecarioForm(forms.ModelForm):

    class Meta():
        model = Hipotecario
        fields = ( 'propiedad', 'valor', 'pie', 'credito', 'plazo', 'gracia')
        widgets = {'propiedad': forms.RadioSelect, 'moneda': forms.RadioSelect }
        labels = {'gracia': 'Meses de Gracia',  'plazo': 'Plazo (años)'}
        placeholder = { 'valor': 'Valor de la Propiedad (UF)'}

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor < 500:
            raise forms.ValidationError("La propiedad no puede costar menos de 500 UF")

        return valor


    # este metodo ilustra una validación a nivel de formulario
    def clean(self):
        cleaned_data = super().clean()
        pie = cleaned_data.get('pie')
        credito = cleaned_data.get('credito')

        if pie < credito * 0.2:
            self.add_error( 'pie', 'El pie no puede ser inferior al 20% del credito')

        '''
        if valor != pie + credito:
            self.add_error( 'pie', 'La suma del credito mas el pie debe ser igual al valor de la propiedad')
            self.add_error('credito', 'La suma del credito mas el pie debe ser igual al valor de la propiedad')
            self.add_error('valor', 'La suma del credito mas el pie debe ser igual al valor de la propiedad')

            raise forms.ValidationError(
                'La suma del credito mas el pie debe ser igual al valor de la propiedad'
            )
        '''





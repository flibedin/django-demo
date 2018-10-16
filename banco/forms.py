from django import forms
from banco.models import Transaccion

# este form lo utilizo para la consulta de transacciones
class TransaccionForm( forms.ModelForm):

    class Meta():
        model = Transaccion
        fields = ( 'cliente', 'fecha', 'tipo' )
        widgets = {'fecha': forms.DateInput(attrs={'id': 'datepicker'})}


    def __init__(self, *args, **kwargs):
        super(TransaccionForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].required = False
        self.fields['fecha'].required = False
        self.fields['tipo'].required = False
        self.fields['tipo'].widget.attrs.update({'class': 'form-control sm-1'})

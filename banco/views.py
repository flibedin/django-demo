from django.shortcuts import render
from django.views.generic import (
            View, TemplateView, ListView, DetailView,
            CreateView, UpdateView, DeleteView)
from banco.models import Cliente, Transaccion
from banco.forms import TransaccionForm


class ClienteList( ListView ):
    context_object_name = 'clientes'
    template_name = 'cliente_list.html'
    model = Cliente

def Query( request):

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            fecha = form.cleaned_data['fecha']
            tipo = form.cleaned_data['tipo']

            transacciones = Transaccion.objects.all();

            if cliente != '' and cliente != None:
                transacciones = transacciones.filter( cliente=cliente )
                
            if fecha != '' and fecha != None :
                transacciones = transacciones.filter( fecha=fecha)

            if tipo != '' and tipo != None :
                transacciones = transacciones.filter( tipo=tipo)


    else:
        form = TransaccionForm()
        transacciones = None

    # despliego el form para edición o ingreso
    context = { 'form': form, 'txs': transacciones }
    return render( request, "query.html", context=context )

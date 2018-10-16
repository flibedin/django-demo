from django.shortcuts import render
from django.views.generic import (
            View, TemplateView, ListView, DetailView,
            CreateView, UpdateView, DeleteView)
from banco.models import Cliente, Transaccion
from banco.forms import TransaccionForm
from django.core.paginator import Paginator
from django.core import serializers

class ClienteList( ListView ):
    context_object_name = 'clientes'
    template_name = 'cliente_list.html'
    model = Cliente
    paginate_by = 10


# este es un ejemplo de Query en base distintos campos y una grilla paginada con los resultados
def Query(request):

    transacciones = None
    paginator = None
    is_paginated = False

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            fecha = form.cleaned_data['fecha']
            tipo = form.cleaned_data['tipo']

            transacciones = Transaccion.objects.all();

            if cliente != '' and cliente != None:
                transacciones = transacciones.filter(cliente=cliente )

            if fecha != None and fecha != None :
                transacciones = transacciones.filter(fecha=fecha)

            if tipo != '' and tipo != None :
                transacciones = transacciones.filter(tipo=tipo)

            # guardo el ibjeto serializado en la sesion
            request.session['query-post'] = serializers.serialize('xml', transacciones)

            paginator = Paginator(transacciones, 5)
            transacciones = paginator.page(1)
            is_paginated = True

    else:   # GET
        form = TransaccionForm()

        # preparo el paginador
        page = request.GET.get('page') #  Get the page number
        if page == '' or page == None:
            is_paginated = False
            paginator = None
        else:
            # recupero el objeto serializado con mi dataset desde la sesion
            transacciones = []
            for obj in serializers.deserialize("xml", request.session['query-post']):
                transacciones.append( obj.object )

            # creo el paginador y recupero la pagina page
            paginator = Paginator(transacciones, 5)
            transacciones = paginator.page(page)
            is_paginated = True

    # despliego el form y grilla de resultados
    context = { 'form': form, 'txs': transacciones, 'is_paginated': is_paginated,
        'page_obj': transacciones, 'paginator': paginator }
    return render( request, "query.html", context=context )

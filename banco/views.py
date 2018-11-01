from django.shortcuts import render
from django.views.generic import (
            View, TemplateView, ListView, DetailView,
            CreateView, UpdateView, DeleteView)
from banco.models import Cliente, Transaccion, Hipotecario
from banco.forms import TransaccionForm, HipotecarioForm
from django.core.paginator import Paginator
from django.core import serializers
from . import models
from ProTwo.utils import render_to_pdf
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError



class ClienteList( ListView ):
    context_object_name = 'clientes'
    template_name = 'cliente_list.html'
    model = Cliente
    paginate_by = 10

def BancoDetailView( request, pk):

    # obtengo el cliente
    clt = Cliente.objects.get(pk=pk)

    # y el detalle de transacciones
    trx = Transaccion.objects.filter(cliente=clt)

    return render( request, "cliente_detail.html", context={ 'cliente': clt, 'tlist': trx, 'pk': pk} )

def BancoPDF( request, pk):

    # obtengo el cliente
    clt = Cliente.objects.get(pk=pk)

    # y el detalle de transacciones
    trx = Transaccion.objects.filter(cliente=clt)


    context = {
        'cliente': clt,
        'tlist': trx,
        'pk': pk
        }

    pdf = render_to_pdf('cliente_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

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

            transacciones = Transaccion.objects.all().order_by('fecha');

            if cliente != '' and cliente != None:
                transacciones = transacciones.filter(cliente=cliente )

            if fecha != None and fecha != None :
                transacciones = transacciones.filter(fecha=fecha)

            if tipo != '' and tipo != None :
                transacciones = transacciones.filter(tipo=tipo)

            # guardo el ibjeto serializado en la sesion
            request.session['query-post'] = serializers.serialize('xml', transacciones)

            if len(transacciones) > 5 :
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

def HipotecarioView(request, pk):

    # obtengo el cliente
    try:
        clt = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        raise Http404("Cliente no existe")

    if request.method == 'POST':
        form = HipotecarioForm(request.POST)
        if form.is_valid():
            h = Hipotecario()
            h.cliente = clt
            h.propiedad = form.cleaned_data['propiedad']
            h.valor = form.cleaned_data['valor']
            h.pie = form.cleaned_data['pie']
            h.credito = form.cleaned_data['credito']
            h.plazo = form.cleaned_data['plazo']
            h.gracia = form.cleaned_data['gracia']
            h.moneda = 'U'
            h.tasa = 3.44
            h.fecha = datetime.datetime.now()

            # Calculo la cuota
            h.cuota = valorCuota( h.credito, h.tasa, h.plazo )

            # guardo el resultado de la simulación
            try:
                h.save()
            except ValidationError as e:
                form.add_error(None, e.message)
                return render(request, "hipotecario.html", context={'form': form, 'cliente': clt})



            # despliego el resultado
            return render(request, "res_hipotecario.html", {'h': h, 'pk': pk })
    else:
        form = HipotecarioForm()

    context = {'form': form , 'cliente': clt}

    return render(request, "hipotecario.html", context=context)


def valorCuota(principal,interest_rate,duration):
    n = duration*12             #total number of months
    r = interest_rate/(100*12) #interest per month
    monthly_payment = principal*((r*((r+1)**n))/(((r+1)**n)-1)) #formula for compound interest applied on mothly payments.
    return monthly_payment
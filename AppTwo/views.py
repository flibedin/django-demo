from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from AppTwo.models import Cliente
from AppTwo.forms import ClienteForm
from django.urls  import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index( request ):
    return render( request, "index.html", context={} )


def help( request ):
    my_dict = { 'help': "Que ayuda necesitas"}
    return render( request, "AppTwo/help.html", context=my_dict )

@login_required
def users( request):
    user_list = Cliente.objects.all()
    context = { 'user_list': user_list }

    return render( request, "users.html", context=context )


# en esta vista edito un Cliente
@login_required
def edit( request, pk = None):

    if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                try:
                    u = Cliente.objects.get( pk=pk)
                    u.first_name = first_name
                    u.last_name = last_name
                    u.email = email
                    u.save()
                except Cliente.DoesNotExist:
                    u = Cliente( first_name=first_name, last_name=last_name, email=email )
                    u.save()

                return users( request )
    else:

        if pk == None:
            form = ClienteForm()       # quiero crear un nuevo Usuario
        else:
            # estoy editando un Usuario que ya existe, lo recupero de la BD
            u = Cliente.objects.get( pk=pk )

            # obtengo el email desde la BD
            form=ClienteForm( None, initial={'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} )

    # despliego el form para edición o ingreso
    context = { 'form': form }
    return render( request, "edit.html", context=context )



@login_required
def special( request ):
    return HttpResponse( "Estas logged in, nice!")

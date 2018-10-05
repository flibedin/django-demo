from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from AppTwo.models import Cliente
from AppTwo.forms import ClienteForm, UserForm, UserProfileInfoForm
from django.urls  import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
def edit( request, first_name = None, last_name = None):

    
    if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                try:
                    u = Cliente.objects.get( first_name=first_name, last_name=last_name)
                    u.email = email
                    u.save()
                except Cliente.DoesNotExist:
                    u = Cliente( first_name=first_name, last_name=last_name, email=email )
                    u.save()

                return users( request )
    else:

        if first_name == None or last_name == None:
            form = ClienteForm()       # quiero crear un nuevo Usuario
        else:
            # estoy editando un Usuario que ya existe, lo recupero de la BD
            u = Cliente.objects.get( first_name=first_name, last_name=last_name)

            # obtengo el email desde la BD
            form=ClienteForm( None, initial={'first_name': first_name, 'last_name': last_name, 'email': u.email} )

    # despliego el form para edición o ingreso
    context = { 'form': form }
    return render( request, "edit.html", context=context )


# Registro de usuarios
def register( request):

    registered = False
    if request.method == "POST":
        user_form = UserForm( data=request.POST )
        profile_form = UserProfileInfoForm( data=request.POST )

        if user_form.is_valid() and profile_form.is_valid() :

            user = user_form.save()
            user.set_password( user.password)
            user.save()

            profile = profile_form.save( commit = False)
            profile.user = user         # lo asocio al user recien grabado

            # veo si trae una imagen
            if 'profile_pic' in request.FILES :
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print( user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render( request, "registration.html",
            context={'registered': registered, 'user_form': user_form, 'profile_form': profile_form } )


# autentica a un usuario
def user_login( request ):

    if request.method == "POST" :
        username = request.POST.get( 'username')
        password = request.POST.get( 'password')

        # aca lo autentifico con Django
        user = authenticate( username=username, password=password)

        if user:
            if user.is_active:
                login( request, user )
                return HttpResponseRedirect( reverse('views.index'))
            else:
                return HttpResponse( "LA CUENTA NO ESTA ACTIVA")
        else:
            print( "Alguien trato de entrar al sistema y no lo logro!")
            print( "Username: {} y Password: {}".format( username, password ))
            return HttpResponse( "Login invalido")
    else:
        return render( request, "login.html", {})

@login_required
def user_logout( request ):
    logout( request )
    return HttpResponseRedirect( reverse('views.index'))

@login_required
def special( request ):
    return HttpResponse( "Estas logged in, nice!")

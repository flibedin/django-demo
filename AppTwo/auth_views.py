from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from AppTwo.models import  UserProfileInfo
from AppTwo.forms import  UserForm, UserProfileInfoForm, UserFullForm
from django.urls  import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Registro de un nuevo usuario
def register( request ):

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
def user_detail( request ):

    # tengo que obtener el UserDetailInfo a partir del user
    userInfo = UserProfileInfo.objects.get( user=request.user )
    return render( request, "user_detail.html", context={ 'user_profile': userInfo } )

@login_required
def user_edit( request ):

    # Este es el form que administra la actualización de datos de un usuario registrado
    # tengo que obtener el UserDetailInfo a partir del user
    userInfo = UserProfileInfo.objects.get( user=request.user )
    u = userInfo.user


    if request.method == "POST":

        user_form = UserFullForm( request.POST )

        if user_form.is_valid() :

            u.first_name = user_form.cleaned_data['first_name']
            u.last_name = user_form.cleaned_data['last_name']
            u.email = user_form.cleaned_data['email']
            u.save()



            '''
            profile = profile_form.save( commit = False)
            profile.user = user         # lo asocio al user recien grabado

            # veo si trae una imagen
            if 'profile_pic' in request.FILES :
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            '''

            # lo retorno a la vista original
            return HttpResponseRedirect( reverse('user_detail'))
    else:

        # este es el GET
        user_form = UserFullForm(
               initial={'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} )


    return render( request, "user_edit.html", context={ 'user_form': user_form, 'user_profile': userInfo } )



@login_required
def user_logout( request ):
    logout( request )
    return HttpResponseRedirect( reverse('views.index'))

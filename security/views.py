from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from security.models import  UserProfileInfo
from security.forms import  UserForm, UserProfileInfoForm, UserFullForm
from django.urls  import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import json
import urllib.request
import os
from django.core.mail import send_mail



# Registro de un nuevo usuario
def register( request ):

    registered = False
    if request.method == "POST":
        user_form = UserForm( data=request.POST )
        profile_form = UserProfileInfoForm( data=request.POST )

        if user_form.is_valid() and profile_form.is_valid() :

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user         # lo asocio al user recien grabado

            # veo si trae una imagen
            if 'profile_pic' in request.FILES :
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

            # envio mail avisando el registro
            '''
            send_mail(
                'Nuevo registro en sitio de FL',
                'Hola, has sido registrado exitosamente en el sitio',
                'flibedinsky.smtp@gmail.com',
                [user.email],
                fail_silently=True )
            '''


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

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if not result['success']:
            return HttpResponse( 'Invalid reCAPTCHA. Please try again.' )

        # aca lo autentifico con Django
        user = authenticate( username=username, password=password)

        if user:
            if user.is_active:
                login( request, user )
                next = request.GET.get('next')
                if next != None and next != 'None' and next != '':
                    return HttpResponseRedirect( next )
                else:
                    return HttpResponseRedirect( reverse('views.index'))
            else:
                return HttpResponse( "LA CUENTA NO ESTA ACTIVA")
        else:
            print( "Alguien trato de entrar al sistema y no lo logro!")
            print( "Username: {} y Password: {}".format( username, password ))
            return HttpResponse( "Login invalido")
    else:
        next = request.GET.get( 'next')
        return render( request, "login.html", {'next': next})


@login_required
def user_detail( request ):

    # tengo que obtener el UserDetailInfo a partir del user
    try:
        userInfo = UserProfileInfo.objects.get( user=request.user )
    except UserProfileInfo.DoesNotExist:
        userInfo = UserProfileInfo()
        userInfo.user = request.user

    return render( request, "user_detail.html", context={ 'user_profile': userInfo } )


# Este form administra la actualización de datos de un usuario registrado
@login_required
def user_edit( request ):

    # Obtengo el UserInfo a partir del user
    try:
        userInfo = UserProfileInfo.objects.get( user=request.user )
    except UserProfileInfo.DoesNotExist:
        userInfo = UserProfileInfo()
        userInfo.user = request.user

    u = userInfo.user

    if request.method == "POST":

        user_form = UserFullForm(request.POST)

        # veo si trae una imagen
        if 'profile_pic' in request.FILES:

            # borro  la imagen antigua
            old_image = userInfo.profile_pic
            userInfo.profile_pic = request.FILES['profile_pic']
            userInfo.save()

            # borro la imagen antigua
            filename = os.path.join(settings.MEDIA_ROOT, old_image.name)
            if os.path.exists(filename):
                os.remove(filename)

        elif user_form.is_valid():

            u.first_name = user_form.cleaned_data['first_name']
            u.last_name = user_form.cleaned_data['last_name']
            u.email = user_form.cleaned_data['email']

            u.save()

            # lo retorno a la vista original
            return HttpResponseRedirect( reverse('security:user_detail'))
    else:

        # este es el GET, debo llenar el user_form con los datos de la BD
        user_form = UserFullForm(
               initial={'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} )

    return render( request, "user_edit.html", context={ 'user_form': user_form, 'user_profile': userInfo } )




@login_required
def user_logout( request ):
    logout( request )
    return HttpResponseRedirect(reverse('views.index'))



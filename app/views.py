# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#Candela Gullo: Importa el modelo User de Django, que representa a los usuarios registrados en la aplicación.
from django.contrib.auth.models import User

#Candela Gullo: Permite mostrar mensajes tipo alerta en la web (por ejemplo, mensajes de éxito o error).
from django.contrib import messages

#Candela Gullo: Te da acceso a la configuración del proyecto (settings.py).
from django.conf import settings

#Candela Gullo: Función integrada de Django para enviar correos electrónicos desde el servidor.
from django.core.mail import send_mail


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):

    #Candela Gullo: Hice que la lista retorne las tarjetas modificadas y definidas en la pagina "Services"
    images = services.getAllImages()

    #Candela Gullo: retorna las imagenes en la pagina "home.html"
    return render(request, 'home.html', { 'images': images })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    #Candela Gullo: si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = services.getAllImages()
        
    #Candela Gullo: filtra por nombre parcial ignorando mayúsculas/minúsculas
        images = [img for img in images if name in img.name.lower()]

        return render(request, 'home.html', { 'images': images})
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
    
    
    
# Candela Gullo: esta funcion es para cuando un usuario accede a /register o similar
def register(request):
    # Candela Gullo: Una vez que se envie el formulario (Usando el metodo POST)
    if request.method == 'POST':
        # Candela Gullo: Extrae los datos enviados desde el formulario HTML
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Candela Gullo: Verifica si el nombre de usuario ya está en uso
        if User.objects.filter(username=username).exists():
            # Candela Gullo: Si no muestra un mensaje de error y vuelve a la misma página
            messages.error(request, 'El nombre de usuario ya existe. Elegí otro.')
            return redirect('register')  #Candela Gullo:  "register" es el nombre de la ruta en urls.py a la cual redirije si esta mal

        # Candela Gullo: Si el usuario no existe, se crea uno nuevo
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Candela Gullo: Se crea un mensaje personalizado que se enviará por correo.
        # Candela Gullo: Que incluye un saludo al nuevo usuario, su nombre de usuario y su contraseña.
        mensaje = f"Bienvenido {first_name}!\n\nTus credenciales son:\nUsuario: {username}\nContraseña: {password}"

        send_mail(
            'Registro exitoso en la aplicación',  # Candela Gullo: Asunto del correo.
            mensaje,                              # Candela Gullo: Cuerpo del correo (el mensaje definido arriba).
            settings.DEFAULT_FROM_EMAIL,          # Candela Gullo: Dirección del remitente (definida en settings.py).
            [email],                              # Candela Gullo: Lista con el destinatario (correo que ingresó el usuario).
            fail_silently=False,                  # Candela Gullo: Si ocurre un error, lo muestra.
        )

        #Candela Gullo: Muesta un mensaje de verificacion al usuario
        messages.success(request, 'Registro exitoso. Revisa tu correo electrónico.')

        # Candela Gullo: Luego de crear el usuario, redirige al login
        return redirect('login')  # Candela Gullo: "login" también es una ruta configurada en urls.py

    # Candela Gullo: Si se accede con GET (por ejemplo, al entrar a la página desde el navegador)
    # Candela Gullo: simplemente se muestra el formulario de registro
    return render(request, 'registration/register.html')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')

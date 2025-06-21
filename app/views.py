# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#Noelia B. Importamos la función desdes services.py , para ello hay que escribir todas las rutas desde la rama principal
#hasta llegar al archivo donde esta la funcion que necesitamos 
from app.layers.services.services import filterByType

#Candela Gullo: Importa el modelo User de Django, que representa a los usuarios registrados en la aplicacion.
from django.contrib.auth.models import User

#Candela Gullo: Permite mostrar mensajes tipo alerta en la web (por ejemplo, mensajes de éxito o error).
from django.contrib import messages

#Candela Gullo: Te da acceso a la configuración del proyecto (settings.py).
from django.conf import settings

#Candela Gullo: Función integrada de Django para enviar correos electrónicos desde el servidor.
from django.core.mail import send_mail

#Candela Gullo: Importa el modelo Favourite desde el archivo models.py que está en el mismo modulo por eso el punto . al comienzo.
from .models import Favourite



def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):

    #Candela Gullo: Hice que la lista retorne las tarjetas modificadas y definidas en la pagina "Services"
    images = services.getAllImages()
    
    #Candela Gullo: esta lista va a retornar los favoritos del usuario
    favourites = getAllFavouritesByUser()

    #Candela Gullo: retorna las imagenes en la pagina "home.html"
    return render(request, 'home.html', {'images': images,'favourites': favourites})


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
#Noelia B. tengo que importar la funcion filterByType del archivo services.py que retorta card filtradas 
        images = filterByType (type) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
#Noelia.B. Esta Funcion (filter_by_type) luego usada en "home.html" va a permitir que los botones de calsificacion "AGUA","PLANTA","FUEGO" se ejecuten  
    
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

        # Candela Gullo: Verifica si el nombre de usuario ya esta en uso
        if User.objects.filter(username=username).exists():
            # Candela Gullo: Si no muestra un mensaje de error y vuelve a la misma pagina
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

        # Candela Gullo: Se crea un mensaje personalizado que se mandara por correo.
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
def saveFavourite(request):
    if request.method == 'POST':

        #Candela Gullo: extraemos los datos del formulario de HTML.
        poke_id = request.POST.get('id')
        name = request.POST.get('name')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        base_experience = request.POST.get('base_experience')
        types = request.POST.getlist('types')
        image = request.POST.get('image')

        # Candela Gullo: verifica si el favorito ya existe para ese usuario.
        exists = Favourite.objects.filter(user=request.user, name=name).exists()

        #Candela Gullo: Si no existe, se crea y guarda un nuevo objeto Favourite con los datos del Pokémon y el usuario actual.
        if not exists:
            Favourite.objects.create(
                id=poke_id,
                name=name,
                height=height,
                weight=weight,
                base_experience=base_experience,
                types=types,
                image=image,
                user=request.user
            )
        #Candela Gullo: Si ya existe, se muestra un mensaje informativo indicando que ya fue agregado antes.
        else:
            messages.info(request, 'Ese Pokémon ya está en tus favoritos.')

    #Candela Gullo: despues te redirije a la pagina de galeria
    return redirect('home')

# Mostrar la lista de favoritos
@login_required
def getAllFavouritesByUser(request):

    #Candela Gullo: Obtiene todos los favoritos que pertenecen al usuario actualmente autenticado.
    favoritos = Favourite.objects.filter(user=request.user)

    return render(request, 'favourites.html', {'favourite_list': favoritos})

# Eliminar un favorito
@login_required
def deleteFavourite(request):

    #Candela Gullo: Esta función también espera un método POST y obtiene el ID del Pokémon a eliminar.
    if request.method == 'POST':
        fav_id = request.POST.get('id')

        # Candela Gullo: Buscamos el favorito del usuario actual con el ID dado
        fav = Favourite.objects.filter(id=fav_id, user=request.user).first()

        if fav:
            fav.delete()
            # Candela Gullo: Mensaje de éxito si se elimina correctamente
            messages.success(request, 'El favorito fue eliminado.')
        else:
            # Candela Gullo: Mensaje de error si no se encuentra el favorito
            messages.error(request, 'No se encontró el favorito o no te pertenece.')

    # Candela Gullo: Redirige a la lista de favoritos
    return redirect('favoritos')  

@login_required
def exit(request):
    logout(request)
    return redirect('home')

# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services.services import filterByType
#Noelia B. Importamos la función desdes services.py , para ello hay que escribir todas las rutas desde la rama principal
#hasta llegar al archivo donde esta la funcion que necesitamos 


def index_page(request):
    return render(request, 'index.html')


# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    #Cndela G. hice que la lista retorne las tarjetas modificadas y definidas en la pag "Services"
    images= services.getAllImages()
  

    return render(request, 'home.html', { 'images': images })


# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
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
#Candela G. esta funciones para cuando un usuario accede a register o similar 
def register(request):
#Una vez que se envie el formulario (usando el metodo POST)
    if request.method == 'POST':
#Extraer los datos enviados desde el formulario HTML
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
#Verificar si el nombre de usuario ya esta en uso 
        if User.objects.filter(username=username).exists():
#si no muestra un mensaje de error  y vuelve a la misma pagina 
            messages.error(request, 'El nombre de usuario ya existe. Elegí otro.')
            return redirect('register')
# Si el usuario no existe, se crea uno nuevo 
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
#Luego de crear el usuario, redirige al login 
        return redirect ("login") #login tambien es una ruta configurada en urls.py

#Si se accede con GET (por ejemplo, al entrar a la pag desde el navegador)
#simplemente se muestra el formulario de registro 
    return render (request,'registration/register.html' )




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
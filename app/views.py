# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.transport import transport
from .layers.utilities import translator
from django.http import HttpResponse
from django.contrib import messages

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list,})

# función utilizada en el buscador.
def search(request):
    # Obtenemos el texto ingresado en el buscador, le sacamos espacios al principio y final, y lo pasamos a minúsculas
    # Traemos todas las tarjetas de Pokémon (ya procesadas) sin filtrar
    name = request.POST.get('query', '').strip().lower()
    images= []
# si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images=services.filterByCharacter(name)
    else:
        images= services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list})


# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '').lower()
    if type != '':
        images = services.filterByType(type)
    else:
        images = services. getAllImages () # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list,})
    
    #return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list=[]
    favourite_list=services.getAllFavourites(request)
    return render(request,'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    #si la solicitud es del tipo post (es decir, el usuario ha enviado un formulario)
    if request.method == 'POST':
        #llamamos al servicio que guarda una carta como favorita por el usurio 
        services.saveFavourite(request)
        
    #redirigimos al usuario a la pagina despues de guardar la carta favorita
    return redirect('home')

@login_required
def deleteFavourite(request):# llama desde la API a la función deleteFavourite del servicio, que a su vez llama al repositorio.
    # Verifica si la solicitud es POST y si se ha enviado un ID de favorito
    
    if request.method == 'POST':
        #llamamos al servicio que elimina una carta de los favoritos del usuario
        fav_id=request.POST.get('id')
        if fav_id:
            success= services.deleteFavourite(request,fav_id)
            if success:
                return redirect('favoritos')
            else:
                return HttpResponse ("no se pudo eliminar el favorito.", status=400)
    #redirigimos al usuario a la pagina de favoritos despues de eliminar la carta
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')
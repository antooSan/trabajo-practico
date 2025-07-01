# capa de servicio/lógica de negocio....

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests
from requests.exceptions import ConnectionError
from app.models import Favourite
from sqlite3 import IntegrityError

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    images= transport.getAllImages()
    # 2) convertir cada img. en una card.
    lista_cards=[]
    for elemento in images:
        card=translator.fromRequestIntoCard(elemento)
        types_aux=[]
        for t in card.types:
            types_aux.append(get_type_icon_url_by_name(t))
        card.types_imgs= types_aux
 # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
        lista_cards.append(card)
    return lista_cards


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []
    for card in getAllImages():
     # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():
            filtered_cards.append(card)
    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []
    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
            filtered_cards.append(card)
    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)  # transforma el POST en Card
    fav.user = get_user(request)                     # asigna usuario
    return repositories.save_favourite(fav)         # guarda el favorito en BD

# obtener favoritos
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    
    user = get_user(request)
    favourite_list = repositories.get_all_favourites(user)
    mapped_favourites = []
    
    for favourite in favourite_list:
        card = translator.fromRepositoryIntoCard(favourite)
        mapped_favourites.append(card)

    return mapped_favourites

# borrar favorito por su id
def deleteFavourite(request,  favId):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) 

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
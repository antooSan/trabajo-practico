# capa DAO de acceso/persistencia de datos....

from sqlite3 import IntegrityError
from app.models import Favourite


def save_favourite(fav):
    try:
        # Verificamos si ya existe un favorito con ese nombre para el usuario
        exists = Favourite.objects.filter(user=fav.user, name=fav.name).exists()
        if exists:
            print("El favorito ya existe para este usuario.")
            return None  # o podés devolver un mensaje o señal especial

        fav_db = Favourite.objects.create(
            id=fav.id,
            name=fav.name,
            types=str(fav.types),
            height=fav.height,
            weight=fav.weight,
            base_experience=fav.base,
            image=fav.image,
            user=fav.user
        )
        return fav_db
    except IntegrityError as e:
        print(f"Error de integridad al guardar el favorito: {e}")
        return None
    except KeyError as e:
        print(f"Error de datos al guardar el favorito: Falta el campo {e}")
        return None

def get_all_favourites(user):
    return list(Favourite.objects.filter(user=user).values(
        'id', 'name', 'height', 'weight', 'types','base_experience', 'image'
    ))


def delete_favourite(fav_id):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe o no pertenece al usuario.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
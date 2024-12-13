import json
from fastapi import HTTPException

def load_data():

    "Funcion encargada de leer los datos que se encuentran en local"

    with open('movies.json', 'r') as file:
        movies = json.load(file)
    return movies 


def save_data(new_data : dict):

    "Funcion que escribe en la base local"

    with open('movies.json', 'w') as file:
        json.dump(new_data, file, indent=4)

    
def load_users():
    """
    Carga de usuarios
    """
    with open('users.json','r') as f:
        return json.load(f)
    

def filter_movies(movies, filter_key, filter_value):
    """
    Función para filtrar películas
    """
    try:
        if filter_key == "title":
            return [movie for movie in movies if movie['title'].strip().lower() == filter_value.strip().lower()]
        elif filter_key == "year":
            return [movie for movie in movies if movie['year'] == int(filter_value)]
        elif filter_key == "genre":
            return [movie for movie in movies if filter_value.strip().lower() in [g.strip().lower() for g in movie['genres']]]
        else:
            raise ValueError("Filtro no válido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar películas: {e}")
    

def validate_admin(user):
    """
    Validación de permisos
    """
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    


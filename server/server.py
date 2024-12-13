from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests
import os
import json
from utils import load_data, save_data, load_users, filter_movies, validate_admin

url = 'https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json'

app = FastAPI()
security = HTTPBasic()

file_dir = "movies.json"
file_path = os.path.isfile(file_dir)


# Verificamos si el archivo ya está en nuestro path, si no, lo descargamos
if not os.path.exists(file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        with open('movies.json', 'w') as file:  # Guardamos el archivo descargado
            json.dump(data, file, indent=4)
        print("Archivo descargado y guardado correctamente")
    except Exception as e:  # Capturamos el error si lo hubiese
        print(f"Error al descargar el archivo: {e}")
else:
    print("El archivo ya existe en el path")

# Ruta base
@app.get("/")
def root():
    return {"message": "Servidor en funcionamiento... Bienvenido"}

# Ruta para login
@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    users = load_users()
    for user in users:
        if user['username'] == credentials.username and user['password'] == credentials.password:
            return user
    raise HTTPException(status_code=401, detail="Invalid username or password")

# Ruta para obtener todo el catálogo de películas
@app.get("/movies")
def get_movies():
    try:
        movies = load_data()
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {e}")

# Búsqueda de película por título
@app.get("/movies/title/{title}")
def get_movie_by_title(title: str, user: dict = Depends(login)):
    try:
        movies = load_data()
        result = filter_movies(movies, "title", title)
        if not result:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {e}")

# Búsqueda de película por año
@app.get("/movies/year/{year}")
def get_movies_by_year(year: int, user: dict = Depends(login)):
    try:
        movies = load_data()
        result = filter_movies(movies, "year", year)
        if not result:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {e}")

# Búsqueda de película por género
@app.get("/movies/genre/{genre}")
def get_movies_by_genre(genre: str, user: dict = Depends(login)):
    try:
        movies = load_data()
        result = filter_movies(movies, "genre", genre)
        if not result:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {e}")

# Ruta para agregar una nueva película al catálogo
@app.post("/movies")
def add_movie(movie: dict, user: dict = Depends(login)):

    validate_admin(user)
    try:
        movies = load_data()
        movies.append(movie)
        save_data(movies)
        return {"message": "Película agregada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la película: {e}")

# Ruta para eliminar una película por título
@app.delete("/movies/title/{title}")
def delete_movie_by_title(title: str, user: dict = Depends(login)):

    validate_admin(user)
    try:
        movies = load_data()
        movies_total = [movie for movie in movies if movie['title'].strip().lower() != title.strip().lower()]
        if len(movies_total) == len(movies):
            raise HTTPException(status_code=404, detail="Película no encontrada")
        save_data(movies_total)
        return {"message": "Película eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la película: {e}")

# Ruta para actualizar una película por título
@app.put("/movies/title/{title}")
def update_movie_by_title(title: str, updated_movie: dict, user: dict = Depends(login)):

    validate_admin(user)
    try:
        movies = load_data()
        found = False
        for movie in movies:
            if movie['title'].strip().lower() == title.strip().lower():
                movie.update(updated_movie)
                found = True
                break
        if not found:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        save_data(movies)
        return {"message": "Película actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la película: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="192.168.56.1", port=8000, reload=True)

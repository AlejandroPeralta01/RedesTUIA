import requests
import flet as ft
import json

# IP ajustable
BASE_IP = "127.0.0.1:8000"  

def format_movies_info(movies : list) -> str:
    """
    Recibe una lista de películas y retorna un string con la información formateada.

    """
    formatted_movies = []

    for movie in movies:
        # Extraer la información con valores predeterminados
        title = movie.get("title", "Sin título")
        year = movie.get("year", "Año desconocido")
        cast = ", ".join(movie.get("cast", []))
        genres = ", ".join(movie.get("genres", []))

        # Crear el texto formateado para una película
        formatted_movie = (
            f"Título: {title}\n"
            f"Año: {year}\n"
            f"Elenco: {cast}\n"
            f"Géneros: {genres}\n"
        )

        formatted_movies.append(formatted_movie)

    # Combinar todas las películas en un único string
    return "\n".join(formatted_movies)

# Front
def main(page: ft.Page):
    page.title = "App de Películas"
    page.window_width = 600
    page.window_height = 600

    def login():
        """
        Inicio de sesión de usuario. Envía una solicitud POST al servidor con las credenciales ingresadas

        """
        username = username_input.value
        password = password_input.value
        response = requests.post(f"http://{BASE_IP}/login", auth=(username, password))
        if response.status_code == 200:
            user = response.json()
            page.session.set("user", user)
            show_menu(user)
        else:
            result_text.value = "Login fallido. Verifica tu nombre de usuario y contraseña."
        page.update()

    def show_menu(user):
        """
        Muestra el munú principal de la aplicación segun el rol del usuario.
        """
        page.clean()
        if user['role'] == "comun":
            page.add(
                ft.ListView(                
                    controls=[
                    ft.Row([title_input, ft.TextButton("Buscar por título", on_click=search_movie)]),
                    ft.Row([year_input, ft.TextButton("Buscar por año", on_click=search_movie_by_year)]),
                    ft.Row([genre_input, ft.TextButton("Buscar por género", on_click=search_movie_by_genre)]),
                    result_text
                    ]
                    
                )    
            )
        else:  # admin
            page.add(
                ft.ListView(                
                    controls=[
                    ft.Row([title_input, year_input, cast_input, genres_input, ft.TextButton("Agregar película", on_click=add_movie)]),
                    ft.Row([title_input, year_input, cast_input, genres_input, ft.TextButton("Modificar película", on_click=modify_movie)]),
                    ft.Row([title_input, ft.TextButton("Eliminar película", on_click=delete_movie)]),
                    ft.Row([title_input, ft.TextButton("Buscar por título", on_click=search_movie)]),
                    ft.Row([year_input, ft.TextButton("Buscar por año", on_click=search_movie_by_year)]),
                    ft.Row([genre_input, ft.TextButton("Buscar por género", on_click=search_movie_by_genre)]),
                    result_text
                    ]
        
                )
            )
        page.update()

    def search_movie():
        """
        Permite buscar una pelicula por título. Realiza una solicitud GET al servidor para obtener los datos de la película
        """
        title = title_input.value
        user = page.session.get("user")
        response = requests.get(f"http://{BASE_IP}/movies/title/{title}", auth=(user['username'], user['password']))
        if response.status_code == 200:
            data = response.json()    
            result_text.value = format_movies_info(data)
        else:
            result_text.value = "Película no encontrada."
        page.update()

    def search_movie_by_year():
        """
        Permite buscar una pelicula por año. Realiza una solicitud GET al servidor para obtener los datos de la película
        """
        year = year_input.value
        if not year.isdigit():
            result_text.value = "Año inválido. Por favor, introduce un año válido."
            page.update()
            return
        user = page.session.get("user")
        response = requests.get(f"http://{BASE_IP}/movies/year/{year}", auth=(user['username'], user['password']))
        if response.status_code == 200:
            data = response.json()
            result_text.value = format_movies_info(data)
        else:
            result_text.value = "Películas no encontradas."
        page.update()

    def search_movie_by_genre():
        """
        Permite buscar películas por género. Envía una solicitud GET al servidor para obtener las películas que coinciden
        con el género ingresado.
        """
        genre = genre_input.value
        user = page.session.get("user")
        response = requests.get(f"http://{BASE_IP}/movies/genre/{genre}", auth=(user['username'], user['password']))
        if response.status_code == 200:
            data = response.json()
            result_text.value = format_movies_info(data)
        else:
            result_text.value = "Películas no encontradas."
        page.update()

    def add_movie():
        """
        Permite agregar una nueva película al sistema.
        Toma los datos ingresados por el usuario (título, año, elenco, géneros),
        los valida, y envía una solicitud POST al servidor para agregar la película. 
        """       
        title = title_input.value
        year = year_input.value
        cast = cast_input.value.split(',')
        genres = genres_input.value.split(',')

        if not year.isdigit():
            result_text.value = "Año inválido. Por favor, introduce un año válido."
            page.update()
            return

        movie = {"title": title, "year": int(year), "cast": cast, "genres": genres}
        user = page.session.get("user")
        response = requests.post(f"http://{BASE_IP}/movies", json=movie, auth=(user['username'], user['password']))
        if response.status_code == 201:
            result_text.value = "Película agregada correctamente."
        else:
            result_text.value = "Error al agregar película."
        page.update()

    def modify_movie():
        """
        Permite modificar los datos de una película existente.
        Toma los valores ingresados por el usuario y envía una solicitud PUT al servidor
        con los datos actualizados. Muestra un mensaje indicando si la actualización fue exitosa.
        """
        title = title_input.value
        updated_movie = {
            "year": year_input.value,
            "cast": cast_input.value.split(','),
            "genres": genres_input.value.split(',')
        }
        user = page.session.get("user")
        response = requests.put(f"http://{BASE_IP}/movies/title/{title}", json=updated_movie, auth=(user['username'], user['password']))
        if response.status_code == 200:
            result_text.value = "Película actualizada correctamente."
        else:
            result_text.value = "Error al actualizar película."
        page.update()

    def delete_movie():
        """
        Permite eliminar una película del sistema.
        Envía una solicitud DELETE al servidor con el título de la película.
        """
        title = title_input.value
        user = page.session.get("user")
        response = requests.delete(f"http://{BASE_IP}/movies/title/{title}", auth=(user['username'], user['password']))
        if response.status_code == 200:
            result_text.value = "Película eliminada correctamente."
        else:
            result_text.value = "Error al eliminar película."
        page.update()

    # Campos de entrada
    username_input = ft.TextField(label="Usuario")
    password_input = ft.TextField(label="Contraseña", password=True)
    title_input = ft.TextField(label="Título")
    year_input = ft.TextField(label="Año")
    cast_input = ft.TextField(label="Elenco (separado por comas)")
    genres_input = ft.TextField(label="Géneros (separado por comas)")
    genre_input = ft.TextField(label="Género")

    result_text = ft.Text("")

    # Layout inicial
    page.add(
        ft.ListView(
            controls=[
                ft.Text("Login"),
                ft.Column([
                    username_input, 
                    password_input, 
                    ft.TextButton("Iniciar sesión", on_click=login)
                    ]),
                result_text,
            ]
        )
    )
    

ft.app(target=main)

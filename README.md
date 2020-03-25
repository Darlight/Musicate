# EmpireMusic
A streaming service utilising SQL and Python with kivy
Instalacion de postgres con python:
En la cmd instalar lo siguiente:
pip install psycogp2

Luego, para conectarse a una base de datos de postgresSQL se deberá modificar la variable con los siguientes parametros:

con = psycopg2.connect(
	host = "localhost" (Generalmente es localhost),
	database = "nombre de la base de datos",
	user = "username del superusuario" (Generalmente es postgres),
	password = "contraseña del superusuario"
)

Instalacion de Kivy

En la cmd instalar las siguientes dependencias:

python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*

python -m pip install kivy_deps.gstreamer==0.1.*

Luego, instalar kivy:

python -m pip install kivy==1.11.1

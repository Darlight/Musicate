import psycopg2 
import fprint
import sys

#connect to de database
con = psycopg2.connect(
    host = "localhost", 
    database = "Proyecto2", 
    user = "postgres", 
    password = "Soymuyguapo")

#create a cursor
cur = con.cursor()
menu = ("\n\t1. Artistas con más álbumes publicados",
"\t2. Generos con más canciones",
"\t3. Duración de cada playlist",
"\t4. Canciones de mayor duracion con la informacion de sus artistas",
"\t5. Artistas que han registrado mas canciones",
"\t6. Promedio de duracion de canciones por genero",
"\t7. Cantidad de artistas diferentes por playlist",
"\t8. Artistas con mas diversidad de generos musicales",
"\t9. Total de ventas por semana dado un rango de fechas",
"\t10. Los N artistas con las mayores ventas para un rango de fechas",
"\t    (La fecha y N artistas deben ser ingresados por el usuario)",
"\t11. Total de ventas por genero para un rango de fechas",
'\t12. Las N canciones con mas reproducciones para un artista',
"\t13. Buscar cancion",
"\t14. Buscar artista",
"\t15. Agregar usuario",
"\t16. Buscar usuario",
"\t17. Agregar cancion",
"\t18. Agregar album",
"\t19. Agregar artista",
"\t20. Login con usuario existente",
"\t21. Modificar cancion",
"\t22. Modificar album",
"\t23. Modificar artista",
"\t24. Eliminar cancion",
"\t25. Eliminar album",
"\t26. Eliminar artista",
"\t27. Buscar album",
"\t28. Salir")

print("BIENVENIDO A MUSICATE")
print("Ingrese la opcion que desea buscar:")
for i in menu:
    print(i)
opcion = int(input())


while (opcion != 28):
    #Artistas con mas albumes publicados
    if (opcion == 1):
        cur.execute("SELECT artist.name, COUNT(album.albumid) FROM artist INNER JOIN album ON artist.artistid = album.artistid GROUP BY artist.name ORDER BY COUNT(album.albumid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Generos con mas canciones
    elif (opcion == 2):
        cur.execute("SELECT genre.name AS Genero, COUNT (genre.name) FROM Track INNER JOIN Genre ON Track.genreid = Genre.genreid GROUP BY Genre.name ORDER BY COUNT(Genre.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Duracion de cada playlist
    elif (opcion == 3):
        cur.execute("SELECT p.name AS Playlist, SUM(t.milliseconds) AS Duration FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY p.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Canciones de mayor duracion con la informacion de sus artistas
    elif (opcion == 4):
        cur.execute("SELECT t.name AS Cancion, t.milliseconds AS Duracion_en_milisegundos, a.artistid, a.name FROM track t INNER JOIN Artist a ON t.composer = a.name ORDER BY t.milliseconds DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]} \t{r[2]} \t{r[3]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Artistas que han registrado mas canciones
    elif (opcion == 5):
        cur.execute("SELECT a.name AS Artista, COUNT(t.trackid) AS Canciones FROM Artist a INNER JOIN Track t ON a.name = t.composer GROUP BY a.name ORDER BY COUNT(t.trackid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Promedio de duracion de canciones por genero
    elif (opcion == 6):
        cur.execute("SELECT g.name AS Genero, AVG(t.milliseconds) AS Promedio_duracion_en_milisegundos FROM Track t INNER JOIN Genre g ON t.genreid = g.genreid GROUP BY g.name ORDER BY AVG(t.milliseconds) DESC")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Cantidad de artistas diferentes por playlist
    elif (opcion == 7):
        cur.execute("SELECT g.name, COUNT(g.name) FROM (SELECT p.name AS Name, COUNT(t.albumid) AS Artists FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY (p.name, t.albumid)) g GROUP BY g.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Artistas con mas diversidad de generos musicales
    elif (opcion == 8):
        cur.execute("SELECT a.name, COUNT(a.name) FROM (SELECT Artist.artistid as artist,track.genreid as genre FROM ARTIST JOIN Album ON Album.ArtistId=Artist.ArtistId JOIN TRACK ON Track.AlbumId=Album.AlbumId GROUP BY(artist.artistID,track.genreid)) G JOIN Artist a ON G.artist=a.artistid JOIN Genre ON G.genre=Genre.genreid GROUP BY (a.name) ORDER BY COUNT(a.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Total de ventas por semana dado un rango de fechas
    elif (opcion == 9):
        fecha1 = input("Ingrese la fecha de inicio: ")
        fecha2 = input("Ingrese la fecha final:")
        cur.execute("CREATE OR REPLACE VIEW weeksales AS SELECT invoice.invoiceid, invoicedate, invoicelineid, trackid, unitprice, quantity, EXTRACT(WEEK FROM invoicedate) as week, EXTRACT(YEAR FROM invoicedate) as year FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid")
        con.commit()
        cur.execute("SELECT sum(unitprice), year, week FROM weeksales WHERE invoicedate < %s AND invoicedate > %s GROUP BY year, week ORDER BY year, week", (fecha2, fecha1,))
        opcion1 = cur.fetchall()
        print("\nVentas\tAño\tSemana")
        for r in opcion1:
            print(f"{r[0]} \t{r[1]} \t{r[2]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Los N artistas con las mayores ventas para un rango de fechas
    #(La fecha y N artistas deben ser ingresados por el usuario)
    elif (opcion == 10):
        cur.execute("CREATE OR REPLACE VIEW mostSoldArtist AS SELECT artist.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN album ON album.albumid = track.albumid INNER JOIN artist ON artist.artistid = album.artistid")
        con.commit()
        N = input("Ingrese la cantidad de artistas que desea ver: ")
        fecha1 = input("Ingrese la fecha de inicio: ")
        fecha2 = input("Ingrese la fecha final: ")

        cur.execute("SELECT name, count(*) FROM mostSoldArtist WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC LIMIT %s", (fecha2, fecha1, N,))
        opcion1 = cur.fetchall()
        print("\n\tNombre\t\tCantidad de ventas")
        contador = 0
        for r in opcion1:
            contador += 1
            print(str(contador) + ".\t", f"{r[0]} \t{r[1]}")
        
        for i in menu:
            print(i)
        opcion = int(input())

    #Total de ventas por genero para un rango de fechas
    elif (opcion == 11):
        cur.execute("CREATE OR REPLACE VIEW mostSoldGenres AS SELECT genre.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN genre ON track.genreid = genre.genreid")
        con.commit()

        fecha1 = input("Ingrese la fecha de inicio: ")
        fecha2 = input("Ingrese la fecha final: ")
        cur.execute("SELECT name, count(*) FROM mostSoldGenres WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC", (fecha2, fecha1,))
        opcion1 = cur.fetchall()

        print("\nGenero\tTotal de ventas")
        for r in opcion1:
            print(f"{r[0]}\t{r[1]}")

        for i in menu:
            print(i)
        opcion = int(input())

    #Las N canciones con mas reproducciones para un artista
    elif (opcion == 12):
        print("Todavia no esta listo")
        for i in menu:
            print(i)
        opcion = int(input())

    #Buscar cancion
    elif (opcion == 13):
        cancion = input("Ingrese el nombre de la cancion: ")
        cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name ILIKE %s LIMIT 10", (cancion,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        for i in menu:
            print(i)
        opcion = int(input())

    #Buscar artista
    elif (opcion == 14):
        artista = input("Ingrese el nombre del artista: ")
        cur.execute("SELECT a.artistid, a.name FROM artist a WHERE a.name ILIKE %s LIMIT 10", (artista,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        for i in menu:
            print(i)
        opcion = int(input())

    #Agregar usuario
    elif (opcion == 15):
        cur.execute("SELECT MAX(userid) FROM users ")
        opcion1 = cur.fetchall()
        newid = 0
        for r in opcion1:
            newid = r[0] + 1
        name = input("Ingrese su nombre: ")
        lastname = input("Ingrese su apellido: ")
        user = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el correo electronico: ")
        password = input("Ingrese la contrasena: ")

        role = input("Ingrese el rol del usuario: ")
        cur.execute("SELECT role.roleid FROM role WHERE role.name = %s ", (role,))
        opcion1 = cur.fetchall()
        roleid = 0
        for r in opcion1:
            roleid = r[0]

        cur.execute("INSERT INTO Users(userid, name, lastname, email, username, password, roleid) VALUES (%s, %s, %s, %s, %s, %s, %s)", (newid, name, lastname, email, user, password, roleid))
        con.commit()
        print("Se ha registrado el usuario")

        for i in menu:
            print(i)
        opcion = int(input())

    #Buscar usuario
    elif (opcion == 16):
        user = input("Ingrese el nombre del usuario: ")
        cur.execute("SELECT u.userid, u.username, u.email, u.password, u.role FROM Users u WHERE u.username = %s", (user,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}  {r[2]}  {r[3]}  {r[4]}")
        
        for i in menu:
            print(i)
        opcion = int(input())

    #Agregar cancion
    elif (opcion == 17):
        cur.execute("SELECT MAX(trackid) FROM track ")
        opcion1 = cur.fetchall()
        trackid = 0
        for r in opcion1:
            trackid = r[0] + 1

        name = input("Ingrese el nombre de la cancion: ")

        album = input("Ingrese el nombre del album: ")
        cur.execute("SELECT album.albumid FROM album WHERE album.title = %s ", (album,))
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0]
        
            
        mediatype = input("Ingrese mediatype: ")
        cur.execute("SELECT mediatype.mediatypeid FROM mediatype WHERE mediatype.name = %s ", (mediatype,))
        opcion1 = cur.fetchall()
        mediatypeid = 0
        for r in opcion1:
            mediatypeid = r[0]

        genre = input("Ingrese el nombre de genero: ")
        cur.execute("SELECT genre.genreid FROM genre WHERE genre.name = %s ", (genre,))
        opcion1 = cur.fetchall()
        genreid = 0
        for r in opcion1:
            genreid = r[0]

        composer = input("Ingrese el nombre del artista: ")
        milliseconds = input("Ingrese la duracion de la cancion en milisegundos: ")
        size = input("Ingrese el tamano de la cancion en bytes: ")
        unitprice = input("Ingrese el valor de la cancion ($): ")

        cur.execute("INSERT INTO track(trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, size, unitprice))
        con.commit()
        print("Se ha guardado la cancion")

        for i in menu:
            print(i)
        opcion = int(input())

    #Agregar album
    elif (opcion == 18):
        cur.execute("SELECT MAX(albumid) FROM album ")
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0] + 1

        title = input("Ingrese el nombre del album: ")
        
        artist = input("Ingrese el nombre del artista: ")
        cur.execute("SELECT artist.artistid FROM artist WHERE artist.name = %s ", (artist,))
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0]
        
        cur.execute("INSERT INTO album(albumid, title, artistid) VALUES (%s, %s, %s)", (albumid, title, artistid))
        con.commit()
        print("Se ha guardado el album")

        for i in menu:
            print(i)
        opcion = int(input())

    #Agregar artista
    elif (opcion == 19):
        cur.execute("SELECT MAX(artistid) FROM artist ")
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0] + 1

        name = input("Ingrese el nombre del artista: ")

        cur.execute("INSERT INTO artist(artistid, name) VALUES (%s, %s)", (artistid, name))
        con.commit()
        print("Se ha guardado el artista")

        for i in menu:
            print(i)
        opcion = int(input())

    #Login con usuario existente
    elif (opcion == 20):
        username = input("Ingrese su usario: ")
        password = input("Ingrese su contrasena: ")
        
        cur.execute("SELECT * FROM users u WHERE username = %s AND password = %s", (username, password,))
        opcion1 = cur.fetchall()
        uconfirm = ""
        pconfirm = ""
        for r in opcion1:
            uconfirm = r[0]
            pconfirm = r[1]

        if ((uconfirm != "") and (pconfirm != "")):
            print("Se ha iniciado sesion correctamente")
        else:
            print("Verifica que tu usuario y contrasena esten bien")
        
        for i in menu:
            print(i)
        opcion = int(input())

    #Modificar la informacion de una cancion
    if (opcion == 21):
        name1 = input("Ingrese el nombre de la cancion que desea modificar: ")
        cur.execute("SELECT track.trackid FROM track WHERE track.name = %s ", (name1,))
        opcion1 = cur.fetchall()
        trackid = 0
        for r in opcion1:
            trackid = r[0]

        newname = input("Ingrese el nuevo nombre de la cancion: ")

        album = input("Ingrese el album de la cancion: ")
        cur.execute("SELECT album.albumid FROM album WHERE album.title = %s ", (album,))
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0]

        mediatype = input("Ingrese el mediatype de la cancion: ")
        cur.execute("SELECT mediatype.mediatypeid FROM mediatype WHERE mediatype.name = %s ", (mediatype,))
        opcion1 = cur.fetchall()
        mediatypeid = 0
        for r in opcion1:
            mediatypeid = r[0]

        genre = input("Ingrese el genero de la cancion: ")
        cur.execute("SELECT genre.genreid FROM genre WHERE genre.name = %s ", (genre,))
        opcion1 = cur.fetchall()
        genreid = 0
        for r in opcion1:
            genreid = r[0]

        composer = input("Ingrese el artista de la cancion: ")
        milliseconds = input("Ingrese la duracion de la cancion: ")
        size = input("Ingrese el tamano de la cancion en bytes: ")
        unitprice = input("Ingrese el precio de la cancion: ")

        cur.execute("UPDATE Track SET name = %s, albumid=%s, mediatypeid=%s, genreid=%s, composer=%s, milliseconds=%s, bytes=%s, unitprice=%s WHERE trackid=%s", (newname, albumid, mediatypeid, genreid, composer, milliseconds, size, unitprice, trackid,))
        con.commit()
        print("Se ha actualizado la cancion en la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Modificar album
    elif (opcion == 22):
        title = input("Ingrese el nombre del album que desea modificar: ")
        cur.execute("SELECT album.albumid FROM album WHERE album.title = %s ", (title,))
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0]

        newtitle = input("Ingrese el nuevo nombre del album: ")

        artist = input("Ingrese el artista del album: ")
        cur.execute("SELECT artist.artistid FROM artist WHERE artist.name = %s ", (artist,))
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0]

        cur.execute("UPDATE album SET title = %s, artistid=%s WHERE albumid=%s", (newtitle, artistid, albumid,))
        con.commit()
        print("Se ha actualizado el album en la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Modificar artista
    elif (opcion == 23):
        name = input("Ingrese el nombre del artista que desea modificar: ")
        cur.execute("SELECT artist.artistid FROM artist WHERE artist.name = %s ", (name,))
        opcion1 = cur.fetchall()
        artistid = ""
        for r in opcion1:
            artistid = r[0]

        newname = input("Ingrese el nuevo nombre del artista: ")

        cur.execute("UPDATE Artist SET name=%s WHERE artistid=%s", (newname, artistid))
        con.commit()
        print("Se ha actualizado el artista en la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Eliminar cancion
    elif (opcion == 24):
        name = input("Ingrese el nombre de la cancion que desea eliminar: ")
        
        cur.execute("DELETE FROM track WHERE track.name=%s", (name, ))
        con.commit()
        print("Se ha eliminado la cancion de la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Eliminar album
    elif (opcion == 25):
        title = input("Ingrese el nombre del album que desea eliminar: ")
        
        cur.execute("DELETE FROM album WHERE title=%s", (title, ))
        con.commit()
        print("Se ha eliminado el album de la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Eliminar artista
    elif (opcion == 26):
        name = input("Ingrese el nombre del artista que desea eliminar: ")
        
        cur.execute("DELETE FROM artist WHERE name=%s", (name, ))
        con.commit()
        print("Se ha eliminado el artista de la base de datos")

        for i in menu:
            print(i)
        opcion = int(input())

    #Buscar album
    elif (opcion == 27):
        album = input("Ingrese el nombre del album: ")
        cur.execute("SELECT a.albumid, a.title FROM album a WHERE a.title ILIKE %s LIMIT 10", (album,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        for i in menu:
            print(i)
        opcion = int(input())
    elif (opcion == 28):
        for i in menu:
            print(i)
        opcion = int(input())

#close the cursor
cur.close()

#close the connection
con.close()



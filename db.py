import psycopg2 
import fprint
import sys

#connect to de database
con = psycopg2.connect(
    host = "localhost", 
    database = "Proyecto", 
    user = "postgres", 
    password = "Soymuyguapo")

#create a cursor
cur = con.cursor()
menu = "\n\t1. Artistas con más álbumes publicados\n\t2. Generos con más canciones\n\t3. Duración de cada playlist\n\t4. Canciones de mayor duracion con la informacion de sus artistas\n\t5. Artistas que han registrado mas canciones\n\t6. Promedio de duracion de canciones por genero\n\t7. Cantidad de artistas diferentes por playlist\n\t8. Artistas con mas diversidad de generos musicales\n\t9. Buscar cancion\n\t10. Buscar artista\n\t11. Agregar usuario\n\t12. Buscar usuario\n\t13. Agregar cancion\n\t14. Agregar album\n\t15. Agregar artista\n\t16. Login con usuario existente\n\t17. Modificar cancion\n\t18. Modificar album\n\t19.Modificar artista\n\t20. Salir"

print("BIENVENIDO A MUSICATE")
print("Ingrese la opcion que desea buscar:")
print(menu)
opcion = int(input())
while (opcion != 20):
    #Artistas con mas albumes publicados
    if (opcion == 1):
        cur.execute("SELECT artist.name, COUNT(album.albumid) FROM artist INNER JOIN album ON artist.artistid = album.artistid GROUP BY artist.name ORDER BY COUNT(album.albumid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Generos con mas canciones
    elif (opcion == 2):
        cur.execute("SELECT genre.name AS Genero, COUNT (genre.name) FROM Track INNER JOIN Genre ON Track.genreid = Genre.genreid GROUP BY Genre.name ORDER BY COUNT(Genre.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Duracion de cada playlist
    elif (opcion == 3):
        cur.execute("SELECT p.name AS Playlist, SUM(t.milliseconds) AS Duration FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY p.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Canciones de mayor duracion con la informacion de sus artistas
    elif (opcion == 4):
        cur.execute("SELECT t.name AS Cancion, t.milliseconds AS Duracion_en_milisegundos, a.artistid, a.name FROM track t INNER JOIN Artist a ON t.composer = a.name ORDER BY t.milliseconds DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]} \t{r[2]} \t{r[3]}")

        print(menu)
        opcion = int(input())

    #Artistas que han registrado mas canciones
    elif (opcion == 5):
        cur.execute("SELECT a.name AS Artista, COUNT(t.trackid) AS Canciones FROM Artist a INNER JOIN Track t ON a.name = t.composer GROUP BY a.name ORDER BY COUNT(t.trackid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Promedio de duracion de canciones por genero
    elif (opcion == 6):
        cur.execute("SELECT g.name AS Genero, AVG(t.milliseconds) AS Promedio_duracion_en_milisegundos FROM Track t INNER JOIN Genre g ON t.genreid = g.genreid GROUP BY g.name ORDER BY AVG(t.milliseconds) DESC")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Cantidad de artistas diferentes por playlist
    elif (opcion == 7):
        cur.execute("SELECT g.name, COUNT(g.name) FROM (SELECT p.name AS Name, COUNT(t.albumid) AS Artists FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY (p.name, t.albumid)) g GROUP BY g.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]}")

        print(menu)
        opcion = int(input())

    #Artistas con mas diversidad de generos musicales
    elif (opcion == 8):
        cur.execute("SELECT a.name, COUNT(a.name) FROM (SELECT Artist.artistid as artist,track.genreid as genre FROM ARTIST JOIN Album ON Album.ArtistId=Artist.ArtistId JOIN TRACK ON Track.AlbumId=Album.AlbumId GROUP BY(artist.artistID,track.genreid)) G JOIN Artist a ON G.artist=a.artistid JOIN Genre ON G.genre=Genre.genreid GROUP BY (a.name) ORDER BY COUNT(a.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())

    #Buscar cancion
    elif (opcion == 9):
        cancion = input("Ingrese el nombre de la cancion: ")
        cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name ILIKE %s LIMIT 10", (cancion,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        print(menu)
        opcion = int(input())

    #Buscar artista
    elif (opcion == 10):
        artista = input("Ingrese el nombre del artista: ")
        cur.execute("SELECT a.artistid, a.name FROM artist a WHERE a.name ILIKE %s LIMIT 10", (artista,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        print(menu)
        opcion = int(input())

    #Agregar usuario
    elif (opcion == 11):
        cur.execute("SELECT MAX(userid) FROM users ")
        opcion1 = cur.fetchall()
        newid = 0
        for r in opcion1:
            newid = r[0] + 1
        user = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el correo electronico: ")
        password = input("Ingrese la contrasena: ")
        role = input("Ingrese el rol del usuario: ")
        cur.execute("INSERT INTO Users(UserID, Username, email, password, role) VALUES (%s, %s, %s, %s, %s)", (newid, user, email, password, role))
        con.commit()
        print("Se ha registrado el usuario")

        print(menu)
        opcion = int(input())

    #Buscar usuario
    elif (opcion == 12):
        user = input("Ingrese el nombre del usuario: ")
        cur.execute("SELECT u.userid, u.username, u.email, u.password, u.role FROM Users u WHERE u.username = %s", (user,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}  {r[2]}  {r[3]}  {r[4]}")
        
        print(menu)
        opcion = int(input())

    #Agregar cancion
    elif (opcion == 13):
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

        print(menu)
        opcion = int(input())

    #Agregar album
    elif (opcion == 14):
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

        print(menu)
        opcion = int(input())

    #Agregar artista
    elif (opcion == 15):
        cur.execute("SELECT MAX(artistid) FROM artist ")
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0] + 1

        name = input("Ingrese el nombre del artista: ")

        cur.execute("INSERT INTO artist(artistid, name) VALUES (%s, %s)", (artistid, name))
        con.commit()
        print("Se ha guardado el artista")

        print(menu)
        opcion = int(input())

    #Login con usuario existente
    elif (opcion == 16):
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
        
        print(menu)
        opcion = int(input())

    #Modificar la informacion de una cancion
    if (opcion == 17):
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

        print(menu)
        opcion = int(input())

    #Modificar album
    elif (opcion == 18):
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

        print(menu)
        opcion = int(input())

    #Modificar artista
    elif (opcion == 19):
        name = input("Ingrese el nombre del artista que desea modificar: ")
        cur.execute("SELECT artist.artistid FROM artist WHERE artist.name = %s ", (name,))
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0]

        newname = input("Ingrese el nuevo nombre del artista: ")

        cur.execute("UPDATE Artist SET name=%s WHERE artistid=%s", (newname, artistid))
        con.commit()
        print("Se ha actualizado el artista en la base de datos")

        print(menu)
        opcion = int(input())
    else:
        print(menu)
        opcion = int(input())

#close the cursor
cur.close()

#close the connection
con.close()

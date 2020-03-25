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
menu = "\n\t1. Artistas con más álbumes publicados\n\t2. Generos con más canciones\n\t3. Duración de cada playlist\n\t4. Canciones de mayor duracion con la informacion de sus artistas\n\t5. Artistas que han registrado mas canciones\n\t6. Promedio de duracion de canciones por genero\n\t7. Cantidad de artistas diferentes por playlist\n\t8. Artistas con mas diversidad de generos musicales\n\t9. Buscar cancion\n\t10. Buscar artista\n\t11. Agregar usuario\n\t12. Buscar usuario\n\t13. Agregar cancion\n\t14. Agregar album\n\t15. Agregar artista\n\t16. Salir"

print("BIENVENIDO A MUSICATE")
print("Ingrese la opcion que desea buscar:")
print(menu)
opcion = int(input())
while (opcion != 16):
    if (opcion == 1):
        cur.execute("SELECT artist.name, COUNT(album.albumid) FROM artist INNER JOIN album ON artist.artistid = album.artistid GROUP BY artist.name ORDER BY COUNT(album.albumid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 2):
        cur.execute("SELECT genre.name AS Genero, COUNT (genre.name) FROM Track INNER JOIN Genre ON Track.genreid = Genre.genreid GROUP BY Genre.name ORDER BY COUNT(Genre.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 3):
        cur.execute("SELECT p.name AS Playlist, SUM(t.milliseconds) AS Duration FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY p.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 4):
        cur.execute("SELECT t.name AS Cancion, t.milliseconds AS Duracion_en_milisegundos, a.artistid, a.name FROM track t INNER JOIN Artist a ON t.composer = a.name ORDER BY t.milliseconds DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]} \t{r[2]} \t{r[3]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 5):
        cur.execute("SELECT a.name AS Artista, COUNT(t.trackid) AS Canciones FROM Artist a INNER JOIN Track t ON a.name = t.composer GROUP BY a.name ORDER BY COUNT(t.trackid) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 6):
        cur.execute("SELECT g.name AS Genero, AVG(t.milliseconds) AS Promedio_duracion_en_milisegundos FROM Track t INNER JOIN Genre g ON t.genreid = g.genreid GROUP BY g.name ORDER BY AVG(t.milliseconds) DESC")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 7):
        cur.execute("SELECT g.name, COUNT(g.name) FROM (SELECT p.name AS Name, COUNT(t.albumid) AS Artists FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY (p.name, t.albumid)) g GROUP BY g.name")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t\t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 8):
        cur.execute("SELECT a.name, COUNT(a.name) FROM (SELECT Artist.artistid as artist,track.genreid as genre FROM ARTIST JOIN Album ON Album.ArtistId=Artist.ArtistId JOIN TRACK ON Track.AlbumId=Album.AlbumId GROUP BY(artist.artistID,track.genreid)) G JOIN Artist a ON G.artist=a.artistid JOIN Genre ON G.genre=Genre.genreid GROUP BY (a.name) ORDER BY COUNT(a.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    elif (opcion == 9):
        cancion = input("Ingrese el nombre de la cancion: ")
        cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name = %s", (cancion,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        print(menu)
        opcion = int(input())
    elif (opcion == 10):
        artista = input("Ingrese el nombre del artista: ")
        cur.execute("SELECT a.artistid, a.name FROM artist a WHERE a.name = %s", (artista,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}")
        
        print(menu)
        opcion = int(input())
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
    elif (opcion == 12):
        user = input("Ingrese el nombre del usuario: ")
        cur.execute("SELECT u.userid, u.username, u.email, u.password, u.role FROM Users u WHERE u.username = %s", (user,))
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]}  {r[1]}  {r[2]}  {r[3]}  {r[4]}")
        
        print(menu)
        opcion = int(input())
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
        unitprice = input("Ingrese el valor de la cancion")

        cur.execute("INSERT INTO track(trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,)", (trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, size, unitprice))
        con.commit()
        print("Se ha guardado la cancion")

        print(menu)
        opcion = int(input())
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
    elif (opcion == 15):
        cur.execute("SELECT MAX(artistid) FROM artist ")
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0] + 1

        name = input("Ingrese el nombre del artista: ")

        cur.execute("INSERT INTO artist(artistid, name) VALUES (%s, %s,)", (artistid, name))
        con.commit()
        print("Se ha guardado el artista")

        print(menu)
        opcion = int(input())
    else:
        print(menu)
        opcion = int(input())

#close the cursor
cur.close()

#close the connection
con.close()
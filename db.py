import psycopg2 

#connect to de database
con = psycopg2.connect(
    host = "localhost", 
    database = "Proyecto", 
    user = "postgres", 
    password = "")

#create a cursor
cur = con.cursor()
menu = "\n\t1. Artistas con más álbumes publicados\n\t2. Generos con más canciones\n\t3. Duración de cada playlist\n\t4. Canciones de mayor duracion con la informacion de sus artistas\n\t5. Artistas que han registrado mas canciones\n\t6. Promedio de duracion de canciones por genero\n\t7. Cantidad de artistas diferentes por playlist\n\t8. Artistas con mas diversidad de generos musicales\n\t9. Salir"

print("BIENVENIDO A MUSICATE")
print("Ingrese la opcion que desea buscar:")
print(menu)
opcion = int(input())
while (opcion != 9):
    if (opcion == 1):
        cur.execute("SELECT artist.artistid, COUNT (album.albumid) FROM artist INNER JOIN album ON artist.artistid = album.artistid ORDER BY COUNT(album.albumid) DESC LIMIT 5")
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
        cur.execute("SELECT p.name AS Playlist, SUM(Track.milliseconds) AS Duration FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY p.name")
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
        print("SELECT g.name, COUNT(g.name) FROM (SELECT p.name AS Name, COUNT(t.albumid) AS Artists FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY (p.name, t.albumid)) g GROUP BY g.name")

        print(menu)
        opcion = int(input())
    elif (opcion == 8):
        cur.execute("SELECT a.name, COUNT(a.name) FROM (SELECT a.artistid AS Artist, t.genreid AS Genre FROM Artist a INNER JOIN album ON album.artistid = a.artistid INNER JOIN track t ON t.albumid = album.albumid GROUP BY (a.artistid, t.genreid)) g INNER JOIN artist a ON g.artist = a.artistid INNER JOIN genre ON g.genre = genre.genreid GROUP BY COUNT(a.name) DESC LIMIT 5")
        opcion1 = cur.fetchall()
        for r in opcion1:
            print(f"{r[0]} \t{r[1]}")

        print(menu)
        opcion = int(input())
    else:
        print(menu)
        opcion = int(input())

#close the cursor
cur.close()

#close the connection
con.close()

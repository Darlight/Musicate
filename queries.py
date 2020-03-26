"""
Universidad del Valle
Sección 20
Grupo - 08
Josue Sagastume 18173
Diego Solorzano 18151
Mario Perdomo 18029
queries.py
"""
# Queries in string

#Queries para usuario
getUsers = "SELECT * FROM User INNER JOIN Role_Permission ON User.id = Rol_Permission.userid WHERE User.role <> 'admin'"
getUsersPermission = 'SELECT * FROM Rol_Permission'
getUser_Username = "SELECT * FROM User INNER JOIN UserPermissions ON User.id=UserPermissions.UserId WHERE Username=parameter AND password=parameter2 AND canLogin='TRUE'"
addUser = 'INSERT INTO User (id, username, email, password, role) VALUES ()'
addUser_Permission = 'INSERT INTO Role_Permission(id,Login,addArtist,addAlbum,addTrack,inactivateSong,modifiySong,deleteSong,modifiyAlbum,deleteAlbum,modifyArtist,deleteArtist) VALUES ()'
getUser_mostAlbums = 'SELECT User.Username,count(User.username) FROM addedAlbum INNER JOIN Users ON User.userid=addedAlbum.userid group by User.username order by count(User.username) DESC LIMIT 10'
getUser = 'SELECT id FROM User WHERE username LIKE (parameter) AND id<>1'
addUser_album = 'INSERT INTO Album (AlbumId, Title, ArtistId) VALUES ()'
addUser_artist = 'INSERT INTO addedArtist (UserId,ArtistId,InDate) VALUES ()'
addUser_track = 'INSERT INTO addedTrack (UserId,TrackId,InDate) VALUES ()'
updateUser = 'UPDATE User SET username=parameter, email=parameter, password=parameter,role=parameter WHERE id=parameter'
#Las que dice no cantidad son todos los usuarios. Clase 3/23/2020

#Queries para artista
getArtists = 'SELECT * FROM Artist'
getArtist_permissionUpdate = 'SELECT * FROM artistPermission WHERE canUpdate = TRUE GROUP BY id'
getArtist_permissionDelete = 'SELECT * FROM artistPermission WHERE canDelete=True GROUP BY id'
getCommonArtists = 'SELECT art1.name, count(art1.name)  FROM Album a1 INNER JOIN Artist art1 ON a1.ArtistId = art1.ArtistId GROUP BY a1.name ORDER BY count(art1.name) desc LIMIT 10'
getMostColaborativeArtists = 'SELECT  '
getArtist = 'SELECT * FROM Artist WHERE Name LIKE parameter LIMIT 1'
addArtist = 'INSERT INTO Artist (ArtistId, Name) VALUES (parameter,parameter2)'


#Queries para musica
#Agregar cancion
"INSERT INTO track(trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,)", ("trackid", 'name', 'albumid', 'mediatypeid', 'genreid', 'composer', 'milliseconds', 'bytes', 'unitprice')
#Agregar album
"INSERT INTO album(albumid, title, artistid) VALUES (%s, %s, %s)", ('albumid', 'title', 'artistid')
#Agregar artista
"INSERT INTO artist(artistid, name) VALUES (%s, %s,)", ('artistid', 'name')

getTracks = ''
#Queries para album
getAlbums= ''
#Queries para genero
getGenres = ''
#Queries para mediatype
getMediaTypes =''


'''
RRR     EEEE    PPP      OOO    RRR     TTTTTTT     EEEE     SSS
R  R    E       P  P    O   O   R  R       T        E       S
RRR     EEEE    PPP     O   O   RRR        T        EEEE     SSS
R  R    E       P       O   O   R  R       T        E           S
R   R   EEEE    P        OOO    R   R      T        EEEE    SSSS
'''

#Reporte 1
#Artistas con mas albumes publicados
rep1 = "SELECT artist.name, COUNT(album.albumid) FROM artist INNER JOIN album ON artist.artistid = album.artistid GROUP BY artist.name ORDER BY COUNT(album.albumid) DESC LIMIT 5"

#Reporte 2
#Generos con mas canciones
rep2 = "SELECT genre.name AS Genero, COUNT (genre.name) FROM Track INNER JOIN Genre ON Track.genreid = Genre.genreid GROUP BY Genre.name ORDER BY COUNT(Genre.name) DESC LIMIT 5"

#Reporte 3
#Duracion de cada playlist
rep3 = "SELECT p.name AS Playlist, SUM(t.milliseconds) AS Duration FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY p.name"

#Reporte 4
#Canciones de mayor duracion con la informacion de sus artistas
rep4 = "SELECT t.name AS Cancion, t.milliseconds AS Duracion_en_milisegundos, a.artistid, a.name FROM track t INNER JOIN Artist a ON t.composer = a.name ORDER BY t.milliseconds DESC LIMIT 5"

#Reporte 5
#Artistas que han registrado mas canciones
rep5 = "SELECT a.name AS Artista, COUNT(t.trackid) AS Canciones FROM Artist a INNER JOIN Track t ON a.name = t.composer GROUP BY a.name ORDER BY COUNT(t.trackid) DESC LIMIT 5"

#Reporte 6
#Promedio de duracion de canciones por genero
rep6 = "SELECT g.name AS Genero, AVG(t.milliseconds) AS Promedio_duracion_en_milisegundos FROM Track t INNER JOIN Genre g ON t.genreid = g.genreid GROUP BY g.name ORDER BY AVG(t.milliseconds) DESC"

#Reporte 7
#Cantidad de artistas diferentes por playlist
rep7 = "SELECT d.name, COUNT(d.name) FROM (SELECT p.name AS Name, COUNT(t.albumid) AS Artists FROM PlaylistTrack pt INNER JOIN Playlist p ON pt.playlistid = p.playlistid INNER JOIN Track t ON pt.trackid = t.trackid GROUP BY (p.name, t.albumid)) d GROUP BY d.name"

#Reporte 8
#Artistas con mas diversidad de generos musicales

rep8 = "SELECT a.name, COUNT(a.name) FROM (SELECT Artist.artistid as artist,track.genreid as genre FROM ARTIST JOIN Album ON Album.ArtistId=Artist.ArtistId JOIN TRACK ON Track.AlbumId=Album.AlbumId GROUP BY(artist.artistID,track.genreid)) G JOIN Artist a ON G.artist=a.artistid JOIN Genre ON G.genre=Genre.genreid GROUP BY (a.name) ORDER BY COUNT(a.name) DESC LIMIT 5"

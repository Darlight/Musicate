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
getUsers = 'SELECT * FROM User INNER JOIN Role_Permission ON User.id = Rol_Permission.userid WHERE User.role <> 'admin'' 
getUsersPermission = 'SELECT * FROM Rol_Permission'
getUser_Username = 'SELECT * FROM User INNER JOIN UserPermissions ON User.id=UserPermissions.UserId WHERE Username=parameter AND password=parameter2 AND canLogin='TRUE''
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

getTracks = ''
#Queries para album
getAlbums= ''
#Queries para genero
getGenres = ''
#Queries para mediatype
getMediaTypes =''

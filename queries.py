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
getUser_Username = 'SELECT * FROM User INNER JOIN UserPermissions ON User.id=UserPermissions.UserId WHERE Username=$1 AND password=$2 AND canLogin='TRUE''
addUser = 'INSERT INTO User (id, username, email, password, role) VALUES ()'
addUser_Permission = 'INSERT INTO Role_Permission(id,Login,addArtist,addAlbum,addTrack,inactivateSong,modifiySong,deleteSong,modifiyAlbum,deleteAlbum,modifyArtist,deleteArtist) VALUES ()'
getUser_mostAlbums = 'SELECT User.Username,count(User.username) FROM addedAlbum INNER JOIN Users ON User.userid=addedAlbum.userid group by User.username order by count(User.username) DESC LIMIT 10'
getUser = 'SELECT id FROM User WHERE username LIKE $1 AND id<>1'

#Queries para artista
#Queries para musi
getArtists = ''
getTracks = ''
#Queries para album
getAlbums= ''
#Queries para genero
getGenres = ''
#Queries para mediatype
getMediaTypes =''

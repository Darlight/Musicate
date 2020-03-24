
#Se debe descargar la liberia pscycopg2  en cmd con pip
#Este python sera para conectarse postgresSQL con Python con log in y sign in

import psycopg2
try:
    db_connetion = psycopg2.connect(
      user = "postgres",
      password = "1234",
      host = "127.0.0.1",
      port = "5432",
      database = "BDProyecto")

    cursor = db_connection.cursor()

    #call stored procedure
    

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

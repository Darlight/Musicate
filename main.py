
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from functools import partial
from queries import *

Window.size = (1100, 700)

import psycopg2

#connect to de database
con = psycopg2.connect(
    host = "localhost",
    database = "Proyecto2",
    user = "postgres",
    password = "Diego199")

#create a cursor
cur = con.cursor()


class MainWindow(Screen):
    errM = ObjectProperty(None)

    def userVer(self):
        usern = self.ids.user_field.text
        passw = self.ids.pass_field.text

        if usern != '':
            cur.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s AND roleid = 3", (str(usern), str(passw)))
            opcion1 = cur.fetchall()
            s = str(opcion1)
            if s != '[(0,)]':

                self.errM.text = ''
                self.manager.transition.direction = "left"
                self.manager.current = 'home'
            else:
                self.errM.text = 'Invalid username or password'


class SecondWindow(Screen):
    errM = ObjectProperty(None)

    def userVer(self):
        usern = self.ids.user_field.text
        passw = self.ids.pass_field.text

        if usern != '':
            cur.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s AND roleid = 1",
                        (str(usern), str(passw)))
            opcion1 = cur.fetchall()
            s = str(opcion1)
            if s != '[(0,)]':

                self.errM.text = ''
                self.manager.current = 'homeA'
                self.manager.transition.direction = "left"
            else:
                self.errM.text = 'Invalid username or password'


class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    songe = ObjectProperty(None)
    name1 = ObjectProperty(None)
    resu = ObjectProperty(None)

    def search(self):
        cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name = %s", (str(self.songe.text),))
        opcion1 = cur.fetchall()
        self.songe.text = ""
        if len(opcion1) == 0:
            cur.execute("SELECT a.artistid, a.name FROM artist a WHERE a.name = %s", (str(self.songe.text),))
            opcion2 = cur.fetchall()
            if len(opcion2) == 0:
                self.resu.text = "No results found"
        else:
            s = str(opcion1)
            s = s.replace(',', ' by ')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace("'", '')
            self.resu.text = s



class FifthWindow(Screen):
    songDur = 0
    songCur = 0

    page = 1
    state = 0

    songPage = 0
    maxPage = 0
    playlistID = 1

    currtime = ObjectProperty(None)
    name1 = ObjectProperty(None)
    titl = ObjectProperty(None)
    pl1 = ObjectProperty(None)
    pl2 = ObjectProperty(None)
    pl3 = ObjectProperty(None)
    pl4 = ObjectProperty(None)
    pl5 = ObjectProperty(None)
    pl6 = ObjectProperty(None)
    pl7 = ObjectProperty(None)
    pl8 = ObjectProperty(None)
    pl9 = ObjectProperty(None)
    pl10 = ObjectProperty(None)

    cur.execute(
        "SELECT * FROM playlist")
    opcion1 = cur.fetchall()
    pls = []
    for r in opcion1:
        pls.append(r[1])

    ides = []
    for r in opcion1:
        pls.append(r[0])

    p1 = pls[0]
    p2 = pls[1]
    p3 = pls[2]
    p4 = pls[3]
    p5 = pls[4]
    p6 = pls[5]
    p7 = pls[6]
    p8 = pls[7]
    p9 = pls[8]
    p10 = pls[9]
    def firstPage(self):
        self.pl1.text = self.pls[0]
        self.pl2.text = self.pls[1]
        self.pl3.text = self.pls[2]
        self.pl4.text = self.pls[3]
        self.pl5.text = self.pls[4]
        self.pl6.text = self.pls[5]
        self.pl7.text = self.pls[6]
        self.pl8.text = self.pls[7]
        self.pl9.text = self.pls[8]
        self.pl10.text = self.pls[9]
        self.titl.text = "Playlists (Page 1)"

    def secondPage(self):
        self.pl1.text = self.pls[10]
        self.pl2.text = self.pls[11]
        self.pl3.text = self.pls[12]
        self.pl4.text = self.pls[13]
        self.pl5.text = self.pls[14]
        self.pl6.text = self.pls[15]
        self.pl7.text = self.pls[16]
        self.pl8.text = self.pls[17]
        self.pl9.text = ""
        self.pl10.text = ""
        self.titl.text = "Playlists (Page 2)"

    def changePage(self):
        if self.state == 0:
            self.changePl()
        else:
            self.changeSong()

    def changePl(self):
        if self.page == 1:
            self.secondPage()
            self.page = 2
        else:
            self.firstPage()
            self.page = 1

    sngs = []

    def selectedPl(self):

        self.sngs.clear()
        self.songPage = 1
        cur.execute(
            "SELECT track.name, track.composer FROM playlisttrack JOIN track on playlisttrack.trackid = track.trackid WHERE playlistid = " + str(
                self.playlistID))
        opcion2 = cur.fetchall()

        for r in opcion2:
            self.sngs.append(r[0])

        if len(self.sngs) > 0:
            self.maxPage = int(len(self.sngs) / 10)
            if self.maxPage == 0:
                self.maxPage = 1
            self.changeSong()



    def changeSong(self):
        if self.songPage >= self.maxPage:
            self.songPage = 1
        x = (self.songPage - 1) * 10
        self.pl1.text = self.sngs[x]
        self.pl2.text = self.sngs[x + 1]
        self.pl3.text = self.sngs[x + 2]
        self.pl4.text = self.sngs[x + 3]
        self.pl5.text = self.sngs[x + 4]
        self.pl6.text = self.sngs[x + 5]
        self.pl7.text = self.sngs[x + 6]
        self.pl8.text = self.sngs[x + 7]
        self.pl7.text = self.sngs[x + 8]
        self.pl8.text = self.sngs[x + 9]

        self.titl.text = "Songs (Page " + str(self.songPage) + " of " + str(self.maxPage) + ")"
        self.songPage += 1

    def selected(self, indexe):

        self.playlistID = indexe
        if self.state == 0:
            self.state = 1
            self.selectedPl()
        else:
            self.playbtn()

    def playtime(self, interval):
        if self.songCur != self.songDur:
            self.songCur = self.songCur + 1
            self.currtime.value = self.songCur / self.songDur

        else:
            self.songCur = 0
            self.currtime.value = 0

    def playbtn(self):
        self.songCur = 0
        cur.execute(
            "SELECT milliseconds FROM track WHERE name = 'Revelations' LIMIT 1")
        opcion3 = cur.fetchall()
        s = str(opcion3[0])
        s = s.replace(',', '')
        s = s.replace('(', '')
        s = s.replace(')', '')
        self.songDur = (float(s)) / 1000
        Clock.schedule_interval(self.playtime, 1)

    def back(self):
        self.state = 0
        self.firstPage()


class SixthWindow(Screen):

    currtime = ObjectProperty(None)
    name1 = ObjectProperty(None)
    titl = ObjectProperty(None)
    pl1 = ObjectProperty(None)
    pl2 = ObjectProperty(None)
    pl3 = ObjectProperty(None)
    pl4 = ObjectProperty(None)
    pl5 = ObjectProperty(None)
    pl6 = ObjectProperty(None)
    pl7 = ObjectProperty(None)
    pl8 = ObjectProperty(None)
    pl9 = ObjectProperty(None)
    pl10 = ObjectProperty(None)

    cur.execute(rep1)
    opcion1 = cur.fetchall()
    report1 = []
    for r in opcion1:
        report1.append(f"{r[0]} with {r[1]} ")

    r = str(report1)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p1 = r

    cur.execute(rep2)
    opcion2 = cur.fetchall()
    report2 = []
    for r in opcion2:
        report2.append(f"{r[0]} with {r[1]} ")

    r = str(report2)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p2 = r

    cur.execute(rep3)
    opcion3 = cur.fetchall()
    report3 = []
    for r in opcion3:
        report3.append(f"{r[0]} with {r[1]} ms")

    r = str(report3)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p3 = r

    cur.execute(rep4)
    opcion4 = cur.fetchall()
    report4 = []
    for r in opcion4:
        report4.append(f"{r[0]} with {r[1]} ms")

    r = str(report4)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p4 = r

    cur.execute(rep5)
    opcion5 = cur.fetchall()
    report5 = []
    for r in opcion5:
        report5.append(f"{r[0]} with {r[1]} ")

    r = str(report5)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p5 = r

    cur.execute(rep6)
    opcion6 = cur.fetchall()
    report6 = []
    for r in opcion6:
        report6.append(f"{r[0]} with {r[1]} ms")

    r = str(report6)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p6 = r

    cur.execute(rep7)
    opcion7 = cur.fetchall()
    report7 = []
    for r in opcion7:
        report7.append(f"{r[0]} with {r[1]} ")

    r = str(report7)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p7 = r

    cur.execute(rep8)
    opcion8 = cur.fetchall()
    report8 = []
    for r in opcion8:
        report8.append(f"{r[0]} with {r[1]} ")

    r = str(report8)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p8 = r

    cur.execute(rep1)
    opcion1 = cur.fetchall()
    report1 = []
    for r in opcion1:
        report1.append(f"{r[0]} with {r[1]} ")




class EigthWindow(Screen):
    pass

class NinthWindow(Screen):
    pass

class TenthWindow(Screen):
    currtime = ObjectProperty(None)
    name1 = ObjectProperty(None)
    titl = ObjectProperty(None)
    pl1 = ObjectProperty(None)
    pl2 = ObjectProperty(None)
    pl3 = ObjectProperty(None)
    pl4 = ObjectProperty(None)
    pl5 = ObjectProperty(None)
    pl6 = ObjectProperty(None)
    pl7 = ObjectProperty(None)
    pl8 = ObjectProperty(None)
    pl9 = ObjectProperty(None)
    pl10 = ObjectProperty(None)

    cur.execute(rep1)
    opcion1 = cur.fetchall()
    report1 = []
    for r in opcion1:
        report1.append(f"{r[0]} with {r[1]} ")

    r = str(report1)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p1 = r

    cur.execute(rep2)
    opcion2 = cur.fetchall()
    report2 = []
    for r in opcion2:
        report2.append(f"{r[0]} with {r[1]} ")

    r = str(report2)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p2 = r

    cur.execute(rep3)
    opcion3 = cur.fetchall()
    report3 = []
    for r in opcion3:
        report3.append(f"{r[0]} with {r[1]} ms")

    r = str(report3)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p3 = r

    cur.execute(rep4)
    opcion4 = cur.fetchall()
    report4 = []
    for r in opcion4:
        report4.append(f"{r[0]} with {r[1]} ms")

    r = str(report4)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p4 = r

    cur.execute(rep5)
    opcion5 = cur.fetchall()
    report5 = []
    for r in opcion5:
        report5.append(f"{r[0]} with {r[1]} ")

    r = str(report5)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p5 = r

    cur.execute(rep6)
    opcion6 = cur.fetchall()
    report6 = []
    for r in opcion6:
        report6.append(f"{r[0]} with {r[1]} ms")

    r = str(report6)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p6 = r

    cur.execute(rep7)
    opcion7 = cur.fetchall()
    report7 = []
    for r in opcion7:
        report7.append(f"{r[0]} with {r[1]} ")

    r = str(report7)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p7 = r

    cur.execute(rep8)
    opcion8 = cur.fetchall()
    report8 = []
    for r in opcion8:
        report8.append(f"{r[0]} with {r[1]} ")

    r = str(report8)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace("'", "")
    r = r.replace(",", '\n')
    p8 = r

    cur.execute(rep1)
    opcion1 = cur.fetchall()
    report1 = []
    for r in opcion1:
        report1.append(f"{r[0]} with {r[1]} ")


class EleventhWindow(Screen):
    def addSong(self):
        artist = self.ids.artisti.text
        album = self.ids.albumi.text
        song = self.ids.songi.text
        duration = self.ids.duration.text
        size = self.ids.sizei.text
        genre = self.ids.genre.text
        media = self.ids.media.text
        price = self.ids.price.text

        cur.execute("SELECT MAX(trackid) FROM track ")
        opcion1 = cur.fetchall()
        trackid = 0
        for r in opcion1:
            trackid = r[0] + 1

        cur.execute("SELECT album.albumid FROM album WHERE album.title = %s ", (album,))
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0]

        cur.execute("SELECT mediatype.mediatypeid FROM mediatype WHERE mediatype.name = %s ", (media,))
        opcion1 = cur.fetchall()
        mediatypeid = 0
        for r in opcion1:
            mediatypeid = r[0]

        cur.execute("SELECT genre.genreid FROM genre WHERE genre.name = %s ", (genre,))
        opcion1 = cur.fetchall()
        genreid = 0
        for r in opcion1:
            genreid = r[0]

        if song != '':
            cur.execute(
                "INSERT INTO track(trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (trackid, song, albumid, mediatypeid, genreid, artist, duration, size, price))
            con.commit()



class TwelveWindow(Screen):
    def addArt(self):
        name = self.ids.fname.text

        cur.execute("SELECT MAX(artistid) FROM artist ")
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0] + 1


        if name != '':
            cur.execute("INSERT INTO artist(artistid, name) VALUES (%s, %s)", (artistid, name))
            con.commit()


class ThirteenWindow(Screen):
    def addAlbum(self):
        artist = self.ids.artisti.text
        album = self.ids.albumi.text

        cur.execute("SELECT MAX(albumid) FROM album ")
        opcion1 = cur.fetchall()
        albumid = 0
        for r in opcion1:
            albumid = r[0] + 1

        cur.execute("SELECT artist.artistid FROM artist WHERE artist.name = %s ", (artist,))
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0]

        if album != '':
            cur.execute("INSERT INTO album(albumid, title, artistid) VALUES (%s, %s, %s)", (albumid, album, artistid))
            con.commit()



class FourteenWindow(Screen):
    def elimi(self, indexe):
        songi = self.ids.songI.text
        arti = self.ids.artistI.text
        albumi = self.ids.albumI.text

        if indexe == 1:
            cur.execute("DELETE FROM track WHERE track.name=%s", (songi,))
            con.commit()
            print("Se ha eliminado la cancion de la base de datos")

        elif indexe == 2:
            cur.execute("DELETE FROM album WHERE title=%s", (albumi, ))
            con.commit()
            print("Se ha eliminado la album de la base de datos")

        elif indexe == 3:
            cur.execute("DELETE FROM artist WHERE name=%s", (arti, ))
            con.commit()
            print("Se ha eliminado la artista de la base de datos")


class FifteenWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()



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
import datetime

Window.size = (1100, 700)

import psycopg2
import csv

#connect to de database
con = psycopg2.connect(
    host = "localhost",
    database = "Musicate",
    user = "postgres",
    password = "Diego199")

#create a cursor
cur = con.cursor()

#MongoDB
import pymongo
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://JDiegoSolorzano:Diego199@cluster0-5fvcd.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["proyectiFinal"]
collection = db["compras"]


class MainWindow(Screen):
    errM = ObjectProperty(None)


    def userVer(self):
        usern = self.ids.user_field.text
        passw = self.ids.pass_field.text
        EleventhWindow.userActual = usern
        TwelveWindow.userActual = usern
        ThirteenWindow.userActual = usern
        FifteenWindow.userActual = usern

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
        EleventhWindow.userActual = usern
        TwelveWindow.userActual = usern
        ThirteenWindow.userActual = usern
        FifteenWindow.userActual = usern

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
    sinp = ObjectProperty(None)

    songsel = ""
    def search(self):
        self.songsel = self.songe.text
        print(str(self.songe.text) + "pol")
        print(self.songsel)
        cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name = %s LIMIT 1", (str(self.songe.text),))
        opcion1 = cur.fetchall()
        self.songe.text = ""
        if len(opcion1) == 0:
            cur.execute("SELECT t.name, t.composer FROM track t WHERE t.name LIKE '%" + self.songsel + "%' LIMIT 1")
            opcion1 = cur.fetchall()
            if len(opcion1) == 0:
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
        else:
            s = str(opcion1)
            s = s.replace(',', ' by ')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace("'", '')
            self.resu.text = s

    def addPla(self):
        print(self.songsel)
        if self.sinp.text != "":
            cur.execute("SELECT playlistid FROM playlist WHERE name LIKE '%" + self.sinp.text + "%' LIMIT 1")
            opcion1 = cur.fetchall()
            s = str(opcion1)
            s = s.replace(',', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace("'", '')
            playid = int(s)
            print(s)
            print(self.songsel)
            cur.execute("SELECT t.trackid FROM track t WHERE t.name LIKE '%" + self.songsel + "%' LIMIT 1")
            opcion1 = cur.fetchall()
            s = str(opcion1)
            s = s.replace(',', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace("'", '')

            print(s)
            trackid = int(s)

            cur.execute("INSERT INTO playlisttrack VALUES(%s, %s)", (playid, trackid))
            con.commit()


class FifthWindow(Screen):
    songDur = 0
    songCur = 0

    state = 0
    plPage = 1
    maxPagep = 0

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
    print(len(pls))

    maxPagep = int(len(pls) / 10)
    print(maxPagep)
    remap = len(pls) % 10
    print(remap)
    if remap > 0:
        maxPagep += 1
    if maxPagep == 0:
        maxPagep = 1


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

    def changePage(self):
        print(self.plPage)
        if self.state == 0:
            self.plPage += 1
            print(self.plPage)
            self.changePl()
        else:
            self.changeSong()

    def back(self):
        self.plPage = 1
        self.state = 0
        cur.execute(
            "SELECT * FROM playlist")
        self.opcion1 = cur.fetchall()
        self.pls = []
        for r in self.opcion1:
            self.pls.append(r[1])


        self.maxPagep = int(len(self.pls) / 10)
        self.remap = len(self.pls) % 10
        if self.remap > 0:
            self.maxPagep += 1
        if self.maxPagep == 0:
            self.maxPagep = 1
        self.changePl()


    def changePl(self):

        if self.plPage > self.maxPagep:
            self.plPage = 1
        x = (self.plPage - 1) * 10
        if self.plPage == self.maxPagep and self.remap > 0:
            self.pl1.text = self.pls[x]
            if self.remap >= 2:
                self.pl2.text = self.pls[x + 1]
            else:
                self.pl2.text = ""
            if self.remap >= 3:
                self.pl3.text = self.pls[x + 2]
            else:
                self.pl3.text = ""
            if self.remap >= 4:
                self.pl4.text = self.pls[x + 3]
            else:
                self.pl4.text = ""
            if self.remap >= 5:
                self.pl5.text = self.pls[x + 4]
            else:
                self.pl5.text = ""
            if self.remap >= 6:
                self.pl6.text = self.pls[x + 5]
            else:
                self.pl6.text = ""
            if self.remap >= 7:
                self.pl7.text = self.pls[x + 6]
            else:
                self.pl7.text = ""
            if self.remap >= 8:
                self.pl8.text = self.pls[x + 7]
            else:
                self.pl8.text = ""
            if self.remap >= 9:
                self.pl9.text = self.pls[x + 8]
            else:
                self.pl9.text = ""
            self.pl10.text = ""
        else:

            self.pl1.text = self.pls[x]
            self.pl2.text = self.pls[x + 1]
            self.pl3.text = self.pls[x + 2]
            self.pl4.text = self.pls[x + 3]
            self.pl5.text = self.pls[x + 4]
            self.pl6.text = self.pls[x + 5]
            self.pl7.text = self.pls[x + 6]
            self.pl8.text = self.pls[x + 7]
            self.pl9.text = self.pls[x + 8]
            self.pl10.text = self.pls[x + 9]

        self.titl.text = "Playlists (Page " + str(self.plPage) + " of " + str(self.maxPagep) + ")"



    sngs = []
    rema = 0

    def selectedPl(self):

        self.sngs.clear()
        self.songPage = 1
        cur.execute(
            "SELECT track.name FROM playlisttrack JOIN track on playlisttrack.trackid = track.trackid WHERE playlistid = " + str(
                self.playlistID))
        opcion2 = cur.fetchall()
        print(self.playlistID)
        print (opcion2)

        for r in opcion2:
            self.sngs.append(r[0])

        if len(self.sngs) > 0:
            self.maxPage = int(len(self.sngs) / 10)
            self.rema = len(self.sngs) % 10
            if self.rema > 0:
                self.maxPage += 1
            if self.maxPage == 0:
                self.maxPage = 1
            self.changeSong()



    def changeSong(self):
        if self.songPage > self.maxPage:
            self.songPage = 1
        x = (self.songPage - 1) * 10
        print(self.rema)
        if self.songPage == self.maxPage and self.rema > 0:
            self.pl1.text = self.sngs[x]
            if self.rema >= 2:
                self.pl2.text = self.sngs[x + 1]
            else:
                self.pl2.text = ""
            if self.rema >= 3:
                self.pl3.text = self.sngs[x + 2]
            else:
                self.pl3.text = ""
            if self.rema >= 4:
                self.pl4.text = self.sngs[x + 3]
            else:
                self.pl4.text = ""
            if self.rema >= 5:
                self.pl5.text = self.sngs[x + 4]
            else:
                self.pl5.text = ""
            if self.rema >= 6:
                self.pl6.text = self.sngs[x + 5]
            else:
                self.pl6.text = ""
            if self.rema >= 7:
                self.pl7.text = self.sngs[x + 6]
            else:
                self.pl7.text = ""
            if self.rema >= 8:
                self.pl8.text = self.sngs[x + 7]
            else:
                self.pl8.text = ""
            if self.rema >= 9:
                self.pl9.text = self.sngs[x + 8]
            else:
                self.pl9.text = ""
            self.pl10.text = ""
        else:

            self.pl1.text = self.sngs[x]
            self.pl2.text = self.sngs[x + 1]
            self.pl3.text = self.sngs[x + 2]
            self.pl4.text = self.sngs[x + 3]
            self.pl5.text = self.sngs[x + 4]
            self.pl6.text = self.sngs[x + 5]
            self.pl7.text = self.sngs[x + 6]
            self.pl8.text = self.sngs[x + 7]
            self.pl9.text = self.sngs[x + 8]
            self.pl10.text = self.sngs[x + 9]

        self.titl.text = "Songs (Page " + str(self.songPage) + " of " + str(self.maxPage) + ")"
        self.songPage += 1

    def selected(self, indexe):

        self.playlistID = indexe + (10 * (self.plPage - 1))
        if self.state == 0:
            self.state = 1
            self.selectedPl()
        else:
            self.playbtn(indexe)

    def playtime(self, interval):
        if self.songCur != self.songDur:
            self.songCur = self.songCur + 1
            self.currtime.value = self.songCur / self.songDur

        else:
            self.songCur = 0
            self.currtime.value = 0

    def playbtn(self, indexe):
        if indexe == 1:
            names = self.pl1.text
        elif indexe == 2:
            names = self.pl2.text
        elif indexe == 3:
            names = self.pl3.text
        elif indexe == 4:
            names = self.pl4.text
        elif indexe == 5:
            names = self.pl5.text
        elif indexe == 6:
            names = self.pl6.text
        elif indexe == 7:
            names = self.pl7.text
        elif indexe == 8:
            names = self.pl8.text
        elif indexe == 9:
            names = self.pl9.text
        elif indexe == 10:
            names = self.pl10.text
        if str(names) != "":
            self.songCur = 0
            cur.execute(
                "SELECT milliseconds FROM track WHERE name = %s LIMIT 1", (str(names),))
            opcion3 = cur.fetchall()
            s = str(opcion3[0])
            s = s.replace(',', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            self.songDur = (float(s)) / 1000
            cur.execute(
                "SELECT composer FROM track WHERE name = %s LIMIT 1", (str(names),))
            opcion3 = cur.fetchall()
            s = str(opcion3[0])
            s = s.replace(',', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            if s == "None":
                s = "Anonymous"
            self.name1.text = "Now Playing: " + str(names) +" by " + s
            Clock.schedule_interval(self.playtime, 1)




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
    estado = False

    def exportRep(self, indexe):
        if self.estado == True:
            mode = 'a'
        else:
            mode = 'w'
            self.estado = True
        with open('reporteTest.csv', mode, newline='') as file:
            writer = csv.writer(file)

            if indexe == 1:
                headin = str(self.ids.repo1.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion1:
                    writer.writerow(line)

            elif indexe == 2:
                headin = str(self.ids.repo2.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion2:
                    writer.writerow(line)
            elif indexe == 3:
                headin = str(self.ids.repo3.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion3:
                    writer.writerow(line)
            elif indexe == 4:
                headin = str(self.ids.repo4.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion4:
                    writer.writerow(line)
            elif indexe == 5:
                headin = str(self.ids.repo5.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion5:
                    writer.writerow(line)
            elif indexe == 6:
                headin = str(self.ids.repo6.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion6:
                    writer.writerow(line)
            elif indexe == 7:
                headin = str(self.ids.repo7.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion7:
                    writer.writerow(line)
            elif indexe == 8:
                headin = str(self.ids.repo8.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion8:
                    writer.writerow(line)
    cur.execute(rep1)
    opcion1 = cur.fetchall()
    print(opcion1)

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




class EigthWindow(Screen):
    pass

class NinthWindow(Screen):
    pass

class TenthWindow(Screen):
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
    estado = False

    def exportRep(self, indexe):
        if self.estado == True:
            mode = 'a'
        else:
            mode = 'w'
            self.estado = True
        with open('reporteTest.csv', mode, newline='') as file:
            writer = csv.writer(file)

            if indexe == 1:
                headin = str(self.ids.repo1.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion1:
                    writer.writerow(line)

            elif indexe == 2:
                headin = str(self.ids.repo2.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion2:
                    writer.writerow(line)
            elif indexe == 3:
                headin = str(self.ids.repo3.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion3:
                    writer.writerow(line)
            elif indexe == 4:
                headin = str(self.ids.repo4.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion4:
                    writer.writerow(line)
            elif indexe == 5:
                headin = str(self.ids.repo5.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion5:
                    writer.writerow(line)
            elif indexe == 6:
                headin = str(self.ids.repo6.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion6:
                    writer.writerow(line)
            elif indexe == 7:
                headin = str(self.ids.repo7.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion7:
                    writer.writerow(line)
            elif indexe == 8:
                headin = str(self.ids.repo8.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Albums"])
                for line in self.opcion8:
                    writer.writerow(line)

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
    userActual = ""

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
                "INSERT INTO track(trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice, modify) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",
                (trackid, song, albumid, mediatypeid, genreid, artist, duration, size, price, self.userActual))
            con.commit()



class TwelveWindow(Screen):
    userActual = ""
    def addArt(self):
        name = self.ids.fname.text
        print(self.userActual)

        cur.execute("SELECT MAX(artistid) FROM artist ")
        opcion1 = cur.fetchall()
        artistid = 0
        for r in opcion1:
            artistid = r[0] + 1


        if name != '':
            cur.execute("INSERT INTO artist(artistid, name, modify) VALUES (%s, %s, %s)", (artistid, name, self.userActual))
            con.commit()


class ThirteenWindow(Screen):
    userActual = ""

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
            cur.execute("INSERT INTO album(albumid, title, artistid, modify) VALUES (%s, %s, %s, %s)", (albumid, album, artistid, self.userActual))
            con.commit()



class FourteenWindow(Screen):

    def elimi(self, indexe):
        songi = self.ids.songI.text
        arti = self.ids.artistI.text
        albumi = self.ids.albumI.text

        if indexe == 1:
            self.elimTrack(songi)

        elif indexe == 2:
            self.elimAlbum(albumi)

        elif indexe == 3:
            self.elimArt(arti)

    def elimTrack(self, name):
        cur.execute("SELECT trackid FROM track WHERE name = %s", (name,))
        opcion1 = cur.fetchall()

        sonNames = []
        for r in opcion1:
            t = str(r[0])

            sonNames.append(t)

        for r in sonNames:
            trackid = int(r)
            cur.execute("DELETE FROM invoiceline WHERE trackid= %s", (trackid,))
            con.commit()
            cur.execute("DELETE FROM playlisttrack WHERE trackid = %s", (trackid,))
            con.commit()
            cur.execute("DELETE FROM track WHERE trackid = %s", (trackid,))
            con.commit()
            print("Se ha eliminado la cancion de la base de datos")

    def elimAlbum(self, name):


        cur.execute("SELECT albumid FROM album WHERE title = %s", (name,))
        opcion1 = cur.fetchall()
        s = str(opcion1)
        s = s.replace(',', '')
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace('[', '')
        s = s.replace(']', '')
        s = s.replace("'", '')
        albumid = int(s)

        cur.execute("SELECT name FROM track WHERE albumid = %s", (albumid,))
        opcion1 = cur.fetchall()

        sonNames = []
        for r in opcion1:
            t = str(r[0])

            sonNames.append(t)
        for r in sonNames:
            songName = str(r)
            print(songName)
            self.elimTrack(songName)
        cur.execute("DELETE FROM album WHERE title= %s", (name, ))
        con.commit()
        print("Se ha eliminado la album de la base de datos")

    def elimArt(self, name):
        cur.execute("SELECT artistid FROM artist WHERE name = %s", (name,))
        opcion1 = cur.fetchall()
        s = str(opcion1)
        s = s.replace(',', '')
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace('[', '')
        s = s.replace(']', '')
        s = s.replace("'", '')
        artistid = int(s)

        cur.execute("SELECT title FROM album WHERE artistid = %s", (artistid,))
        opcion1 = cur.fetchall()

        sonNames = []
        for r in opcion1:
            t = str(r[0])

            sonNames.append(t)
        print(sonNames[0])
        for r in sonNames:
            albumName = str(r)
            self.elimAlbum(albumName)

        cur.execute("DELETE FROM artist WHERE name= %s", (name,))
        con.commit()
        print("Se ha eliminado la artista de la base de datos")

class FifteenWindow(Screen):
    userActual = ""
    def addPl(self):
        name = self.ids.pname.text

        cur.execute("SELECT MAX(playlistid) FROM playlist ")
        opcion1 = cur.fetchall()
        plid = 0
        for r in opcion1:
            plid = r[0] + 1

        if name != '':
            cur.execute("INSERT INTO playlist(playlistid, name, modify) VALUES (%s, %s, %s)", (plid, name, self.userActual))
            con.commit()

class SixteenWindow(Screen):

    cur.execute("SELECT fechita FROM bitacora")
    opcion5 = cur.fetchall()
    print(opcion5[0])
    report1 = []
    for r in opcion5:
        report1.append(r)

    r = str(report1)
    print(report1)
    r = r.replace('datetime.date', "")
    r = r.replace(",), ", '\n')
    r = r.replace(",)", '')
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace('(', "")
    r = r.replace(')', "")
    r = r.replace("'", "")
    r = r.replace(", ", '/')
    p1 = r

    cur.execute("SELECT horita FROM bitacora")
    opcion5 = cur.fetchall()
    print(opcion5)
    report2 = []
    for r in opcion5:
        report2.append(r)

    r = str(report2)
    print(report2)
    r = r.replace('datetime.time', "")
    r = r.replace('tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-360, name=None', "")
    r = r.replace(",), ", '\n')
    r = r.replace(",)", '')
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace('(', "")
    r = r.replace(')', "")
    r = r.replace("'", "")
    r = r.replace(", ", ':')
    p2 = r

    cur.execute("SELECT usuario FROM bitacora")
    opcion5 = cur.fetchall()
    print(opcion5)
    report3 = []
    for r in opcion5:
        report3.append(r)

    r = str(report3)
    print(report3)
    r = r.replace('[', "")
    r = r.replace(']', "")
    r = r.replace('(', "")
    r = r.replace(')', "")
    r = r.replace("'", "")
    r = r.replace(", ", '\n')
    r = r.replace(',', "")
    p3 = r

class SeventeenWindow(Screen):
    def insertMongo(self):
        year = self.ids.year.text
        month = self.ids.month.text
        day = self.ids.day.text
        year2 = self.ids.year2.text
        month2 = self.ids.month2.text
        day2 = self.ids.day2.text

        indate1 = year + "-" + month + "-" + day + " 00:00:00"
        indate2 = year2 + "-" + month2 + "-" + day2 + " 00:00:00"

        cur.execute("SELECT invoiceid, customerid, total FROM invoice WHERE invoicedate BETWEEN %s AND %s", (indate1, indate2 ))
        opcion1 = cur.fetchall()
        print(opcion1)
        datei = "from" + indate1 + " to " + indate2
        mylist = []
        for r in opcion1:
            inid = int(r[0])
            cusid = int(r[1])
            total = float(r[2])
            res = {"invoiceid": inid, "customerid": cusid, "date": datei, "total": total}
            mylist.append(res)
        print(mylist)
        if len(mylist) == 1:
            collection.insert_one(mylist)
        elif len(mylist) > 1:
            collection.insert_many(mylist)

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()


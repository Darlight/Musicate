
import kivy
from kivy.app import App

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from queries import *
import datetime
from reportlab.pdfgen import canvas
from youtube_search import YoutubeSearch
import ast
import youtube_dl
import os
import random
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

cluster = MongoClient("mongodb+srv://JDiegoSolorzano:Diego199@cluster0-5fvcd.mongodb.net/proyectiFinal?retryWrites=true&w=majority")
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
        FourthWindow.userActual = usern
        FifteenWindow.userActual = usern
        FourteenWindow.userActual = usern
        NineteenWindow.userActual = usern

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
        FourthWindow.userActual = usern
        FifteenWindow.userActual = usern
        FourteenWindow.userActual = usern
        NineteenWindow.userActual = usern
        TwentyWindow.userActual = usern

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

class AddPlWindow(Screen):
    sinp = ObjectProperty(None)
    songsele = ""
    seco = ""
    def addPla(self):
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
            cur.execute("SELECT t.trackid FROM track t WHERE t.name = '" + self.songsele + "' LIMIT 1")
            opcion1 = cur.fetchall()
            if len(opcion1) == 0:
                cur.execute("SELECT t.trackid FROM track t WHERE t.name = '" + self.seco + "' LIMIT 1")
                opcion1 = cur.fetchall()
            print(opcion1)
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

class FourthWindow(Screen):
    songe = ObjectProperty(None)
    name1 = ObjectProperty(None)
    resu = ObjectProperty(None)
    userActual = ""

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
    songDur = 0
    songCur = 0
    currtime = ObjectProperty(None)
    name1 = ObjectProperty(None)
    opcion1 = []

    songsel = ""
    segund = []
    def search(self):
        canciones = []
        self.songsel = self.songe.text
        arti = ""
        self.songe.text = ""
        cur.execute(
            "SELECT track.name, artist.name FROM track INNER JOIN album on album.albumid = track.albumid INNER JOIN artist on artist.artistid = album.artistid WHERE track.name LIKE '%" + self.songsel + "%' LIMIT 10")
        self.opcion1 = cur.fetchall()
        print(self.opcion1)
        if len(self.opcion1) == 0:
            cur.execute("SELECT track.name, artist.name FROM track INNER JOIN album on album.albumid = track.albumid INNER JOIN artist on artist.artistid = album.artistid WHERE artist.name LIKE '%" + self.songsel + "%' LIMIT 10")
            self.opcion1 = cur.fetchall()
            if len(self.opcion1) == 0:
                cur.execute(
                    "SELECT track.name, artist.name FROM track INNER JOIN album on album.albumid = track.albumid INNER JOIN artist on artist.artistid = album.artistid WHERE album.title LIKE '%" + self.songsel + "%' LIMIT 10")
                self.opcion1 = cur.fetchall()
                if len(self.opcion1) == 0:

                    self.pl1.text = "No results found"
                    self.pl2.text = ""
                    self.pl3.text = ""
                    self.pl4.text = ""
                    self.pl5.text = ""
                    self.pl6.text = ""
                    self.pl7.text = ""
                    self.pl8.text = ""
                    self.pl9.text = ""
                    self.pl10.text = ""
                else:

                    for s in self.opcion1:
                        s = str(s)
                        s = s.replace("', ", ' by ')
                        s = s.replace('", ', ' by ')
                        s = s.replace(',', '')
                        s = s.replace('(', '')
                        s = s.replace(')', '')
                        s = s.replace('[', '')
                        s = s.replace(']', '')
                        s = s.replace("'", '')
                        s = s.replace('"', '')
                        canciones.append(s)
            else:

                for s in self.opcion1:
                    s = str(s)
                    s = s.replace("', ", ' by ')
                    s = s.replace('", ', ' by ')
                    s = s.replace(',', '')
                    s = s.replace('(', '')
                    s = s.replace(')', '')
                    s = s.replace('[', '')
                    s = s.replace(']', '')
                    s = s.replace("'", '')
                    s = s.replace('"', '')
                    canciones.append(s)

        else:
            for s in self.opcion1:
                s = str(s)
                s = s.replace("', ", ' by ')
                s = s.replace('", ', ' by ')
                s = s.replace(',', '')
                s = s.replace('(', '')
                s = s.replace(')', '')
                s = s.replace('[', '')
                s = s.replace(']', '')
                s = s.replace("'", '')
                s = s.replace('"', '')
                canciones.append(s)

        if len(canciones) > 0:
            self.pl1.text = canciones[0]
            self.pl2.text = ""
            self.pl3.text = ""
            self.pl4.text = ""
            self.pl5.text = ""
            self.pl6.text = ""
            self.pl7.text = ""
            self.pl8.text = ""
            self.pl9.text = ""
            self.pl10.text = ""
            if len(canciones) > 1:
                self.pl2.text = canciones[1]
                if len(canciones) > 2:
                    self.pl3.text = canciones[2]
                    if len(canciones) > 3:
                        self.pl4.text = canciones[3]
                        if len(canciones) > 4:
                            self.pl5.text = canciones[4]
                            if len(canciones) > 5:
                                self.pl6.text = canciones[5]
                                if len(canciones) > 6:
                                    self.pl7.text = canciones[6]
                                    if len(canciones) > 7:
                                        self.pl8.text = canciones[7]
                                        if len(canciones) > 8:
                                            self.pl9.text = canciones[8]
                                            if len(canciones) > 8:
                                                self.pl10.text = canciones[9]
        print(canciones)


        print(self.opcion1)
        for s in self.opcion1:
            s = str(s)
            s = s.replace('", ', ' by ')
            s = s.replace("', ", ' by ')
            s = s.replace(',', '')
            s = s.replace("'", "''")
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace('"', '')
            self.segund.append(s)
    def addPla(self, indexe):
        if indexe == 1:
            names = self.pl1.text
            seco = self.segund[0]
        elif indexe == 2:
            names = self.pl2.text
            seco = self.segund[1]
        elif indexe == 3:
            names = self.pl3.text
            seco = self.segund[2]
        elif indexe == 4:
            names = self.pl4.text
            seco = self.segund[3]
        elif indexe == 5:
            names = self.pl5.text
            seco = self.segund[4]
        elif indexe == 6:
            names = self.pl6.text
            seco = self.segund[5]
        elif indexe == 7:
            names = self.pl7.text
            seco = self.segund[6]
        elif indexe == 8:
            names = self.pl8.text
            seco = self.segund[7]
        elif indexe == 9:
            names = self.pl9.text
            seco = self.segund[8]
        elif indexe == 10:
            names = self.pl10.text
            seco = self.segund[9]
        if str(names) != "":
            titl = names.split(" by", 1)
            print(titl)
            second = seco.split(" by", 1)
            print(seco)
            AddPlWindow.songsele = titl[0]
            AddPlWindow.seco = second[0]
            self.manager.current = 'addPlaylist'
    def selected(self, indexe):
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
            seco = self.segund[0]
        elif indexe == 2:
            names = self.pl2.text
            seco = self.segund[1]
        elif indexe == 3:
            names = self.pl3.text
            seco = self.segund[2]
        elif indexe == 4:
            names = self.pl4.text
            seco = self.segund[3]
        elif indexe == 5:
            names = self.pl5.text
            seco = self.segund[4]
        elif indexe == 6:
            names = self.pl6.text
            seco = self.segund[5]
        elif indexe == 7:
            names = self.pl7.text
            seco = self.segund[6]
        elif indexe == 8:
            names = self.pl8.text
            seco = self.segund[7]
        elif indexe == 9:
            names = self.pl9.text
            seco = self.segund[8]
        elif indexe == 10:
            names = self.pl10.text
            seco = self.segund[9]
        if str(names) != "":
            conserv = names
            titl = names.split(" by", 1)
            print(titl)
            second = seco.split(" by", 1)
            print(seco)
            names = titl[0]
            Clock.unschedule(self.playtime)

            print(conserv)
            result = YoutubeSearch(conserv, max_results=1).to_json()
            resultado = ast.literal_eval(result)
            valor = list(resultado.values())
            try:
                values = list(valor[0][0].values())
                url = 'https://www.youtube.com' + str(values[1])
                file1 = values[1].split('=')
                file_name = file1[1]

                def my_hook(d):
                    if d['status'] == 'finished':
                        print('Done downloading, now converting ...')

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(id)s',
                    'noplaylist': True,
                    'progress_hooks': [my_hook],
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                try:
                    os.rename(file_name, file_name + '.mp3')
                except:
                    print("")
                os.system("start " + file_name + '.mp3')
            except:
                print("Esta cancion no se encuentra disponible en este momento")
                print("Intente de nuevo en un momento")


            print(names[0])
            cur.execute(
                "SELECT trackid FROM track WHERE name = '" + str(names) + "' LIMIT 1")
            opcion6 = cur.fetchall()
            if len(opcion6) != 0:

                s = str(opcion6[0])
                s = s.replace(',', '')
                s = s.replace('(', '')
                s = s.replace(')', '')
                tid = s
                print("aho")
                print(tid)
                print(self.userActual)
                cur.execute(
                    "update track set views = views + 1 , modify = '" + str(self.userActual) + "' where trackid = " + str(tid) + "")
                con.commit()
            self.songCur = 0
            cur.execute(
                "SELECT milliseconds FROM track WHERE name = %s LIMIT 1", (str(names),))
            opcion3 = cur.fetchall()
            if len(opcion3) == 0:
                cur.execute(
                "SELECT milliseconds FROM track WHERE name = '" + str(second[0]) + "' LIMIT 1")
                opcion3 = cur.fetchall()
                if len(opcion3) == 0:
                    opcion3.append(300000)
            s = str(opcion3[0])
            s = s.replace(',', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            self.songDur = (float(s)) / 1000

            self.name1.text = "Now Playing: " + str(conserv)
            Clock.schedule_interval(self.playtime, 1)

    def buy(self, indexe):
        if indexe == 1:
            names = self.pl1.text
            seco = self.segund[0]
        elif indexe == 2:
            names = self.pl2.text
            seco = self.segund[1]
        elif indexe == 3:
            names = self.pl3.text
            seco = self.segund[2]
        elif indexe == 4:
            names = self.pl4.text
            seco = self.segund[3]
        elif indexe == 5:
            names = self.pl5.text
            seco = self.segund[4]
        elif indexe == 6:
            names = self.pl6.text
            seco = self.segund[5]
        elif indexe == 7:
            names = self.pl7.text
            seco = self.segund[6]
        elif indexe == 8:
            names = self.pl8.text
            seco = self.segund[7]
        elif indexe == 9:
            names = self.pl9.text
            seco = self.segund[8]
        elif indexe == 10:
            names = self.pl10.text
            seco = self.segund[9]
        if str(names) != "":
            NineteenWindow.songsele = names
            NineteenWindow.seco = seco
            self.manager.transition.direction = "left"
            self.manager.current = 'cart'


class NineteenWindow(Screen):
    songsele = ""
    seco = ""
    userActual = ""

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

    avail = []
    totalprice = 0


    def on_enter(self, *args):
        self.addSel()
    def addSel(self):
        if len(self.avail) < 10:
            if self.songsele not in self.avail:
                self.avail.append(self.songsele)
                self.setS()


    def setS(self):
        if len(self.avail) <= 10:
            self.pl1.text = ""
            self.pl2.text = ""
            self.pl3.text = ""
            self.pl4.text = ""
            self.pl5.text = ""
            self.pl6.text = ""
            self.pl7.text = ""
            self.pl8.text = ""
            self.pl9.text = ""
            self.pl10.text = ""
            if len(self.avail) > 0 and self.avail[0]:
                self.pl1.text = self.avail[0]
                if len(self.avail) > 1:
                    self.pl2.text = self.avail[1]
                    if len(self.avail) > 2:
                        self.pl3.text = self.avail[2]
                        if len(self.avail) > 3:
                            self.pl4.text = self.avail[3]
                            if len(self.avail) > 4:
                                self.pl5.text = self.avail[4]
                                if len(self.avail) > 5:
                                    self.pl6.text = self.avail[5]
                                    if len(self.avail) > 6:
                                        self.pl7.text = self.avail[6]
                                        if len(self.avail) > 7:
                                            self.pl8.text = self.avail[7]
                                            if len(self.avail) > 8:
                                                self.pl9.text = self.avail[8]
                                                if len(self.avail) > 8:
                                                    self.pl10.text = self.avai[9]

    def removes(self, indexe):
        print(self.avail[indexe - 1])
        self.avail.remove(self.avail[indexe - 1])
        self.setS()

    found = True
    def checkout(self):
        if len(self.avail) > 0:
            cur.execute(
                "SELECT MAX(invoicelineid) + 1 FROM invoiceline")
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", "")
            print(r)
            print(opcion3)
            self.invoicelineid = int(r)

            cur.execute(
                "SELECT MAX(invoiceid) + 1 FROM invoiceline")
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.invoiceid = int(r)

            cur.execute(
                "SELECT customer.customerid FROM customer INNER JOIN users on customer.customerid = users.customerid WHERE users.username = '" + str(self.userActual) + "'")
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.cusid = int(r)

            today = datetime.datetime.now()
            d1 = today.strftime("%Y-%m-%d %H:%M:%S")

            cur.execute(
                "SELECT address FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.address = str(r)

            cur.execute(
                "SELECT city FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.city = str(r)

            cur.execute(
                "SELECT state FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.state = str(r)

            cur.execute(
                "SELECT country FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            self.country = str(r)

            cur.execute(
                "SELECT postalcode FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            self.postal = str(r)

            i = 0
            for r in self.avail:

                titl = r.split(" by", 1)
                print(titl)
                cur.execute(
                    "SELECT trackid FROM track WHERE name = '" + str((titl[0])) + "' LIMIT 1")
                opcion3 = cur.fetchall()
                r = str(opcion3)
                r = r.replace('[', "")
                r = r.replace(']', "")
                r = r.replace('(', "")
                r = r.replace(')', "")
                r = r.replace("'", "")
                r = r.replace('"', "")
                r = r.replace(",", '')
                print(opcion3)
                if len(opcion3):
                    self.idss = 3
                    self.found = False
                else:

                    self.idss = int(r)

                cur.execute(
                    "SELECT unitprice FROM track WHERE trackid = " + str(self.idss))
                opcion3 = cur.fetchall()
                r = str(opcion3)
                r = r.replace('[', "")
                r = r.replace(']', "")
                r = r.replace('(', "")
                r = r.replace(')', "")
                r = r.replace('Decimal', "")
                r = r.replace("'", "")
                r = r.replace('"', "")
                r = r.replace(",", '')
                print(opcion3)
                self.price = float(r)

                if self.found == True:
                    cur.execute(
                        "INSERT INTO invoiceline VALUES("+ str((self.invoicelineid + i))+", "+str(self.invoiceid) +", "+ str(self.idss) +", "+ str(self.price) +", 1)")
                    con.commit()

                self.totalprice += self.price
                i += 1

            if self.found == True:
                cur.execute("INSERT INTO invoice VALUES(" + str(self.invoiceid) + ", " + str(self.cusid) + ", '" + str(
                    d1) + "', '" + self.address + "', '" + self.city + "', '" + self.state + "', '" + self.country + "', '" + str(
                    self.postal) + "', " + str(self.totalprice) + ")")
                con.commit()

        self.dpdf()

    def dpdf(self):
        textLines = []
        userp = "Username: " + self.userActual
        billinga = "Billing address: " + self.address + ", " + self.country
        totalpd = "Total: " + str(self.totalprice)
        textLines.append(userp)
        textLines.append(billinga)
        textLines.append(totalpd)
        pdf = canvas.Canvas('Receipt.pdf')
        pdf.setTitle("Empire Receipt")
        pdf.setFont('Helvetica', 36)
        pdf.drawCentredString(300, 750, "Empire Music")
        pdf.setFont('Helvetica', 25)
        pdf.drawInlineImage("Images/emp.png", 100, 380)
        pdf.drawCentredString(290, 240, "Purchase Receipt")
        pdf.line(30, 230, 550, 230)
        text = pdf.beginText(40, 180)
        text.setFont("Helvetica", 18)
        for line in textLines:
            text.textLine((line))

        pdf.drawText(text)
        pdf.line(30, 130, 550, 130)
        pdf.drawCentredString(290, 100, "Thank you for using our service!")
        pdf.save()

class TwentyWindow(Screen):
    ntracks = ObjectProperty(None)
    date = ObjectProperty(None)
    resu = ObjectProperty(None)

    invoicelineid = ""
    invoiceid = ""
    idss = 0
    price = 0
    totalprice = 0
    country = ""
    state = ""
    city = ""
    postal = ""
    address = ""
    cusid = 0
    cusname = ""

    traks = []
    def simulate(self):
        cur.execute(
            "SELECT MAX(trackid) FROM track")
        opcion3 = cur.fetchall()
        r = str(opcion3)
        r = r.replace('[', "")
        r = r.replace(']', "")
        r = r.replace('(', "")
        r = r.replace(')', "")
        r = r.replace("'", "")
        r = r.replace('"', "")
        r = r.replace(",", "")
        maxt = int(r)
        ntr = int(str(self.ntracks.text))

        cur.execute(
            "SELECT MAX(invoiceid) + 1 FROM invoiceline")
        opcion3 = cur.fetchall()
        r = str(opcion3)
        r = r.replace('[', "")
        r = r.replace(']', "")
        r = r.replace('(', "")
        r = r.replace(')', "")
        r = r.replace("'", "")
        r = r.replace('"', "")
        r = r.replace(",", '')
        print(opcion3)
        self.invoiceid = int(r)
        rand4 = random.randint(1, 62)
        self.cusid = rand4

        cur.execute(
            "SELECT firstname FROM customer WHERE customerid = " + str(self.cusid))
        opcion3 = cur.fetchall()
        r = str(opcion3)
        r = r.replace('[', "")
        r = r.replace(']', "")
        r = r.replace('(', "")
        r = r.replace(')', "")
        r = r.replace("'", "")
        r = r.replace('"', "")
        r = r.replace(",", '')
        print(opcion3)
        self.cusname = str(r)

        i = 0
        while i < ntr:
            rand = random.randint(1, maxt)
            if rand not in self.traks:
                self.traks.append(rand)

            i += 1

        for e in self.traks:
            rand2 = random.randint(50, 1000)
            cur.execute(
                "UPDATE track SET views = " + str(rand2) + " , modify = '" + self.cusname + "' WHERE trackid = " + str(e) + "")
            con.commit()

            rand3 = random.randint(10, 300)

            cur.execute(
                "SELECT MAX(invoicelineid) + 1 FROM invoiceline")
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", "")
            print(r)
            print(opcion3)
            self.invoicelineid = int(r)




            today = datetime.datetime.now()
            d1 = today.strftime("%Y-%m-%d %H:%M:%S")

            cur.execute(
                "SELECT address FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.address = str(r)

            cur.execute(
                "SELECT city FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.city = str(r)

            cur.execute(
                "SELECT state FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.state = str(r)

            cur.execute(
                "SELECT country FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            self.country = str(r)

            cur.execute(
                "SELECT postalcode FROM customer WHERE customerid = " + str(self.cusid))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            self.postal = str(r)

            i = 0


            cur.execute(
                "SELECT unitprice FROM track WHERE trackid = " + str(e))
            opcion3 = cur.fetchall()
            r = str(opcion3)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace('Decimal', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(",", '')
            print(opcion3)
            self.price = float(r)

            cur.execute(
                "INSERT INTO invoiceline VALUES(" + str((self.invoicelineid + i)) + ", " + str(
                    self.invoiceid) + ", " + str(e) + ", " + str(self.price) + ", " + str(rand3) +")")
            con.commit()

        cur.execute("INSERT INTO invoice VALUES(" + str(self.invoiceid) + ", " + str(self.cusid) + ", '" + str(
            self.date.text) + "', '" + self.address + "', '" + self.city + "', '" + self.state + "', '" + self.country + "', '" + str(
            self.postal) + "', " + str(self.totalprice) + ")")
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
            self.state = 1
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
            Clock.unschedule(self.playtime)
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
    pl11 = ObjectProperty(None)
    pl12 = ObjectProperty(None)
    estado = False
    datei = ObjectProperty(None)
    datef = ObjectProperty(None)
    datei2 = ObjectProperty(None)
    datef2 = ObjectProperty(None)
    datei3 = ObjectProperty(None)
    datef3 = ObjectProperty(None)
    arti3 = ObjectProperty(None)
    ntrack3 = ObjectProperty(None)

    p9 = ""
    p10 = ""
    p11 = ""
    p12 = ""
    opcion9 = []

    def reporte9(self):
        fecha1 = self.datei.text
        fecha2 = self.datef.text
        cur.execute(
            "CREATE OR REPLACE VIEW weeksales AS SELECT invoice.invoiceid, invoicedate, invoicelineid, trackid, unitprice, quantity, EXTRACT(WEEK FROM invoicedate) as week, EXTRACT(YEAR FROM invoicedate) as year FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid")
        con.commit()
        cur.execute(
            "SELECT sum(unitprice), year, week FROM weeksales WHERE invoicedate < %s AND invoicedate > %s GROUP BY year, week ORDER BY year, week",
            (fecha2, fecha1,))
        self.opcion9 = cur.fetchall()
        price = []
        year = []
        week = []
        for r in self.opcion9:
            price.append(r[0])
            year.append(r[1])
            week.append(r[2])

        rep9 = [("Year  Week  Sales")]

        i = 0
        for r in price:
            rep9.append(str(int(year[i])) + '    ' + str(int(week[i])) + '      ' + str(float(r)))
            i += 1
        for r in rep9:
            r = str(rep9)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace(", ", '\n')
        self.pl9.text = r

    opcion10 = []

    def reporte10(self):
        fecha1 = self.datei2.text
        fecha2 = self.datef2.text
        N = self.nart.text
        cur.execute(
            "CREATE OR REPLACE VIEW mostSoldArtist AS SELECT artist.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN album ON album.albumid = track.albumid INNER JOIN artist ON artist.artistid = album.artistid")
        con.commit()
        cur.execute(
            "SELECT name, count(*) FROM mostSoldArtist WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC LIMIT %s",
            (fecha2, fecha1, N,))
        self.opcion10 = cur.fetchall()
        name = []
        sales = []
        for r in self.opcion10:
            name.append(r[0])
            sales.append(r[1])

        rep10 = [("Artist                                                Sales")]

        i = 0
        for r in name:
            rep10.append(str(name[i]) + '                        ' + str(float(sales[i])))
            i += 1
        for r in rep10:
            r = str(rep10)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl10.text = r

    opcion11 = []

    def reporte11(self):
        fecha1 = self.datei3.text
        fecha2 = self.datef3.text
        cur.execute(
            "CREATE OR REPLACE VIEW mostSoldGenres AS SELECT genre.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN genre ON track.genreid = genre.genreid")
        con.commit()
        cur.execute(
            "SELECT name, count(*) FROM mostSoldGenres WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC",
            (fecha2, fecha1,))
        self.opcion11 = cur.fetchall()
        genre = []
        sales = []
        for r in self.opcion11:
            genre.append(r[0])
            sales.append(r[1])
            # print(f"{r[0]}\t{r[1]}")

        rep11 = [("Genre                        Sales")]

        i = 0
        for r in genre:
            rep11.append(str(genre[i]) + '                        ' + str(float(sales[i])))
            i += 1
        for r in rep11:
            r = str(rep11)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl11.text = r

    opcion12 = []
    def reporte12(self):
        arti3 = self.arti3.text
        ntrack3 = self.ntrack3.text
        cur.execute(
            "CREATE OR REPLACE VIEW songsReproduced AS SELECT artist.name as artist, track.name as track, track.views as views FROM artist INNER JOIN track ON artist.name = track.composer")
        con.commit()
        cur.execute(
            "SELECT artist, track, count(*) FROM songsReproduced WHERE artist = %s GROUP BY artist, track ORDER BY COUNT(*) DESC, track LIMIT %s",
            (arti3, ntrack3,))
        opcion12 = cur.fetchall()
        artist = []
        track = []
        views = []
        for r in opcion12:
            artist.append(r[0])
            track.append(r[1])
            views.append(r[2])

        rep12 = [("Artist           Song            Listens")]

        i = 0
        for r in artist:
            rep12.append(str(artist[i]) + '            ' + str(float(track[i]))  + '              ' + str(float(views[i])))
            i += 1
        for r in rep12:
            r = str(rep12)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl12.text = r

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

            elif indexe == 9:
                headin = str(self.ids.repo9.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Sales", "Year", "Week"])
                for line in self.opcion9:
                    writer.writerow(line)
            elif indexe == 10:
                headin = str(self.ids.repo10.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Sales"])
                for line in self.opcion10:
                    writer.writerow(line)
            elif indexe == 11:
                headin = str(self.ids.repo11.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Genre", "Sales"])
                for line in self.opcion11:
                    writer.writerow(line)
            elif indexe == 12:
                headin = str(self.ids.repo12.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Song", "Reproducctions"])
                for line in self.opcion12:
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
    pl11 = ObjectProperty(None)
    pl12 = ObjectProperty(None)
    estado = False
    datei = ObjectProperty(None)
    datef = ObjectProperty(None)
    datei2 = ObjectProperty(None)
    datef2 = ObjectProperty(None)
    datei3 = ObjectProperty(None)
    datef3 = ObjectProperty(None)
    arti3 = ObjectProperty(None)
    ntrack3 = ObjectProperty(None)

    p9 = ""
    p10 = ""
    p11 = ""
    p12 = ""
    opcion9 = []
    def reporte9(self):
        fecha1 = self.datei.text
        fecha2 = self.datef.text
        cur.execute(
            "CREATE OR REPLACE VIEW weeksales AS SELECT invoice.invoiceid, invoicedate, invoicelineid, trackid, unitprice, quantity, EXTRACT(WEEK FROM invoicedate) as week, EXTRACT(YEAR FROM invoicedate) as year FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid")
        con.commit()
        cur.execute(
            "SELECT sum(unitprice), year, week FROM weeksales WHERE invoicedate < %s AND invoicedate > %s GROUP BY year, week ORDER BY year, week",
            (fecha2, fecha1,))
        self.opcion9 = cur.fetchall()
        price = []
        year = []
        week = []
        for r in self.opcion9:
            price.append(r[0])
            year.append(r[1])
            week.append(r[2])

        rep9 = [("Year  Week  Sales")]

        i = 0
        for r in price:
            rep9.append(str(int(year[i])) + '    ' + str(int(week[i])) + '      ' + str(float(r)))
            i += 1
        for r in rep9:
            r = str(rep9)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace(", ", '\n')
        self.pl9.text = r

    opcion10 = []
    def reporte10(self):
        fecha1 = self.datei2.text
        fecha2 = self.datef2.text
        N = self.nart.text
        cur.execute(
            "CREATE OR REPLACE VIEW mostSoldArtist AS SELECT artist.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN album ON album.albumid = track.albumid INNER JOIN artist ON artist.artistid = album.artistid")
        con.commit()
        cur.execute(
            "SELECT name, count(*) FROM mostSoldArtist WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC LIMIT %s",
            (fecha2, fecha1, N,))
        self.opcion10 = cur.fetchall()
        name = []
        sales = []
        for r in self.opcion10:
            name.append(r[0])
            sales.append(r[1])

        rep10 = [("Artist                                                Sales")]

        i = 0
        for r in name:
            rep10.append(str(name[i]) + '                        ' + str(float(sales[i])))
            i += 1
        for r in rep10:
            r = str(rep10)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl10.text = r

    opcion11 = []
    def reporte11(self):
        fecha1 = self.datei3.text
        fecha2 = self.datef3.text
        cur.execute(
            "CREATE OR REPLACE VIEW mostSoldGenres AS SELECT genre.name, invoice.invoicedate FROM invoice INNER JOIN invoiceline ON invoice.invoiceid = invoiceline.invoiceid INNER JOIN track ON track.trackid = invoiceline.trackid INNER JOIN genre ON track.genreid = genre.genreid")
        con.commit()
        cur.execute(
            "SELECT name, count(*) FROM mostSoldGenres WHERE invoicedate < %s AND invoicedate > %s GROUP BY name ORDER BY count(*) DESC",
            (fecha2, fecha1,))
        self.opcion11 = cur.fetchall()
        genre = []
        sales = []
        for r in self.opcion11:
            genre.append(r[0])
            sales.append(r[1])
            # print(f"{r[0]}\t{r[1]}")

        rep11 = [("Genre                        Sales")]

        i = 0
        for r in genre:
            rep11.append(str(genre[i]) + '                        ' + str(float(sales[i])))
            i += 1
        for r in rep11:
            r = str(rep11)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl11.text = r

    opcion12 = []
    def reporte12(self):
        arti3 = self.arti3.text
        ntrack3 = self.ntrack3.text
        cur.execute(
            "CREATE OR REPLACE VIEW songsReproduced AS SELECT artist.name as artist, track.name as track, track.views as views FROM artist INNER JOIN track ON artist.name = track.composer")
        con.commit()
        cur.execute(
            "SELECT artist, track, count(*) FROM songsReproduced WHERE artist = %s GROUP BY artist, track ORDER BY COUNT(*) DESC, track LIMIT %s",
            (arti3, ntrack3,))
        opcion12 = cur.fetchall()
        artist = []
        track = []
        views = []
        for r in opcion12:
            artist.append(r[0])
            track.append(r[1])
            views.append(r[2])

        rep12 = [("Artist           Song            Listens")]

        i = 0
        for r in artist:
            rep12.append(str(artist[i]) + '      ' + str(track[i] + '              ' + str(int(views[i]))))
            i += 1
        for r in rep12:
            r = str(rep12)
            r = r.replace('[', "")
            r = r.replace(']', "")
            r = r.replace("'", "")
            r = r.replace('"', "")
            r = r.replace(", ", '\n')
        self.pl12.text = r
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

            elif indexe == 9:
                headin = str(self.ids.repo9.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Sales", "Year", "Week"])
                for line in self.opcion9:
                    writer.writerow(line)
            elif indexe == 10:
                headin = str(self.ids.repo10.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Sales"])
                for line in self.opcion10:
                    writer.writerow(line)
            elif indexe == 11:
                headin = str(self.ids.repo11.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Genre", "Sales"])
                for line in self.opcion11:
                    writer.writerow(line)

            elif indexe == 12:
                headin = str(self.ids.repo12.text)
                print(headin)
                writer.writerow([headin])
                writer.writerow(["Artist", "Song", "Reproducctions"])
                for line in self.opcion12:
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

    userActual = ""
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
        today = ""
        today = datetime.datetime.now()
        d1 = today.strftime("%Y-%m-%d")
        d2 = today.strftime("%H:%M:%S")
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
            cur.execute("INSERT INTO bitacora VALUES(%s, %s, %s) ", (d1, d2, self.userActual,))
            con.commit()
            print("Se ha eliminado la cancion de la base de datos")

    def elimAlbum(self, name):

        today = ""
        today = datetime.datetime.now()
        d1 = today.strftime("%Y-%m-%d")
        d2 = today.strftime("%H:%M:%S")
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
        cur.execute("INSERT INTO bitacora VALUES(%s, %s, %s) ", (d1, d2, self.userActual,))
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

        today = ""
        today = datetime.datetime.now()
        d1 = today.strftime("%Y-%m-%d")
        d2 = today.strftime("%H:%M:%S")
        cur.execute("DELETE FROM artist WHERE name= %s", (name,))
        con.commit()
        cur.execute("INSERT INTO bitacora VALUES(%s, %s, %s) ", (d1, d2, self.userActual,))
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
    pl1 = ObjectProperty(None)
    pl2 = ObjectProperty(None)
    pl3 = ObjectProperty(None)
    p1 = ""
    p2 = ""
    p3 = ""

    def on_enter(self, *args):
        self.resBit()

    def resBit(self):
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
        self.pl1.text = r

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
        self.pl2.text = r

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
        self.pl3.text = r


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
        datei = "from " + indate1 + " to " + indate2
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

#Recomendaciones a 10 clientes
class EightteenWindow(Screen):
    pl1 = ObjectProperty(None)
    pl2 = ObjectProperty(None)
    p1 = ""
    p2 = ""
    p3 = ""

    def on_enter(self, *args):
        self.refSu()

    def refSu(self):
        cur.execute("SELECT genreid FROM track WHERE trackid > (SELECT MAX(trackid) - 100 FROM track) ORDER by trackid DESC")
        opcion5 = cur.fetchall()
        paso1 = []
        for r in opcion5:
            r = str(r)
            r = r.replace('(', "")
            r = r.replace(')', "")
            r = r.replace(",", '')
            r = r.replace("'", '')
            r = int(r)
            if r not in paso1:
                paso1.append(r)

        print(paso1)
        paso2 = []
        for i in paso1:
            cur.execute(
                "SELECT invoiceid FROM invoiceline INNER JOIN track on invoiceline.trackid = track.trackid WHERE track.genreid = " + str(i) + " GROUP by invoiceid ORDER by invoiceid DESC LIMIT 2")
            opcion5 = cur.fetchall()
            report2 = []
            for r in opcion5:
                r = str(r)
                r = r.replace('(', "")
                r = r.replace(')', "")
                r = r.replace(",", '')
                r = r.replace("'", '')
                r = int(r)
                if r not in report2 and len(paso2) < 10:
                    paso2.append(r)

        paso3 = []
        for i in paso2:
            cur.execute(
                "SELECT firstname, lastname FROM customer WHERE customerid = (SELECT customerid FROM invoice WHERE invoiceid = " + str(i) +")")
            opcion5 = cur.fetchall()
            report3 = []
            for r in opcion5:
                paso3.append(r)

        r = str(paso3)
        r = r.replace('), ', "\n")
        r = r.replace('(', "")
        r = r.replace(')', "")
        r = r.replace(",", '')
        r = r.replace("'", '')
        r = r.replace('[', "")
        r = r.replace(']', "")
        self.pl1.text = r
        print(self.pl1.text)

        el = 0
        canc = []
        secn = []
        for i in paso1[0:5]:
            cur.execute(
                "SELECT name, composer FROM track WHERE genreid = " + str(i) + " ORDER by trackid DESC LIMIT 5")
            opcion5 = cur.fetchall()
            for r in opcion5:
                if el == 4:
                    secn.append(r)
                    canc.append(secn)
                    canc.append(secn)
                    secn = []
                    el = 0
                else:
                    secn.append(r)
                    el += 1
        print(canc)

        r = str(canc)
        r = r.replace(')], ', "\n")
        r = r.replace('), ', ", ")
        r = r.replace("', '", " by ")
        r = r.replace(', None', "")
        r = r.replace('(', "")
        r = r.replace(')', "")
        r = r.replace("'", '')
        r = r.replace('[', "")
        r = r.replace(']', "")
        self.pl2.text = r



class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()


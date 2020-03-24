#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, sql

# for the sys.exit() method call
import sys

# import the Pygame libraries
import pygame
from pygame.locals import *

# set the DB name, table, and table data to 'None'
table_data = None
db_name = None
table_name = None

# change these globals to match your settings
user_name = "objectrocket"
user_pass = "mypass"

# create a class for the buttons and labels
class Button():

    # empty list for button registry
    registry = []

    # selected button (will have outline rect)
    selected = None

    # pygame RGBA colors
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    red = (255, 0, 0, 255)
    green = (50, 205, 50, 255)
    light_blue = (173, 216, 230, 255)

    # default font color for buttons/labels is white
    def __init__(self, name, loc, color=white):

        # add button to registry
        self.registry.append(self)

        # paramater attributes
        self.name = name

        self.loc = loc
        self.color = color

        # text attr for button
        self.text = ""

        # size of button changes depending on length of text
        self.size = (int(len(self.text)*200), 200)

        # font.render(text, antialias, color, background=None) -> Surface
        self.font = font.render (
            self.name + " " + self.text, # display text
            True, # antialias on
            self.color, # font color
            self.black # background color
        )

        # rect for button
        self.rect = self.font.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

# function that connects to Postgres
def connect_postgres(db):

    # connect to PostgreSQL
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            dbname = postgres,
            user = postgres,
            host = "localhost",
            password = 1234
        )
    except Exception as err:

        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    # return the connection object
    return conn

# function that returns PostgreSQL records
def return_records(conn):

    # instantiate a new cursor object
    cursor = conn.cursor()

    # use sql.SQL() to prevent SQL injection attacks
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        "SELECT * FROM {} LIMIT 20;"
    ).format(
        # pass the identifier to the Identifier() method
        sql.Identifier( table_name )
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        table_data = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        table_data = None

    return table_data

# initialize the pygame window
pygame.init()

# change the caption/title for the Pygame app
pygame.display.set_caption("ObjectRocket PostgreSQL App", "ObjectRocket PostgreSQL App")

# get the OS screen/monitor resolution
max_width = pygame.display.Info().current_w
max_height = pygame.display.Info().current_h

# create a pygame resizable screen
screen = pygame.display.set_mode(
    (int(max_width*0.55), int(max_height*0.6)),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)
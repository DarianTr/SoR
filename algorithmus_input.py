from sqlalchemy import *  
import sqlalchemy.orm
import structure
from flask import session
from config import database_url


################################################################

##########################  DATABASE  ##########################


engine = create_engine(database_url, echo=True)
engine.connect()


with sqlalchemy.orm.Session(engine) as session:
    s = session.query(structure.Person).where(structure.Person.position == 'Schueler')
    list_of_students = s.all()


    s = session.query(structure.Workshop)
    list_of_projects = s.all()



################################################################

########################### Classes ############################


class Schueler:
    def __init__(self, name, klasse, wunsch1, wunsch2, wunsch3):
        self.name = name
        self.klasse = klasse
        self.wunsch1 = wunsch1
        self.wunsch2 = wunsch2
        self.wunsch3 = wunsch3
        self.project = "noch nichts"
    
    
class Project:
    def __init__(self, name, minKlasse, maxKlasse, minTeilnehmer, maxTeilnehmer):
        self.name = name
        self.minTeilnehmer = minTeilnehmer
        self.maxTeilnehmer = maxTeilnehmer
        self.minKlasse = minKlasse
        self.maxKlasse = maxKlasse
        self.anzahlTeilnehmer = 0
    def free(self):
        return self.anzahlTeilnehmer < self.maxTeilnehmer
    def increment(self):
        self.anzahlTeilnehmer += 1
    def decrement(self):
        self.anzahlTeilnehmer -= 1
    def zustandekommen(self):
        return self.anzahlTeilnehmer >= self.minTeilnehmer
    def diff_zustandekommen(self):
        return self.minTeilnehmer - self.anzahlTeilnehmer
    
        
################################################################

#########################  Testdaten  ##########################

Schueler2 = [
    Schueler("Thomas Mueller", 8, "Bio", "Chemie", "Physik"),
    Schueler("Christine Kopa", 10, "Geschichte", "PW", "Bio"),
    Schueler("Ana Lardt", 11, "Bio", "PW", "Englisch"),
    Schueler("Hank Lies", 8, "Physik", "Mathe", "Geo"),
    Schueler("Margarete Schneider", 9, "Physik", "Chemie", "Bio"),
    Schueler("Lise Fiels", 10, "Mathe", "Physik", "Bio"),
    Schueler("Bernardt Fachs", 12, "Bio", "Physik", "Englisch"),
    Schueler("Hannoke Karke", 9, "Physik", "Physik", "Englisch"),
    Schueler("Bilou Zambaar", 10, "Englisch", "Physik", "PW"),
     Schueler("Paul Klein", 11, "Geschichte", "PW", "Chemie"),
     Schueler("Hilde Affenhartz" , 9, "Physik", "Bio", "Chemie")
]



Projekt1 = [
    Project("Physik", minKlasse = 6, maxKlasse = 12, minTeilnehmer = 2, maxTeilnehmer =  2),
    Project("Bio", minKlasse = 6, maxKlasse = 12, minTeilnehmer = 1, maxTeilnehmer = 1),
    Project("Chemie", 6, 12, 1, 2),
    Project("Geschichte", 0, 12, 1, 2),
    Project("PW", 8, 12, 1, 1),
    Project("Englisch", 1, 12, 1, 1),
    Project("Mathe", 2, 12, 1, 1),
    Project("Geo", 4, 12, 1, 10)
]

################################################################

#######################  CONST FOR COST  #######################

COST_1 = 100
COST_2 = 75
COST_3 = 50
COST_N = 0            # COST_N: Kosten wenn man in keines seiner gewünschten Projekte kommt

####################### HIGHER IS BETTER #######################

################################################################




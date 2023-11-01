
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, Text, Table, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN
from website import database
from sqlalchemy import create_engine
from config import database_url
from flask_login import UserMixin
from alembic import command
import datetime

engine = create_engine(database_url, echo=True)
engine.connect()


class Job(database.Model):
    __tablename__ = 'Job'
    id = Column(Integer, primary_key=True)
    status = Column(Text)
    start = Column(DateTime, default=datetime.datetime.now)
    finish = Column(DateTime)
    message = Column(Text)
    started_by = Column(ForeignKey('Person.id'), index = True)
    cost = Column(Integer)

    starter = relationship('Person', foreign_keys =[started_by])
class Workshop(database.Model):
    __tablename__ = 'Workshop'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    minTeilnehmer = Column(INTEGER(10))
    maxTeilnehmer = Column(INTEGER(10))
    minKlasse = Column(INTEGER(10))
    maxKlasse = Column(INTEGER(10))     
    anzahlTeilnehmer = Column(INTEGER(10))
    kurzbeschreibung = Column(Text)
    
    

class Person(database.Model, UserMixin):

    __tablename__ = 'Person'
    
    id = Column(INTEGER(10), primary_key=True)
    vorname = Column(Text)
    nachname = Column(Text)
    klassenstufe = Column(INTEGER(10))
    # erstwunsch = Column(INTEGER(10), ForeignKey('Workshop.name'), index = True)
    # zweitwunsch = Column(INTEGER(10),ForeignKey('Workshop.name'), index = True)
    # drittwunsch = Column(INTEGER(10),ForeignKey('Workshop.name'), index = True)
    # projekt = Column(INTEGER(10),ForeignKey('Workshop.name'))
    _wunsch1_id = Column(ForeignKey('Workshop.id'), index = True, nullable=True)
    _wunsch2_id = Column(ForeignKey('Workshop.id'), index = True, nullable=True)
    _wunsch3_id = Column(ForeignKey('Workshop.id'), index = True, nullable=True)
    _projekt_id = Column(ForeignKey('Workshop.id'), index = True, nullable=True)
    position = Column(Text)
    username = Column(Text, unique = True)
    password = Column(Text)
    
    wunsch1 = relationship('Workshop', foreign_keys =[_wunsch1_id])
    wunsch2 = relationship('Workshop', foreign_keys =[_wunsch2_id])
    wunsch3 = relationship('Workshop', foreign_keys =[_wunsch3_id])
    projekt = relationship('Workshop', foreign_keys =[_projekt_id])
        
        
    #def __init__(self, position):
    #   self.position = position
    def pos(self):
        return self.position
        # erstwunsch1 = relationship('erstwunsch', primaryjoin='Workshop.name == Schueler.erstwunsch')
        # zweitwunsch2 = relationship('zweitwunsch', secondary='Workshop', backref='Schueler')
        # drittwunsch3 = relationship('drittwunsch', secondary='Workshop', backref='Schueler')
        # projekt4 = relationship('projekt', secondary='Workshop', backref='Schueler')
        # Workshop1 = relationship("Workshop", primaryjoin='Schuler.zweitwunsch == Workshop.name')
        # Workshop2 = relationship("Workshop", primaryjoin='Schuler.drittwunsch == Workshop.name')
        # Workshop3 = relationship("Workshop", primaryjoin='Schuler.projekt == Workshop.name')
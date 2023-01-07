
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, Text, Table, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER
from website import database
from sqlalchemy import create_engine
from config import database_url
from flask_login import UserMixin
from alembic import command

engine = create_engine(database_url, echo=True)
engine.connect()

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
    erstwunsch = Column(ForeignKey('Workshop.name'), index = True)
    zweitwunsch = Column(ForeignKey('Workshop.name'), index = True)
    drittwunsch = Column(ForeignKey('Workshop.name'), index = True)
    projekt = Column(ForeignKey('Workshop.name'), index = True)
    position = Column(Text)
    username = Column(Text)
    password = Column(Text)
    
    wunsch1 = relationship('Workshop', foreign_keys =[erstwunsch])
    wunsch2 = relationship('Workshop', foreign_keys =[zweitwunsch])
    wunsch3 = relationship('Workshop', foreign_keys =[drittwunsch])
    result = relationship('Workshop', foreign_keys =[projekt])
        
        
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
from app import database, engine
import structure
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import query

with sqlalchemy.orm.Session(engine) as session:
    s = session.query(structure.Schueler.id, structure.Schueler.erstwunsch, structure.Schueler.zweitwunsch, structure.Schueler.drittwunsch) 
    result = session.execute(s)
    list_of_tuples = []
    # for row in result:
    #     list_of_tuples.append((row[0], (row[1], row[2], row[3])))
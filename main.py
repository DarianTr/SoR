from SoR.website import database, engine
import SoR.structure
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import query

# with sqlalchemy.orm.Session(engine) as session:
#     s = session.query(structure.Person.id, structure.Person.erstwunsch, structure.Person.zweitwunsch, structure.Person.drittwunsch) 
#     result = session.execute(s)
#     list_of_tuples = []
#     # for row in result:
#     #     list_of_tuples.append((row[0], (row[1], row[2], row[3])))
from SoR.website import create_app
app = create_app()


if __name__ == '__main__':
    app.run(host='192.168.0.94', debug=True, threaded=True)
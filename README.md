# **Informationen**

## **Alembic**

Aenderungen der Datenbank bitte immer ueber structure.py

aktuelle Version herausfinden:
> $ alembic current

Die Aenderungen speichern:
> $ alembic revision --autogenerate -m "beschreibung"

Die Aenderungen auf die Datenbank uebertragen:
> $ alembic upgrade +1

Die Aenderungen rueckgaengig machen:
> $ alembic downgrade -1

Weitere Informationen:
<https://alembic.sqlalchemy.org/en/latest/tutorial.html>

## **Requirements.txt install**

Alle benoetigten module sollen in die datei geschrieben werden. Moeglicherweise muss der Pfad vollstaendig angegeben werden.

> $ pip install -r requirements.txt

## **Datenbankeinstellungen**

Datei `config.py.dist` nach `config.py` kopieren und

- `USER` ersetzen
- `PASSWORD` ersetzen
- `DATABASE` ersetzen
- `SECRET` ersetzen

## **Testdaten**

`testData.py` und die csv-dateien in `sampleData` bieten beispiellisten zum testen des algorithmus

```python
from testData import testData
td = testData(numberOfStudents)
td.nameList # Liste mit Namen und Wünschen
td.workshopList # Liste der Workshops
```

## **React**
Um die React App zu testen ist [Node](https://nodejs.org/en/) erforderlich. Wenn das fertig installiert ist bitte noch die benötigten Module importieren (es sollte ein Ordner namens node_modules entstehen).
```shell
cd react-app
npm install
```

zum Starten der App im Standardbrowser:

```shell
cd react-app
npm start
```
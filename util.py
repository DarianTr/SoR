import string
from random import choice
import pandas as pd
from website import engine, database
from werkzeug.security import generate_password_hash
from io import StringIO

def generate_password(laenge):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(characters) for x in range(laenge))
    return password

def username_password_csv_erweiterung(file, filetype, pw_laenge, output_name):
    input = pd.read_csv(StringIO(file), sep=',', encoding='utf-8')
    input['Vorname'] = input['Vorname'].apply(lambda x: x.split(' ')[0].replace(',', ''))
    input['Nachname'] = input['Nachname'].apply(lambda x: x.split(' ')[0].replace(',', ''))
    input['Username'] = input['Vorname']+'.'+input['Nachname']
    output_name_with_extension = f"{output_name}.{filetype}"
    if filetype == 'csv':
        input.to_csv(output_name_with_extension, index=False)
    elif filetype == 'xlsx':
        input.to_excel(output_name_with_extension, index=False)
    return output_name_with_extension

def projekt_csv(file, filetype):
    # file = open(file)
    # content = file.read()
    content = file
    input = pd.read_csv(StringIO(content), sep=';', encoding='utf-8')
    print(input.columns)
    print(input)
    # NUR FÜR DATENTESTEN // MUSS NOCH UMGESCHRIEBEN WERDEN
    #schueler_liste = input['Vorname'], input['Nachname'], input['Stufe']
    #schueler_liste.to_csv("test", index=False, sep=',')
    #print(input)
    input.to_csv('schueler.csv', columns=['Vorname', 'Nachname', 'Stufe'], index=False, sep=',')

    schueler_mit_passwort = username_password_csv_erweiterung(open('schueler.csv').read(), 'csv', 7, 'testdaten_pietschmann_schueler')

    projekte = [column_name for (column_name, column) in input.transpose().iterrows() if column_name not in ['Nachname', 'Vorname', 'Stufe', 'Klasse']]


    return (schueler_mit_passwort, projekte)

# def create_schueler(csv_file):
#     data = pd.read_csv(csv_file, sep=',', encoding='utf-8')
#     for row in data.itertuples():
#         print(row[1], row[2], row[3], row[4])
#         new_user = Person(vorname=row[1], nachname=row[2], klasse=None, position='Schueler', username=row[3],  password=generate_password_hash(row[4], method='sha256'))
#         database.session.add(new_user)
#         database.session.commit()
# # username_password_csv_erweiterung('schuelerliste.csv', 'xlsx', 7)
# create_schueler('output.csv')
def wuensche(file):
    # schueler_mit_passwort = pd.read_csv(StringIO(schueler_mit_passwort.read()), sep=';', encoding='utf-8')
    # projekte = pd.read_csv(StringIO(projekte.read()), sep=';', encoding = 'utf-8')
    file = open(file)
    content = file.read()
    input = pd.read_csv(StringIO(content), sep=',', encoding='utf-8')
    
    wahl = []
    for index, rows in input.iterrows():
        row = [rows.Vorname, rows.Nachname, rows.Wunsch1, rows.Wunsch2, rows.Wunsch3]
        wahl.append(row)
    return wahl


#ad projekt_csv('/mnt/c/Users/Darian/AppData/Local/Temp/pid-28564/testdaten.csv', 'csv')
print(username_password_csv_erweiterung(open('schueler.csv', encoding='utf-8').read(), 'csv', 7, 'test'))
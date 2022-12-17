import string
from random import choice
import pandas as pd
from website import engine, database
from werkzeug.security import generate_password_hash
from structure import Person

def generate_password(laenge):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(characters) for x in range(laenge))
    return password

def username_password_csv_erweiterung(file, filetype, pw_laenge):
    input = pd.read_csv(file, sep='\t', encoding='utf-8')
    input['Username'] = input['Vorname']
    input['Username'] = input['Vorname']+'.'+input['Nachname']
    input['Password'] = input.apply(lambda x: generate_password(pw_laenge), axis=1)
    if filetype == 'csv':
        input.to_csv('output.csv', index=False)
        return 'output.csv'
    elif filetype == 'xlsx':
        input.to_excel('output.xlsx', index=False)
        return 'output.xlsx'

# def create_schueler(csv_file):
#     data = pd.read_csv(csv_file, sep=',', encoding='utf-8')
#     for row in data.itertuples():
#         print(row[1], row[2], row[3], row[4])
#         new_user = Person(vorname=row[1], nachname=row[2], klasse=None, position='Schueler', username=row[3],  password=generate_password_hash(row[4], method='sha256'))
#         database.session.add(new_user)
#         database.session.commit()
# # username_password_csv_erweiterung('schuelerliste.csv', 'xlsx', 7)
# create_schueler('output.csv')
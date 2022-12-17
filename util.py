import string
from random import choice
import pandas as pd

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
    elif filetype == 'xlsx':
        input.to_excel('output.xlsx', index=False)



# username_password_csv_erweiterung('schuelerliste.csv', 'xlsx', 7)

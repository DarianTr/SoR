import pandas as pd
from random import randint

class testData:
    def __init__(self, numberOfStudents):
        firstName = pd.read_csv('sampleData/firstname.csv')['name'].to_list()
        firstName = [i.upper() for i in firstName]
        lastName = pd.read_csv('sampleData/lastname.csv')['name'].to_list()
        workshops = pd.read_csv('sampleData/workshops.csv')['name'].to_list()
        self.workshopList = [(i+1, workshops[i]) for i in range(len(workshops))]
        self.nameList = [(firstName[i], lastName[i], randint(1, len(workshops)), randint(1, len(workshops)), randint(1, len(workshops))) for i in range(numberOfStudents)]

#Instanzierung
td = testData(100)
#Nur zum Testen, in der Implementierung bitte weglassen
for i in td.nameList:
    print(i)
print('-'*30)
for i in td.workshopList:
    print(i)
from random import choice
from algorithmus_darian import COST_1, COST_2, COST_3, COST_N, Schueler2, Projekt1


#### NICHT FETIG ####


def str_to_class(str, list):
    counter = 0
    p = list[counter]
    while p.name != str:
        counter +=1
        p = list[counter]
    return p

def check_if_free(project, projectlist):
    p= str_to_class(project, projectlist)
    return p.free()

def change_teilnehmeranzahl(project, change, projectlist): # z. B.change = -1 
    p = str_to_class(project, projectlist)
    p.anzahlTeilnehmer += change
    
    
    
def without_switching(projectlist):
    for student in Schueler2:
        if student.bool:
            if check_if_free(student.wunsch1, projectlist):
                student.project = student.wunsch1
                student.cost = COST_1
            elif check_if_free(student.wunsch2, projectlist):
                student.project = student.wunsch2
                student.cost = COST_2
            elif check_if_free(student.wunsch3, projectlist):
                student.project = student.wunsch3
                student.cost = COST_3
            else:
                list_of_free_projects = [x for x in projectlist if x.anzahlTeilnehmer < x.maxTeilnehmer and x.minKlasse <= student.klasse and x.maxKlasse >= student.klasse]
                if len(list_of_free_projects) > 0:
                    student.project = choice(list_of_free_projects).name
                    student.cost = COST_N
                else:
                        poss_partner = [x for x in Schueler2 if str_to_class(x.wunsch2, projectlist).free()]
                        if len(poss_partner) > 0:
                            partner = choice(poss_partner)
                            student.project = partner.project
                            change_project(partner, partner.wunsch2, projectlist, COST_2)
                            
                        else:                                                                           #Annahme: ab diesem Punkt wird jeder zugeordnet
                            p = [x for x in Schueler2 if str_to_class(x.wunsch2, projectlist).free()]
                            partner = choice(p)
                            student.project = partner.project
                            change_project(partner, partner.wunsch3, projectlist, COST_3)

        projectClass = str_to_class(student.project, projectlist)
        projectClass.increment()


def calculate_cost(SuS, possible_project):
    student = str_to_class(SuS, Schueler2)
    if student.wunsch1 == possible_project:
        return COST_1
    elif student.wunsch2 == possible_project:
        return COST_2
    elif student.wunsch3 == possible_project:
        return COST_3
    else:
        return COST_N
    
def calculate_change_cost(project_1, project_2, student_1, student_2): #eins zu eins tausch
    s1_cost = calculate_cost(student_1, project_2)
    s2_cost = calculate_cost(student_2, project_1)
    if s1_cost + s2_cost > student_1.cost + student_2.cost and student_1.klasse >= project_2.minKlasse and student_2.klasse <= project_1.maxKlasse and student_2.klasse >= project_1.minKlasse and student_1.klasse <= project_2.maxKlasse:
        return True
    else:
        return False
    
    '''
    schueler_in_seinem_erstwunsch = [x for x in studentlist if x.project == student.wunsch1]
            for schueler in schueler_in_seinem_erstwunsch:
                if calculate_change_cost(student.project, schueler.project, student, schueler):
                    student.project, schueler.project = schueler.project, student.project
                    break
            schueler_in_seinem_zweitwunsch = [x for x in studentlist if x.project == student.wunsch2]
            for schueler in schueler_in_seinem_zweitwunsch:
                if calculate_change_cost(student.project, schueler.project, student, schueler):
                    student.project, schueler.project = schueler.project, student.project
                    break
            schueler_in_seinem_drittwunsch = [x for x in studentlist if x.project == student.wunsch3]
            for schueler in schueler_in_seinem_drittwunsch:
                if calculate_change_cost(student.project, schueler.project, student, schueler):
                    student.project, schueler.project = schueler.project, student.project
                    break
    
    '''
def change_project(student, project, projectlist, cost):
    str_to_class(student.project, projectlist).decrement()
    student.project = project
    student.cost = cost
    str_to_class(student.project, projectlist).increment()

def switch_ppl_cost_n(projectlist, studentlist):
    st_cost_n = [x for x in studentlist if x.cost <= COST_N]
    for student in st_cost_n:
        schueler_in_seinem_erstwunsch = [x for x in studentlist if x.project == student.wunsch1]
        for schueler in schueler_in_seinem_erstwunsch:
            if check_if_free(schueler.wunsch2, projectlist):
                change_project(schueler, schueler.wunsch2, projectlist, COST_2)
                change_project(student, student.wunsch1, projectlist, COST_1)    
                break        
        for schueler in schueler_in_seinem_erstwunsch:
            if check_if_free(schueler.wunsch3, projectlist):
                change_project(schueler, schueler.wunsch3, projectlist, COST_3)
                change_project(student, student.wunsch1, projectlist, COST_1) 
                break
        schueler_in_seinem_zweitwunsch = [x for x in studentlist if x.project == student.wunsch2]
        for schueler in schueler_in_seinem_zweitwunsch:
            if check_if_free(schueler.wunsch2, projectlist):
                change_project(schueler, schueler.wunsch2, projectlist, COST_2)
                change_project(student, student.wunsch1, projectlist, COST_1)    
                break        
        for schueler in schueler_in_seinem_zweitwunsch:
            if check_if_free(schueler.wunsch3, projectlist):
                change_project(schueler, schueler.wunsch3, projectlist, COST_3)
                change_project(student, student.wunsch1, projectlist, COST_1) 
                break
    

def total_cost(Schuelerliste):
    cost = 0
    for s in Schueler2:
        cost +=s.cost
    return cost


def minTeilnehmer(projectlist, studentlist):
    startcost = total_cost(studentlist)
    nicht_zustandekommen = [x for x in projectlist if not x.zustandekommen()]     
    for project in nicht_zustandekommen:
        students_needed = project.diff_zustandekommen()
        while students_needed != 0:
            s_with_cost_1 = [x for x in studentlist if x.wunsch2 == project.name and x.project != project]
            s_with_cost_n = [x for x in studentlist if x.cost == COST_N]
            if len(s_with_cost_n) > 0:
                counter = 0
                while counter < students_needed and counter < len(s_with_cost_n):
                    partner = choice(s_with_cost_n)
                    change_project(partner, project, studentlist, COST_N)

           
                
without_switching(Projekt1)
for p in Projekt1:
    print(p.anzahlTeilnehmer)
print(total_cost(Schueler2))
switch_ppl_cost_n(Projekt1, Schueler2)
for p in Projekt1:
    print(p.anzahlTeilnehmer)
print(total_cost(Schueler2))

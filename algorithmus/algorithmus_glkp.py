
from algorithmus_input import Schueler2, Projekt1, COST_1, COST_2, COST_3, pos_of_proj, list_of_projects, list_of_students
from pymprog import * 
from itertools import product 
from random import randint


###  Schuler2 und Projekt1 sind Testdaten. 
### Um die echten Daten zu nehmen muss man Schuler2 mit list_of_students und Projekt1 mit list_of_projects austauschen


#problem data
m = len(Schueler2) # students
M = range(m) #set of students

n = len(Projekt1) # courses
N = range(n) #set of courses

c = { (i,j) : 0 for (i,j) in product(M,N) }
# randomly select first and second preference for each studen
for i in M:
    first = pos_of_proj(Schueler2[i].wunsch1, Projekt1)
    second = pos_of_proj(Schueler2[i].wunsch2, Projekt1)
    third = pos_of_proj(Schueler2[i].wunsch3, Projekt1)
    c[(i, first)] = COST_1
    c[(i, second)] = COST_2
    c[(i, third)] =  COST_3

c=[ [c[(i,j)] for j in N] for i in M ]




# maximum students per course 
t_max = [p.maxTeilnehmer for p in Projekt1]
# minimum students per course 
t_min = [p.minTeilnehmer for p in Projekt1]
# minimale Klassenstufe pro projekt
k_min = [p.minKlasse for p in Projekt1]
# maximal Klassenstufe pro projekt
k_max = [p.maxKlasse for p in Projekt1]
# klassenstufe
k_schueler = [s.klasse for s in Schueler2]


begin("assign")
#verbose(True) # for model output
A = iprod(M, N) # Descartan product 
x = var('x', A, bool) # assignment decisions

# use parameters for automatic model update
c = par('c', c) # when their values change
t_max = par('t_max', t_max)
t_min = par('t_min', t_min)
k_min = par('k_min', k_min)
k_max = par('k_max', k_max)
k_schueler = par('k_schueler', k_schueler)

maximize(sum(c[i][j]*x[i,j] for i,j in A))


# each student is assigned to exactly one course
for k in M: sum(x[k,j] for j in N)==1 

# each task is assigned at most k_max students
for k in N: t_max[k] - sum(x[i,k] for i in M) >= 0 

# each task is assigned at least k_min students
for k in N: t_min[k] - sum(x[i,k] for i in M) <= 0

#klasse max

for k in M: k_schueler[k] - sum(x[k,j]*k_max[j] for j in N) <= 0  
for k in M: k_schueler[k] - sum(x[k,j]*k_min[j] for j in N) >= 0  


def report():
    print("Total Cost = %g"%vobj())
    assign = [(i,j) for i in M for j in N 
                if x[i,j].primal == 1]
    for i,j in assign:
        print("Student %s gets Course %s"%(Schueler2[i].name, Projekt1[j].name))
    return assign

solve()
report()
end()
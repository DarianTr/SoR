import random


def clean_list(list):
    new_list = []
    # if the number of open places is not 0, then add it to a new list (will be used later for random project allocation
    for element in list:
        if element[1] != 0:
            new_list.append(element)

    return new_list


def check_grade(student):
    grade_nums = student[1].split('-') #splittling the grade at the sign -
    grade = int(grade_nums[0])
    return grade


def find_place(student, projects):
    projectname = []
    for project in projects:
        projectname.append(project[0])

    list_index1 = projectname.index(student[2]) # place of the 1st wish project in the list
    list_index2 = projectname.index(student[3])
    list_index3 = projectname.index(student[4])

    grade = check_grade(student) #finding the grade of the student

    if projects[list_index1][2] <= grade <= projects[list_index1][3] and projects[list_index1][1] > 0:
        assignedProject = projects[list_index1][0]  # assigned project, for which the student qualified
        list_index = list_index1 #the list index (specific for the 1st choice)
        num_places = projects[list_index1][1] #the number of places left for the project

    elif projects[list_index2][2] <= grade <= projects[list_index2][3] and projects[list_index2][1] > 0:
        assignedProject = projects[list_index2][0]  # assigned project, for which the student qualified
        list_index = list_index2
        num_places = projects[list_index2][1]

    elif projects[list_index3][2] <= grade <= projects[list_index3][3] and projects[list_index3][1] > 0:
        assignedProject = projects[list_index3][0]  # assigned project, for which the student qualified
        list_index = list_index3
        num_places = projects[list_index3][1]

    else:
        cleaned_list = clean_list(projects)
        list_index = random.randint(0, len(cleaned_list))
        assignedProject = cleaned_list[list_index][0]  # assigned project, for which the student qualified
        num_places = cleaned_list[list_index][1]

    return num_places, assignedProject, list_index


def decr_participant_num(numPlaces, list, index):
    # taking out whole data sentence of the specified project
    proj_tuple = list[index]
    del list[index]  # deleting it from the main list
    proj_list = [item for item in proj_tuple]  # turning the extracted tuple into a list
    del proj_list[1]  # deleting the number of empty spaces for the participants
    proj_list.insert(1, (numPlaces - 1))  # decreasing this number by 1
    list.insert(index, proj_list)  # inserting this changed list into the main list
    return list


def add_to_proj(students, allprojects):
    final_list = []
    for student in students:
        output_find_place = find_place(student, allprojects)  # assigning project to student
        decr_participant_num(output_find_place[0], allprojects, output_find_place[2])  # decreasing the number of available places at project
        final_list.append((student[0], student[1], output_find_place[1]))# making a final list in which only the student name, class and project is
    return final_list, allprojects


'''Schueler0 = [
    ("Thomas Mueller", "8-2", "Bio", "Chemie", "Physik"),
    ("Christine Kopa", "10-1", "Chemie", "Physik", "Bio"),
    ("Frankie Grant", "10-1", "Physik", "Bio", "Chemie")

]

Schueler2 = [
    ("Thomas Mueller", "8-2", "Bio", "Chemie", "Physik"),
    ("Christine Kopa", "10-1", "Geschichte", "PW", "Bio"),
    ("Ana Lardt", "11-3", "Bio", "PW", "Englisch"),
    ("Hank Lies", "8-1", "Physik", "Mathe", "Geo"),
    ("Margarete Schneider", "9-2", "Physik", "Chemie", "Bio"),
    ("Lise Fiels", "10-3", "Mathe", "Physik", "Bio"),
    ("Bernardt Fachs", "12-2", "Bio", "Physik", "Englisch"),
    ("Hannoke Karke", "9-2", "Physik", "Physik", "Physik"),
    ("Bilou Zambaar", "10-1", "Englisch", "Physik", "PW"),
    ("Paul Klein", "11-1", "Geschichte", "PW", "Chemie"),
    ("Hilde Affenhartz" , "9-3", "Physik", "Bio", "Chemie")
]

Projekt0 = [
    ("Physik", 3, 8, 12),
    ("Bio", 2, 10, 12),
    ("Chemie", 1, 8, 10),
    ("Geschichte", 1, 9, 11),
    ("PW", 10, 8, 12),
    ("Englisch", 1, 8, 8),
    ("Mathe", 3, 8, 11),
    ("Geo", 4, 9, 10)
]

Projekt1 = [
    ("Physik", 0, 8, 12),
    ("Bio", 0, 10, 12),
    ("Chemie", 0, 8, 10),
    ("Geschichte", 0, 9, 11),
    ("PW", 8, 8, 12),
    ("Englisch", 1, 8, 8),
    ("Mathe", 2, 8, 11),
    ("Geo", 4, 9, 10)
]
'''
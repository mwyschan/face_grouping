import os
import shutil
from PIL import Image
import glob
import face_recognition
import itertools
from os import makedirs
from PIL import Image
import shutil
from os import listdir
from os.path import isfile, join
from datetime import datetime
import numpy as np

def backendlogic(directory):
    folder_name = "C:" + directory
    onlyfiles = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    files=len(onlyfiles)

    faces = []
    files = []

    for i in range(len(onlyfiles)):
        load_image = face_recognition.load_image_file(folder_name+onlyfiles[i])
        number_of_faces = len(face_recognition.face_encodings(load_image))
        for j in range(number_of_faces):
            face_to_compare = face_recognition.face_encodings(load_image)[j]
            files.append(onlyfiles[i])
            faces.append(face_to_compare)

    final_list = []
    loop_counter = 0
    for i in range(len(faces)):
        if i > (len(faces)-2):
            break
        only_once = False
        if str(faces[i]) != str(np.array([" "])):
            final_list.append([files[i]])
            if i != 0:
                loop_counter+=1
            
        for z in range(len(faces)):
            if str(faces[i]) == str(np.array([" "])):
                break
            if z < i:
                continue
            if z > (len(faces)-2):
                break
            if (not (str(faces[z+1]) == str(np.array([" "])))) and (not(str(faces[i]) == str(np.array([" "])))):
                comparison = face_recognition.compare_faces([faces[i]], faces[z+1])
            if str(faces[z+1]) == str(np.array([" "])) or str(faces[i]) == str(np.array([" "])):
                comparison[0] = False
            if comparison[0] == True:
                final_list[loop_counter].append(files[z+1])
                faces[z+1] = (np.array([" "]))
                files[z+1] = (np.array([" "]))
        faces[i] = (np.array([" "]))

    final_list.sort()
    duplicate = [final_list[i] for i in range(len(final_list)) if i == 0 or final_list[i] != final_list[i-1]]

    check = True
    while(check):
        for x in range(len(duplicate)):
            if len(duplicate[x]) == 1:
                duplicate.pop(x)
                break
            check = False
    check = True
    while(check):
        for x in range(len(duplicate)):
            if len(duplicate[x]) == 1:
                duplicate.pop(x)
                break
            check = False   
    print(duplicate)
    for x in range(len(duplicate)):
        duplicate[x] = list(dict.fromkeys(duplicate[x]))

    actual_path = folder_name
    date_time = datetime.now()
    date_time = date_time.strftime("%d%m%Y-%H%M%S")
    for s in range(len(duplicate)):
        
        dir_structure = str(actual_path) + str(s) + "_" + date_time
        makedirs(dir_structure)
    
        for image in duplicate[s]:
            image = folder_name+image
            shutil.copy(image, dir_structure)

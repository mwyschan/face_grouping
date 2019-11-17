import os
import shutil
from PIL import Image
import glob
import face_recognition
import itertools
from os import listdir
from os.path import isfile, join

def backendlogic(directory):
    folder_name = "C:" + directory
    onlyfiles = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    files=len(onlyfiles)
    #differentFolders = [[]*files]

    faces = []
    files = []

    for i in range(len(onlyfiles)):
        load_image = face_recognition.load_image_file(onlyfiles[i])
        number_of_faces = len(face_recognition.face_encodings(load_image))
        for j in range(number_of_faces):
            face_to_compare = face_recognition.face_encodings(load_image)[j]
            files.append(onlyfiles[i])
            faces.append(face_to_compare)

    final_list = []
    loop_counter = 0
    for i in range(len(faces)):
        if i > len(faces)-2:
            break
        only_once = False
        for z in range(len(faces)):
            if faces[i] == [" "]:
                break
            if z < i:
                continue
            if z > len(faces)-2:
                break
            if (not (faces[z+1] == [" "])) and (not(faces[i] == [" "])):
                comparison = face_recognition.compare_faces([faces[i]], faces[z+1])
                print("comparing ", i, " with ", z)
            if faces[z+1] == [" "] or faces[i] == [" "]:
                comparison[0] = False
            if comparison[0] == True:
                if only_once == False:
                    final_list.append([files[i]])
                    only_once = True
                final_list[loop_counter].append(files[z+1])
                faces[z+1] = [" "]
                files[z+1] = [" "]
        if faces[i] != [" "]:
            loop_counter+=1
        faces[i] = [" "]

    final_list.sort()
    duplicate = [final_list[i] for i in range(len(final_list)) if i == 0 or final_list[i] != final_list[i-1]]

    #for x in range(len(final_list)):
    #    if x >= (len(final_list)):
    #        break
    #    if len(final_list[x]) == 1:
    #        final_list.pop(x)
    check = True
    while(check):
        for x in range(len(duplicate)):
            if len(duplicate[x]) == 1:
                duplicate.pop(x)
                break
            check = False
    for x in range(len(duplicate)):
        duplicate[x] = list(dict.fromkeys(duplicate[x]))
    print(duplicate)

    # for i in range(num_of_people= len(duplicate)):
    #     path = "~/Desktop/" + i
    #     try:
    #         os.mkdir(path)
    #     except OSError:
    #         print("Creation of directory %s failed" % path)
    #     else:
    #         print("Successful Successfully created the directory %s" % path)
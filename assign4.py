# ---------------------------------------------------------------
# File: assign4.py
# Role: takes in variables from the data directory and outputs a
# template with those variables filled in.
# ----------------------------------------------------------------

#!/usr/bin/env python3

import sys # get pyton sys library
import os # get python os library
import subprocess # get python subprocess library
import glob # get python glob library

# checking for the correct number/type of arguments
if len(sys.argv) != 5: # if the number of arguments is not four
    print("Usage: " + sys.argv[0] + " <data directory> <template file> <date> <output directory>") # print Usage msg
    sys.exit(1) # exits program

# end of if statement

# output directory
dir_in = sys.argv[1] # input directory
file_template = sys.argv[2] # file template
date = sys.argv[3] # date
dir_out = sys.argv[4] # output directory

if not os.path.isdir(dir_in):
    print("ERROR - argv[1] not a valid directory")
    sys.exit(1)

if not os.path.isdir(dir_out): # if the 4th argument is a directory that doesn't exist
    os.mkdir(dir_out) # makes the directory straight from python

# end of if statement

# .crs file retrieval
crs_files = glob.glob(dir_in + "/*.crs") # gets the .crs files in the data directory

# getting variables an enrollment checking
for f in crs_files: # for every file in the data dir
    # try and except method
    try:
        with open(f, "r") as curr_f: # opening the file for reading and marking it with an 'curr_f' id
            dept_code, dept_name = curr_f.readline().split(" ", 1) # finds the dept_code and dept_name of the .crs file
            dept_code = dept_code.rstrip()
            dept_name = dept_name.rstrip() # strips newline off
            crs_name = curr_f.readline().rstrip() # gets the course name, stripping newline off
            crs_num = f[8:-4] # extracts the course number from the filename
            crs_sched, crs_start, crs_end = curr_f.readline().split(" ", 2) # gets the schedule, start and end date for the course
            crs_sched = crs_sched.rstrip() # strips newline off
            crs_start = crs_start.rstrip() # strips newline off
            crs_end = crs_end.rstrip() # gets the course ending date, stripping the newline off
            crs_hours = curr_f.readline().rstrip() # gets the course's credit hours, stripping off the new line
            crs_students = curr_f.readline().rstrip() # gets the number of students enrolled in the course, stripping the newline off
            if (int(crs_students) > 30): # if the number of students for that course is more than thirty
                with open(file_template, "r") as tFile: # opens the template file for reading and stores it in tFile
                    warnFile = dir_out + "/" + f[4:-4] + ".warn" # stores string of output's filename (".warn")
                    with open(warnFile, "w") as w_F: # opens the warnFile up for writing, storing it in w_F
                        data = tFile.read() # reads the entire template file
                        data = data.replace("[[dept_code]]", dept_code) # replaces all instances of "[[dept_code]]" with the actual dept code
                        data = data.replace("[[dept_name]]", dept_name) # replaces all instances of "[[dept_name]]" with the actual dept name
                        data = data.replace("[[course_name]]", crs_name) # replaces all instances of "[[crs_name]]" with the actual course name
                        data = data.replace("[[course_start]]", crs_start) # replaces all instances of "[[course_start]]" with the actual course starting date
                        data = data.replace("[[course_schedule]]", crs_sched) # replaces all instances of [["course_schedule]]" with the actual schedule for the course
                        data = data.replace("[[course_end]]", crs_end) # repalces all instances of "[[course_end]]" with the actual end date of the course
                        data = data.replace("[[credit_hours]]", crs_hours) # replaces all instances of "[[credit_hours]]" with the actual credit hours
                        data = data.replace("[[num_students]]", crs_students) # replaces all instances of "[[num_students]]" with the actual number of students
                        data = data.replace("[[date]]", date) # replaces all instances of "[[date]]" with the third argument
                        data = data.replace("[[course_num]]", crs_num) # replaces all instances of "[[course_num]]" with the actual course number
                        w_F.write(data) # writes the data into the .warn file
    except FileNotFoundError: # catches any error that can occur if the file is not found
        print("Error: file not found")
        sys.exit(1) # exits program
    except ValueError:
        print("Error: Invalid value")
        sys.exit(1) # exits program
    
# end of for...in block

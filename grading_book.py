"""
This file contains the program for the grading book problem.
Assignment Details : https://bits-pilani.instructure.com/courses/692/assignments/2846

This program has the following components:
1. Definition of hash function and creation of a hash table using primitive data structures
2. Reading of input file and insertion into the hash table
3. Reading prompt file and executing the prompts as:
  a. Creation of Hall of fame list
  b. Creation of List of students to be offered new courses
  c. Creation of the Department Average CGPA list
4. There will be a destroy hash function to be executed after the program ends or on exit
"""
import ast
import fcntl

DEPT_LIST = ["CSE", "MEC", "ECE", "ARC"]
HASHING_STARTER_SEED = 1000000
HASH_TABLE_SIZE = 650000
STARTING_YEAR = 2000
STUDENT_ID_LENGTH = 11
INPUT_PS = "inputPS18.txt"
PROMPTS_PS = "promptsPS18.txt"
OUTPUT_PS = "outputPS18.txt"


class customHash:
    values_list = []

    def __init__(self):
        self.values_list = [None] * HASH_TABLE_SIZE

    def insertStudentRec(self, current_index, key, value):
        """
        Inserts the record in the hash table if the provided key is valid.
        """
        try:
            if current_index >= HASH_TABLE_SIZE:
                raise Exception("The entered key has hash generated more than table size", key, current_index)
            if self.values_list[current_index] is not None:
                # Overwriting Value of the current index as the computed hash is same
                print("There is a value at the current calculated hash. ", self.values_list[current_index])
            self.values_list[current_index] = (key, value)
        except Exception as e:
            print("Error inserting the given key in the hash table.", key, e)

    def _validate_input(self, key):
        """
        Key Validation based on the year and roll number format
        """
        if len(key) == STUDENT_ID_LENGTH:
            _a, _b, _c = int(key[:4]), str(key[4:7]), int(key[7:])
            if _a < 2010 or _a > 2016 or _b not in DEPT_LIST:
                raise Exception("The entered input key has incorrect year", key)
        else:
            raise Exception("The entered input is incorrect", key)

    def get_key(self, key):
        """
        Returns the fetched Value for the key if the key is present.
        If the data for the given key is not present the function returns None

        Includes Input Validation to avoid unnecessary processing.
        """
        try:
            self._validate_input(key)
            current_index = self.get_hash_key(key)
            if current_index >= HASH_TABLE_SIZE:
                raise Exception("The entered key has hash generated more than table size", key)
            if self.values_list[current_index] is not None:
                return self.values_list[current_index][1]
            else:
                return None

        except Exception as e:
            print("Error fetching the entry from the hash table.", key)

    def get_hash_key(self, key):
        """
        This function creates the unique hash id from the student Id given.

        Since the hash function to be generated is for a given student Id,
        we can leverage the student Id attributes for the purpose of creating the hash Id.
        The student Ids in themselves are unique so creating another hash Id is a redundant process
        as we can directly create a map with the student ids as keys.
        Student Id consists of Year, Department and Roll number.

        Based on the above, the hash value can be generated as a concatenation of
        year_offset, branch Id and roll number and to get the correct index we can
        do index correction by subtracting from the first record. (10 0 0000)
        """
        year, dept, roll = int(key[:4]), str(key[4:7]), int(key[7:])
        year_offset = self._get_year_offset(year)
        department_id = self._get_department_id(dept)
        return int(str(year_offset) + str(department_id) + str(roll)) - HASHING_STARTER_SEED

    def _get_year_offset(self, year):
        """
        As the year of study/courses start from 2010,
        we can convert the years into its difference from the starting year (i.e. 2000).

        This function returns the offset of the current year from the Starting year.
        """
        return year - STARTING_YEAR

    def _get_department_id(self, dept):
        """
        We can assign a unique number to each course.
        This function return the index of the current branch from the list of
        pre defined branches.
        """
        return DEPT_LIST.index(dept)

    def getStudentRecords(self):
        """
        Read the INPUT_PS file.
        This function will update the student record from text file to hash table.
        """
        try:
            with open(INPUT_PS, "r") as input_file:
                read_file = input_file.read().splitlines()
                for record in read_file:
                    split_data = record.split("/")
                    # It will generate the hash key and save the value.
                    self._validate_input(split_data[0])
                    current_index = self.get_hash_key(split_data[0])
                    self.insertStudentRec(current_index, split_data[0], split_data[1])
        except Exception as e:
            print("Failed to read input file.", INPUT_PS)

    def readPromptFile(self):
        """
        In prompt file tags are mentioned according to that steps will be method will be
        executed.
        """
        try:
            with open(PROMPTS_PS, "r") as prompt_file:
                read_file = prompt_file.read().splitlines()
                for record in read_file:
                    if record.find("hallOfFame") != -1:
                        self.hallOfFame()
                    else:
                        self.newCourseList(record)
        except Exception as e:
            print("Failed to read prompt file.", PROMPTS_PS)

    def hallOfFame(self):
        """
        This function prints the list of all students who have graduated
        and  topped  their  department  in  their year of graduation
        """
        initial_cse_range = 0.0
        initial_me_range = 0.0
        initial_ec_range = 0.0
        initial_ar_range = 0.0

        with open(OUTPUT_PS, "w") as output_file:
            fcntl.flock(output_file, fcntl.LOCK_EX)
            output_file.truncate(0)
            output_file.write("----------hall of fame ----------")
            output_file.write("\nQualified students:")
            for student_list in self.values_list:
                if student_list:
                    if student_list[0].find(DEPT_LIST[0]) != -1 \
                            and initial_cse_range < ast.literal_eval(student_list[1]):
                        initial_cse_range = ast.literal_eval(student_list[1])
                        cse_fame = student_list[0] + " / " + student_list[1]
                    elif student_list[0].find(DEPT_LIST[1]) != -1 and initial_me_range < ast.literal_eval(
                            student_list[1]):
                        initial_me_range = ast.literal_eval(student_list[1])
                        me_fame = student_list[0] + " / " + student_list[1]
                    elif student_list[0].find(DEPT_LIST[2]) != -1 and initial_ec_range < ast.literal_eval(
                            student_list[1]):
                        initial_ec_range = ast.literal_eval(student_list[1])
                        ec_fame = student_list[0] + " / " + student_list[1]
                    elif student_list[0].find(DEPT_LIST[3]) != -1 and initial_ar_range < ast.literal_eval(
                            student_list[1]):
                        initial_ar_range = ast.literal_eval(student_list[1])
                        ar_fame = student_list[0] + " / " + student_list[1]

            output_file.write("\n" + cse_fame)
            output_file.write("\n" + me_fame)
            output_file.write("\n" + ec_fame)
            output_file.write("\n" + ar_fame)
            output_file.write("\n------------------------------------------")
            fcntl.flock(output_file, fcntl.LOCK_UN)

    def newCourseList(self, record):
        cgpa_range = record.split(":")
        with open(OUTPUT_PS, "a") as output_file:
            output_file.write("\n----------new course candidates ----------")
            output_file.write("\nInput: " + cgpa_range[1] + " to " + cgpa_range[2])
            output_file.write("\nQualified students:")
            for student_list in self.values_list:
                if student_list:
                    if cgpa_range[1] <= student_list[1] <= cgpa_range[2]:
                        output_file.write("\n")
                        output_file.write(student_list[0] + " / " + student_list[1])
            output_file.write("\n------------------------------------------")


# customHash Test
cHash = customHash()
cHash.getStudentRecords()
cHash.readPromptFile()
# cHash.readPromptFile()
# cHash.insert("2010CSE1234", 4.5)
# # cHash.insert("2000CSE1234", 4.5)
# cHash.insert("2014MEC1231", 4.5)
# cHash.insert("2016ARC1234", 4.5)
# # cHash.insert("20CSE1234", 4.5)
# # cHash.insert("20a0CSE1234", 4.5)
print(cHash.get_key("2010CSE1223"))
# # print(cHash.get_key("2000CSE1234"))
# print(cHash.get_key("2014MEC1231"))
# print(cHash.get_key("2016ARC1234"))
# # print(cHash.get_key("20CSE1234"))
# # print(cHash.get_key("2010C3E1234"))

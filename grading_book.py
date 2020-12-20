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
import datetime

current_time = datetime.datetime.now()

DEPT_LIST = ["CSE", "MEC", "ECE", "ARC"]

# This is the year university started as per requirements
STARTING_YEAR = 2010

CURRENT_YEAR = current_time.year
HASH_TABLE_SIZE = int(str(CURRENT_YEAR - STARTING_YEAR - 4) + str(len(DEPT_LIST)-1) + "9999")

STUDENT_ID_LENGTH = 11
INPUT_PS = "inputPS18.txt"
PROMPTS_PS = "promptsPS18.txt"
OUTPUT_PS = "outputPS18.txt"
SECTION_END_SEPARATOR = "\n------------------------------------------"


class customHash:
    values_list = []

    def __init__(self):
        self.values_list = [None] * HASH_TABLE_SIZE

    def insert_student_record(self, current_index, key, value):
        """
        Inserts the record in the hash table if the provided key is valid.

        Complexity : O(1)
        """
        try:
            if current_index >= HASH_TABLE_SIZE:
                raise Exception("The entered key has hash generated more than table size", key, current_index)
            if self.values_list[current_index] is not None:
                # Overwriting Value of the current index as the computed hash is same
                print("There is a value at the current calculated hash. ", self.values_list[current_index])
            self.values_list[current_index] = (key, value)
        except Exception as e:
            print("Error inserting the given key in the hash table.", key, " Error: ", e)

    def _validate_input(self, key):
        """
        Key Validation based on the year and roll number format

        Complexity: O(1)
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

        Complexity : O(1)
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
            print("Error fetching the entry from the hash table.", key, " Error: ", e)

    def get_hash_key(self, key):
        """
        This function creates the unique hash id from the student Id given.

        Since the hash function to be generated is for a given student Id,
        we can leverage the student Id attributes for the purpose of creating the hash Id.
        The student Ids in themselves are unique so creating another hash Id is a redundant process
        as we can directly create a map with the student ids as keys.
        Student Id consists of Year, Department and Roll number.

        Based on the above, the hash value can be generated as a concatenation of
        year_offset, branch Id and roll number.

        Complexity: O(1)
        """
        year, dept, roll = int(key[:4]), str(key[4:7]), int(key[7:])
        year_offset = self._get_year_offset(year)
        department_id = self._get_department_id(dept)
        return int(str(year_offset) + str(department_id) + str(roll))

    def _get_year_offset(self, year):
        """
        As the year of study/courses start from 2010,
        we can convert the years into its difference from the starting year (i.e. 2000).

        This function returns the offset of the current year from the Starting year.

        Complexity: O(1)
        """
        return year - STARTING_YEAR

    def _get_department_id(self, dept):
        """
        We can assign a unique number to each course.
        This function return the index of the current branch from the list of
        pre defined branches.

        Complexity: O(1)
        """
        return DEPT_LIST.index(dept)

    def populate_student_table(self):
        """
        This function reads the INPUT_PS file and
        updates the student record from text file to hash table.

        Complexity: O(n) , where n is the number of records in the file
        """
        try:
            with open(INPUT_PS, "r") as input_file:
                read_file = input_file.read().splitlines()
                for record in read_file:
                    try:
                        student_roll, cgpa = record.split("/")

                        # Validate the student input record
                        self._validate_input(student_roll)

                        # Generate the hash key
                        current_index = self.get_hash_key(student_roll)

                        # Insert valid record
                        self.insert_student_record(current_index, student_roll, cgpa)
                    except Exception as e:
                        print("Failed to read current line in Input file. Error: ", e)
        except IOError as e:
            print("Failed to read input file.", INPUT_PS, " Error: ", e)

    def read_prompts(self):
        """
        In prompt file tags are mentioned according to that steps will be method will be
        executed.

        Complexity: O(n) , as the underlying operations have complexity of O(n) and the given function runs in O(1)
        """
        try:
            with open(PROMPTS_PS, "r") as prompt_file:
                read_file = prompt_file.read().splitlines()
                for record in read_file:
                    if record.find("hallOfFame") != -1:
                        self.hall_of_fame()
                    else:
                        self.new_course_list(record)

                # Department max and average to be calculated irrespective of prompt
                self.department_stats()
        except Exception as e:
            print("Failed to read prompt file.", PROMPTS_PS, " Error: ", e)

    def hall_of_fame(self):
        """
        This function prints the list of all students who have graduated
        and  topped  their  department  in  their year of graduation

        Complexity: O(n) , n being the number of records in the table.
        The other 2 nested for loops iterate over constant sizes and not variable sizes
        so the complexity from them is O(1)
        """
        max_cgpa_per_branch = [[[None, 0] for _ in range(len(DEPT_LIST))]
                               for __ in range(CURRENT_YEAR - STARTING_YEAR - 3)]
        with open(OUTPUT_PS, "w") as output_file:
            output_file.truncate(0)
            output_file.write("---------- hall of fame ----------")
            for student_record in self.values_list:
                if student_record:
                    roll, cgpa = student_record
                    year, dept = int(roll[:4]), roll[4:7]
                    cgpa = float(cgpa)
                    if year <= (CURRENT_YEAR - 4):
                        if max_cgpa_per_branch[year - STARTING_YEAR][self._get_department_id(dept)][1] < cgpa:
                            max_cgpa_per_branch[year - STARTING_YEAR][self._get_department_id(dept)][0] = roll
                            max_cgpa_per_branch[year - STARTING_YEAR][self._get_department_id(dept)][1] = cgpa
            total_toppers = 0
            for i in range(CURRENT_YEAR - STARTING_YEAR - 4):
                for j in range(len(DEPT_LIST)):
                    total_toppers += 1 if max_cgpa_per_branch[i][j][0] else 0

            output_file.write("\nTotal eligible students: " + str(total_toppers))
            output_file.write("\nQualified students:")
            for i in range(CURRENT_YEAR - STARTING_YEAR - 4):
                for j in range(len(DEPT_LIST)):
                    if max_cgpa_per_branch[i][j][0]:
                        output_file.write("\n" + max_cgpa_per_branch[i][j][0] + "/"
                                          + str(max_cgpa_per_branch[i][j][1]))
            output_file.write(SECTION_END_SEPARATOR)

    def new_course_list(self, record):
        """
        This function outputs the eligible students who have graduated in the last 5 years and whose CGPA fall under the
        CGPA range passed as part of the record

        Complexity: O(n) , n being the number of records in the table.
        :param record: containing the starting and ending CGPAs
        """
        cgpa_range = record.split(":")
        NEW_COURSE_YEARS = self._get_eligible_years()
        eligible_students = []
        for student_record in self.values_list:
            if student_record and int(student_record[0][:4]) in NEW_COURSE_YEARS and cgpa_range[1] <= student_record[1] <= cgpa_range[2]:
                eligible_students.append(student_record)
        with open(OUTPUT_PS, "a") as output_file:
            output_file.write("\n---------- new course candidates ----------")
            output_file.write("\nInput: " + cgpa_range[1] + " to " + cgpa_range[2])
            output_file.write("\nTotal eligible students: " + str(len(eligible_students)))
            output_file.write("\nQualified students:")
            for i in range(len(eligible_students)):
                output_file.write("\n" + eligible_students[i][0] + "/" + str(eligible_students[i][1]))
            output_file.write(SECTION_END_SEPARATOR)

    def department_stats(self):
        """
        This function evaluates the max and average CGPA for each branch
        and saves the output to a file.

        Complexity: O(n) , n being the number of records in the table.
        """
        try:
            dept_count = len(DEPT_LIST)
            dept_max = [0] * dept_count
            dept_avg = [0] * dept_count
            dept_students = [0] * dept_count

            with open(OUTPUT_PS, "a") as output_file:
                output_file.write("\n---------- department CGPA ----------")
                # Create the department max and average arrays
                for student_record in self.values_list:
                    if student_record:
                        cur_dept = student_record[0][4:7]
                        cur_cgpa = ast.literal_eval(student_record[1])
                        dept_max[self._get_department_id(cur_dept)] = max(dept_max[self._get_department_id(cur_dept)],
                                                                          cur_cgpa)
                        dept_avg[self._get_department_id(cur_dept)] += cur_cgpa
                        dept_students[self._get_department_id(cur_dept)] += 1
                for i in range(dept_count):
                    output_file.write("\n" + DEPT_LIST[i] + ": ")
                    output_file.write("max: " + str(dept_max[i]) + ", ")
                    output_file.write("avg: " + str(round(dept_avg[i]/dept_students[i], 1)
                                                    if dept_students[i] > 0 else 0))
                output_file.write(SECTION_END_SEPARATOR)
        except Exception as e:
            print("Issue in calculating and saving the department statistics: ", e)

    def destroy_hash(self):
        """
        This function just empties the list of our records.

        Complexity: O(1)
        """
        self.values_list = []

    @staticmethod
    def _get_eligible_years():
        """
        As we need to calculate people graduating in the last 5 years so a person who joined 9 years back would have
        graduated in the last 5th year and the person who joined 4 years back would have graduated last year.
        The students who joined 3 years back are yet t graduate this year. So our upper bound is Current year - 3
        Similarly, the students who joined in current year - 5 - 3 would have graduated 5 years back, so our lower bound
        is current year - 8.

        Complexity: O(1) , as the year count is a constant value

        :return: list of years eligible for new course list operation
        """
        __l = []

        for __i in range(CURRENT_YEAR - 8, CURRENT_YEAR - 3):
            __l.append(__i)
        return __l


# customHash Test
cHash = customHash()
cHash.populate_student_table()
cHash.read_prompts()
cHash.destroy_hash()

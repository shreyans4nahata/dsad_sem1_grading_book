"""
This file contains the program for the grading book problem.
Assigment Details : https://bits-pilani.instructure.com/courses/692/assignments/2846

This progrma has the following components:
1. Definition of hash function and creation of a hash table using primitive data structures
2. Reading of input file and insertion into the hash table
3. Reading prompt file and executing the prompts as:
  a. Creation of Hall of fame list
  b. Creation of Lsit of students to be offered new courses
  c. Creation of the Department Average CGPA list
4. There will be a destroy hash function to be executed after the program ends or on exit
"""

DEPT_LIST = ["CSE", "MEC", "ECE", "ARC"]
HASHING_STRATER_SEED = 1000000
HASH_TABLE_SIZE = 650000
STARTING_YEAR = 2000
STUDENT_ID_LENGTH = 11

class customHash:

    values_list = []

    def __init__(self):
        """
        Initialize the Empty hash table with the default size
        """
        self.values_list = [None]*HASH_TABLE_SIZE

    def insert(self, key: str, value: float):
        """
        Inserts the record in the hash table if the provided key is valid.
        """
        try:
            self._validate_input(key)
            current_index = self.get_hash_key(key)
            if current_index >= HASH_TABLE_SIZE:
                raise Exception("The entered key has hash generated more than table size", key, current_index)
            if self.values_list[current_index] is not None:
                # Overwriting Value of the current index as the computed hash is same
                print("There is a value at the current calculated hash. ", self.values_list[current_index])
            self.values_list[current_index] = (key, value)
        except Exception as e:
            print("Error inserting the given key in the hash table.", key, e)

    def _validate_input(self, key: str):
        """
        Key Validation based on the year and roll number format
        """
        if len(key) == STUDENT_ID_LENGTH:
            _a, _b, _c = int(key[:4]), str(key[4:7]), int(key[7:])
            if _a <2010 or _a > 2016 or _b not in DEPT_LIST:
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

    def get_hash_key(self, key: str):
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
        return int(str(year_offset) + str(department_id) + str(roll)) - HASHING_STRATER_SEED

    def _get_year_offset(self, year: int):
        """
        As the year of study/courses start from 2010,
        we can convert the years into its difference from the starting year (i.e. 2000).

        This function returns the offset of the current year from the Starting year.
        """
        return year - STARTING_YEAR

    def _get_department_id(self, dept: str):
        """
        We can assign a unique number to each course.
        This function return the index of the current branch from the list of
        pre defined branches.
        """
        return DEPT_LIST.index(dept)



"""
# customHash Test
cHash = customHash()
cHash.insert("2010CSE1234", 4.5)
cHash.insert("2000CSE1234", 4.5)
cHash.insert("2014MEC1231", 4.5)
cHash.insert("2016ARC1234", 4.5)
cHash.insert("20CSE1234", 4.5)
cHash.insert("20a0CSE1234", 4.5)
print(cHash.get_key("2010CSE1234"))
print(cHash.get_key("2000CSE1234"))
print(cHash.get_key("2014MEC1231"))
print(cHash.get_key("2016ARC1234"))
print(cHash.get_key("20CSE1234"))
print(cHash.get_key("2010C3E1234"))
"""

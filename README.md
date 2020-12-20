### Introduction
This document details the design for the grade book problem as part of DSAD Assignment 1.
#### Details of Assignment:
Assignment 1 – PS18 - [Grade Book] : https://bits-pilani.instructure.com/courses/692/assignments/2846

### Assumptions and Constraints
1. Let us consider that the CGPA of the student is stored against the student id in the input file.
 a. Every row of the input file should contain the <student id> / <CGPA> separated by a slash (/).
 b. The year of the student ids in the file cannot be greater than 2014 (considering that the file contains the CGPA of only graduating students).
 c. Consider a CGPA scale of 0.0 to 5.0.
2. The students ID has the following format <YYYYAAADDDD> where
 a. YYYY - represents the year in which this student joined the university
 b. AAA - a three letter (alphabet) representing degree program
 c. DDDD - a four digit number representing the students roll number
3. The university offers a 4 year graduate degree program in CSE (Computer Science and Engineering), MEC (Mechanical Engineering), ECE (Electronics and Communication Engineering) and ARC (Architecture).
4. Assume that the academic year is from January to December. There will be no graduations in the middle of the year.

### Requirements
1. Create an input file input.txt with a random list of students per year and their corresponding CGPA (maximum of 5.0 point CGPA).
 a. For students that have graduated, the CGPA would be the overall CGPA and for those who are still to complete the program, you can consider their CGPA to be a temporary CGPA.
 b. In the year 2010 the first batch of 20 students were admitted to the university. Now in the year 2020, 200 students were admitted across all departments. So the starting year for the university is 2010.
2. Design a hash table, which uses student Id as the key to hash elements into the hash table. Generate necessary hash table definitions needed.
3. Design a hash function HashId() which accepts the student-ID as a parameter and returns the hash value. You are only allowed to use basic arithmetic and logic operations in implementing this hash function.

### Solution
#### Approach

We use the lazy approach to generate the hash table. 
This ensures that all our saves are mapped to unique keys and there are no conflicts during insertion.
Given, we have a very short span of the operational years of the college (2010 - 2020) and limited departments (4), our approach can easily be implemented by using more space and lesser time.
 
Since the hash function to be generated is for a given student Id, we can leverage the student Id attributes for the purpose of creating the hash Id. The student Ids in themselves are unique so creating another hash Id is a redundant process as we can directly create a map with the student ids as keys.
Student Id consists of Year, Department and Roll number. We can assign a unique number to each course.

As the year of study/courses start from 2010, we can convert the years into its difference from the starting year (i.e. 2010). So 2020 can be converted into 2020-2010 = 10.

Based on the above, the hash value can be generated as a concatenation of
year_offset, branch Id and roll number.

Therefore, the person who joined CSE in 2010 and was given a roll number of 0001 would have a hash value of :
year_offset = 2010 - 2010
branch_id (CSE) : 0
roll: 0001
key : 000001 -> 1

Similarly, we can map each of these keys. The total max size of our hash table would be 640K.

**Design:**

![IMG](https://drive.google.com/uc?export=view&id=1S_skSnGEucSgqoaUazqjQVR4F7E9NnmH)
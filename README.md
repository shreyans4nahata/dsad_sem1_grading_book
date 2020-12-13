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
2. Design a hash table, which uses student Id as the key to hash elements into the hash table. Generate necessary hash table definitions needed.
3. Design a hash function HashId() which accepts the student-ID as a parameter and returns the hash value. You are only allowed to use basic arithmetic and logic operations in implementing this hash function.

### Solution
#### Approach
Since the hash function to be generated is for a given student Id, we can leverage the student Id attributes for the purpose of creating the hash Id. The student Ids in themselves are unique so creating another hash Id is a redundant process as we can directly create a map with the student ids as keys.
Student Id consists of Year, Department and Roll number. We can assign a unique number to each course.
As the year of study/courses start from 2010, we can convert the years into its difference from the starting year (i.e. 2010). So 2020 can be converted into 2020-2010 = 10.

Based on the above, the hash value can be generated as a concatenation of
year_offset, branch Id and roll number.

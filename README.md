# sectionGrader README
`dprep_grade.py` is a script for evaluating pre-discussion assignment submissions for TAM 251 at the University of Illinois Urbana-Champaign. It works by looking at provided submission files (as `.csv`'s) downloaded from PrairieLearn as well as three files (also as `.csv`'s) providing relevant course information (student roster, course sections, submission info).

It creates a grade book file ready for upload to Compass. 

`generate_grader_data.py` is a script for generating fake submission data, for the purpose of testing `sectionGrader.py` and providing FERPA-compliant examples. It takes a course section `.csv` and then creates a student roster, submission info, and simulated student submissions.

## How to use the grader
1. Download submissions for each assignment from PrairieLearn to a directory containing the `dprep_grade.py` script. These should be `.csv` files which include the headers `Submission Date`, `UID`, and `Correct`.
2. In the same directory, create a course roster file, `roster.csv`. This can be easily accomplished by downloading a record from Compass and removing unnecessary columns. The two columns that must be included are:
    - `Username`, the unique identifier for each student, usually a NetID
    - `Section`, the 3-letter name of the discussion section the student is in (Note: Compass includes other information in the section column, this can be left in as long as the first 3 characters are the section code)
3. In the same directory, create a file `submission_info.csv` with two columns:
    - `Path`, each row containing the path to a submission file intended for grading  
    - `Start`, each row containing the date of the first day of  class the week the assignment is due; format `MM-DD`.
4. In the same directory, create a file `deadlines.csv` with two columns:
    - `section`, the 3-letter name of each section of the course
    - `start_date`, the date of the first time the section meets and the hour it starts, formatted `YYYY-MM-DD-HH`
5. Run the script, `dprep_grade.py` and it will output a file `gradebook.csv`, with each row containing the usernames of each student, their score on each assignment (either `1` or `0`), and their total for all the assignments that have been graded. This file file may be uploaded directly to Compass.

## Example
Coming soon

## How to use the sample data generator
Coming soon 

## Data used by sectionGrader

### Roster file
- Accepted by: `get roster()`
- Opened as `roster.csv`
'Username': str # Student usernames 
'Section': str : # Student sections

### Submission files
- Loaded by: `get_submissions()`
- Accepted by: `grade_submissions`
'Submissions date': str # Date format is `YYYY-MM-DDTHH:MM:SS-05`
'UID': str # formatted as netid@illinois.edu
'Correct': bool # Whether or not submission is correct

### Info file
- Accepted by: `get_info(info_filename)`
'Path': str # Path to submission files
'Start' str # Date format is `MM-DD`

### Deadline file
Currently hypothetical, no such file exists to my knowledge
Doesn't need to exist?
- Accepted by `get_deadlines()`
Should have
'section': str
'start_date': str # Date format is YYYY-MM-DD-HH
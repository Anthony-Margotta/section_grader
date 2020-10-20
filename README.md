# sectionGrader README
`sectionGrader.py` is a script for evaluating pre-discussion assignment submissions for TAM 251 at the University of Illinois Urbana-Champaign. It works by looking at provided submission files (as `.csv`'s) downloaded from PrairieLearn as well as three files (also as `.csv`'s) providing relevant course information (student roster, course sections, submission info).

It creates a grade book file ready for upload to Compass. 

`graderData.py` is a script for generating fake submission data, for the purpose of testing `sectionGrader.py` and providing FERPA-compliant examples. It takes a course section `.csv` and then creates a student roster, submission info, and simulated student submissions.


## Instructions
1. Download submissions for each assignment from PrairieLearn to a directory containing the `dprep_grade.py` script. These should be `.csv` files which include the headers `Submission Date`, `UID`, and `Correct`.
2. In the same directory, create a file `submission_info.csv` with two columns: `Path`, each row containing the path to a submission file intended for grading; and `Start`, each row containing the date


## Documentation Outline
- Overview
- Instructions
- Examples
- Test data generator

## Data used by sectionGrader

### Roster file
- Accepted by: `get roster()`
- Opened as `roster.csv`
'Username': str # Student usernames 
'Section': str : # Student sections

### Submission files
- Loaded by: `get_submissions()`
- Accepted by: `grade_submissions`
'Submssions date': str # Date format is `YYYY-MM-DDTHH:MM:SS-05`
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
'start_date': str # FORMAT TBD
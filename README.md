#
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
Currently hypothetical, no suck file exists to my knowledge
Doesn't need to exist?
- Accepted by `get_deadlines()`
Should have
'section': str
'start_date': str # FORMAT TBD
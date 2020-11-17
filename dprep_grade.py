import csv
import datetime


def get_roster(roster_filename):
    """Loads the course roster from specified csv"""
    with open(roster_filename) as roster_file:
        roster_dict = csv.DictReader(roster_file)
        roster = {}
        for row in roster_dict:
            roster[row['Username']] = row['Section'][-3:]
    return roster


def get_deadlines(date):
    """Returns deadline for given week's assignment based on
    the start time of each section
    """
    with open('deadlines.csv') as deadline_file:
        deadline_dict = csv.DictReader(deadline_file)
        first_week = {}
        for row in deadline_dict:
            section_start = datetime.datetime.strptime(row["start"],
                                                       "%Y-%m-%d-%H")
            first_week[row['section']] = section_start

    date_dif = date_offset(first_week, date)

    deadlines = {}
    for sec, time in first_week.items():
        deadlines[sec] = first_week[sec] + date_dif

    return deadlines


def date_offset(first_week, grade_week):
    """Determines difference between the first week of the
    course and a specified date
    """
    date_dif = grade_week.date() - sorted(first_week.values())[0].date()
    return date_dif


def get_submissions(submission_filename):
    """Loads submission file into a dictionary"""
    with open(submission_filename, encoding='utf8') as sub_file:
        submission_dict = list(csv.DictReader(sub_file))
    return submission_dict


def grade_submissions(submissions, roster, deadlines):
    """Grades submissions (dict) against specified deadlines
    uses roster to match student section to deadlines
    """
    grades = dict([(u, 0) for u in roster.keys()])
    for sub in submissions:
        sub_date = convert_date(sub['Submission date'])
        user = sub['UID'].split('@')[0]
        score = 0
        if user in roster:
            if (sub_date < deadlines[roster[user]] and
                    sub['Correct'].upper() == 'TRUE'):
                score = 1
            if grades[user] != 1:
                grades[user] = score
    return grades


def convert_date(datestring):
    """Converts string from PrairieLearn format YYYY-MM-DDTHH:MM:SS:GMT
    """
    date, time = datestring.split('T')
    year, month, day = list(map(int, date.split('-')))
    hour = int(time[:2])
    sub_date = datetime.datetime(year, month, day, hour)
    return sub_date


def get_info(info_filename):
    """Loads info file into a dictionary"""
    with open(info_filename) as info_file:
        info_dict = csv.DictReader(info_file)
        info = {}
        for row in info_dict:
            info[row['path']] = datetime.datetime.strptime(row['start'],
                                                           '%Y-%m-%d')
    return info


def make_gradebook(roster, grades, sub_info):
    """Creates a summary of student grades in gradebook format
    roster: dict - {username: section}
    grades: list [dict - {username: score}, ...]
    sub_info: dict - {filename: start_date}
    """
    gradebook = []
    for student in roster.keys():
        s = {}
        # fill student file with evaluation grades
        for day, score in zip(sub_info.keys(), grades):
            s[str(day)] = score[student]
        s['total'] = sum(s.values())
        s['username'] = student
        gradebook.append(s)
    return gradebook


def write_gradebook(gradebook, sub_info):
    """Writes gradebook list to a local .csv file"""
    with open('gradebook.csv', 'w', newline='') as gfile:
        fieldnames = ['username']
        [fieldnames.append(f) for f in sub_info.keys()]
        fieldnames.append('total')
        grade_writer = csv.DictWriter(gfile, fieldnames=fieldnames)
        grade_writer.writeheader()
        [grade_writer.writerow(s) for s in gradebook]


if __name__ == "__main__":
    try:
        course_roster = get_roster('roster.csv')
    except FileNotFoundError:
        course_roster = get_roster('examples/roster.csv')
        print('roster.csv retrieved from examples directory!')
    try:
        submission_info = get_info('submission_info.csv')
    except FileNotFoundError:
        submission_info = get_info('examples/submission_info.csv')
        print('submission_info.csv file retrieved from examples directory!')
    student_grades = []
    for path, start in submission_info.items():
        deadline = get_deadlines(start)
        student_submissions = get_submissions(path)
        grade = grade_submissions(student_submissions, course_roster, deadline)
        student_grades.append(grade)
    gb = make_gradebook(course_roster, student_grades, submission_info)
    write_gradebook(gb, submission_info)

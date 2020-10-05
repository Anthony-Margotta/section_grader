import csv
import datetime

def get_roster(roster_filename):
    with open('roster.csv') as roster_file:
        roster_dict = csv.DictReader(roster_file)
        roster = {}
        for row in roster_dict:
            roster[row['Username']] = row['Section'][-3:]
            # roster[row['Score']] = 0
    return roster


def get_deadlines(month, day):
    with open('deadlines.csv') as deadline_file:
        deadline_dict = csv.DictReader(deadline_file)
        first_week = {}
        for row in deadline_dict:
            start = datetime.datetime.strptime(row["start"],"%Y-%m-%d-%H")
            first_week[row['section']] = start
    # first_week = {'AD1': datetime.datetime(year=2019, month=1, day=14, hour=12),
    #               'AD2': datetime.datetime(year=2019, month=1, day=14, hour=13),
    #               'AD3': datetime.datetime(year=2019, month=1, day=14, hour=14),
    #               'AD4': datetime.datetime(year=2019, month=1, day=14, hour=15),
    #               'AD5': datetime.datetime(year=2019, month=1, day=14, hour=16),
    #               'AD7': datetime.datetime(year=2019, month=1, day=15, hour=14),
    #               'AD8': datetime.datetime(year=2019, month=1, day=15, hour=15),
    #               'AD9': datetime.datetime(year=2019, month=1, day=15, hour=16),
    #               'ADC': datetime.datetime(year=2019, month=1, day=17, hour=9),
    #               'ADD': datetime.datetime(year=2019, month=1, day=17, hour=10),
    #               'ADE': datetime.datetime(year=2019, month=1, day=17, hour=11)}

    date_dif = date_offset(first_week, month, day)

    deadlines = {}
    for sec, time in first_week.items():
        deadlines[sec] = first_week[sec] + date_dif

    return deadlines


def date_offset(first_week, month, day):
    grade_week = datetime.date(year=2019, month=month, day=day)
    date_dif = grade_week - first_week['AD1'].date()
    return date_dif



def get_submissions(submission_filename):
    with open(submission_filename, encoding='utf8') as sub_file:
        submission_dict = list(csv.DictReader(sub_file))
    return submission_dict


def grade_submissions(submissions, roster, deadlines):
    grades = dict([(u, 0) for u in roster.keys()])
    for sub in submissions:
        sub_date = convert_date(sub['Submission date'])
        user = sub['UID'].split('@')[0]
        score = 0
        if user in roster:
            if sub_date < deadlines[roster[user]] and sub['Correct'] == 'TRUE':
                score = 1
            if grades[user] != 1:
                grades[user] = score
            # if sub_date < deadlines[roster[user]] and sub['Score'] is not '':
            #     score = float(sub['Score'])
            # if grades[user] < score:
            #     grades[user] = score
    return grades

def convert_date(datestring):
    date,time = datestring.split('T')
    year, month, day = list(map(int,date.split('-')))
    hour = int(time[:2])
    sub_date = datetime.datetime(year, month, day, hour)
    return sub_date


def get_info(info_filename):
    with open(info_filename) as info_file:
        info_dict = csv.DictReader(info_file)
        info = {}
        for row in info_dict:
            info[row['path']] = list(map(int,row['start'].split('-')))
    return info


def make_gradebook(roster, grades, sub_info):
    '''
    roster: dict - {username: section}
    grades: list [dict - {username: score}, ...]
    sub_info: dict - {filename: start_date}
    '''
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
    with open('gradebook.csv', 'w', newline='') as gfile:
        fieldnames = ['username']
        [fieldnames.append(f) for f in sub_info.keys()]
        fieldnames.append('total')
        grade_writer = csv.DictWriter(gfile, fieldnames=fieldnames)
        grade_writer.writeheader()
        [grade_writer.writerow(s) for s in gradebook]

if __name__ == "__main__":
    roster = get_roster('roster.csv')
    sub_info =get_info('submission_info.csv')
    grades = []

    for path, start in sub_info.items():
        deadline = get_deadlines(start[0], start[1])
        submissions = get_submissions(path)
        grade = grade_submissions(submissions, roster, deadline)
        grades.append(grade)

    gb = make_gradebook(roster, grades, sub_info)
    write_gradebook(gb, sub_info)

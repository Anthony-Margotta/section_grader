import random
import datetime
import csv


class Student:
    """A class to represent students in the course

    Attributes
    ----------
    name : name of the student
    section : the discussion section the student is in
    motivation : motivation score of the student, affects simulation
    successes : list tracking on which assignments students scored 'correct'
    section_start : start time of the student's discussion section

    Methods
    -------
    attempt(week, gradebook):
        simulates the student's attempt on a week's assignment and records
        their score in the gradebook
    asdict():
        return the student name and section in a dict object
    """

    def __init__(self, name, section, motivation, length):
        self.name = name
        self.section = section  # a dict
        self.motivation = motivation  # an int
        self.successes = [0] * length
        self.section_start = datetime.datetime.strptime(section['start'],
                                                        "%Y-%m-%d-%H")

    def attempt(self, week, gradebook):
        """simulates the student's attempt on a week's assignment and
        records their score in the gradebook

        Note: This is currently designed to repeat until the student suceedes
        the assignment at least once, even if that success is late. This was
        determined to be a good balance of realism and simplicity, but could
        be improved.
        """
        due = self.section_start + datetime.timedelta(weeks=week)
        # randomly generated "effort" determined window for assignment attempt
        effort = random.randrange(10) + self.motivation
        if effort > 10:  # early
            # due - 3 days +- 12 hour range
            attempt_date = pick_time(due, -72, 12)
        elif effort > 5:  # on time
            # due date - 12 hour range
            attempt_date = pick_time(due, -12, 12)
        elif effort > 2:  # late
            # due date + 6 hour range
            attempt_date = pick_time(due, -3, 3)
        else:  # very late
            # due date + 6days +- 24 hour range
            attempt_date = pick_time(due, 72, 72)

        # Determine if an attempt is made.
        # An attempt is always made if the student has no successes this week.
        # An attempt is occasionally made if the student already has succeeded.
        if random.random() < (1 - 0.9 * self.successes[week]):
            # Check if attempt is right (hardcoded 70% chance each time)
            if random.random() < 0.7:
                self.successes[week] = 1  # log success in attribute
                correct = True
            else:
                correct = False
            # Appends attempt info to the Course gradebook
            gradebook.append(
                (self.name,
                 self.section.get("label"),
                 attempt_date.strftime("%Y-%m-%dT%H"),  # Match PrairieLearn
                 correct,
                 week + 1)  # Adjust for zero-based indexing
            )
            # Always makes another attempt, will eventually terminate once
            # success has been logged. P(Repeat|Success) = 0.1)
            self.attempt(week, gradebook)

    def asdict(self):
        """Return the student name and section as a dict"""
        return {'Username': self.name, 'Section': self.section['section']}


class Course:
    """A class to represent a course which contains students and a schedule

    Attributes
    ----------
    length : the length of the course, in weeks
    students : a list containing all the Students in the Course
    submissions : a list of all the submissions that have been simulated

    Methods
    -------
    run():
        Simulates a semester of the course, generating student submissions
    write_files():
        Creates files for the course, including student submission files, and
        a submission_info file with the paths and deadlines for each
        assignment's submissions
    """

    def __init__(self, length, sections='deadlines.csv'):
        self.length = length
        self.students = []
        self.submissions = None

        # Get sections dict either from local .csv or passed dict
        if type(sections) is str:
            with open(sections) as deadline_file:
                self.sections = list(csv.DictReader(deadline_file))
        else:
            self.sections = sections

        self.start = self.get_start()

        # Create Students in each section
        for section in self.sections:
            for i in range(int(section.get("size"))):
                name = str(random.randrange(1000000, 9999999))
                motivation = random.randint(1, 3)  # Used to simulate attempts
                self.students.append(
                    Student(name, section, motivation, self.length)
                )

    def run(self):
        """Simulates running a semester of the course"""
        submissions = []
        for student in self.students:
            for week in range(0, self.length):  # for each week of the Course
                student.attempt(week=week, gradebook=submissions)

        self.submissions = submissions

    def write_files(self):
        """Creates files for the course necessary to run the grader"""
        with open('roster.csv', 'w', newline='') as rosterfile:
            writer = csv.DictWriter(rosterfile, ['Username', 'Section'])
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.asdict())

        # Create submission files
        fieldnames = ['UID', 'Section', 'Submission date', 'Correct', 'week']
        file_names = []
        for w in range(1, self.length + 1):
            file_names.append('submissions_week%i' % w)
            with open(file_names[w - 1], 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)
                # write file for each week
                for r in range(len(self.submissions)):
                    # check if row was for week w (current loop)
                    if self.submissions[r][-1] == w:
                        writer.writerow(self.submissions[r])

        # Create submission info file
        with open('submission_info.csv', 'w', newline='') as infofile:
            writer = csv.writer(infofile)
            writer.writerow(['path', 'start'])
            for i, path in enumerate(file_names):
                start = self.start + datetime.timedelta(weeks=i)
                writer.writerow([path, start.strftime('%m-%d')])

    def get_start(self):
        starts = []
        for section in self.sections:
            # noinspection PyTypeChecker
            starts.append(
                datetime.datetime.strptime(section['start'], "%Y-%m-%d-%H"))

        starts.sort()
        return starts[0]


def pick_time(target, hours_offset, hours_spread):
    """Used by Student.attempt() to determine when the attempt is made"""
    dhours = hours_offset + random.uniform(-hours_spread, hours_spread)
    delta = datetime.timedelta(hours=dhours)
    return target + delta


if __name__ == "__main__":
    random.seed(0)

    test_course = Course(length=3)
    test_course.run()

    print('There were ' + str(
        len(test_course.submissions)) + ' submissions generated')

    test_course.write_files()

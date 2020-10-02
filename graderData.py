import random
import datetime
import csv


class Student:
    """Student class"""
    
    def __init__(self, name, section, motivation, length):
        self.name = name
        self.section = section
        self.motivation = motivation
        self.successes = [0] * length
        self.section_start = datetime.datetime.strptime(section["start"],"%Y-%m-%d-%H")
    
    def attempt(self, week, gradebook):
        due = self.section_start + datetime.timedelta(weeks=week)
        effort = random.randrange(10) + self.motivation
        if (effort > 10):
            # due date - 3 days +- 12hourrange
            attempt_date = pick_time(due, -72, 12)
        elif (effort > 5):
            # due date - 12hourrange
            attempt_date = pick_time(due, -12, 12)
        elif (effort > 2):
            # due date + 6hourrange
            attempt_date = pick_time(due, -3, 3)
        else:
            # due date + 6days +- 24 hourrange
            attempt_date = pick_time(due, 72, 72)
        
        # make attempt if there's not previous sucesses,
        # maybe make attempt if there are
        if (random.random()<(1 - 0.9*self.successes[week])):
            # check if attempt is right (70% chance each time)
            if (random.random() < 0.7):
                self.successes[week] = 1
                correct = True
            else:
                correct = False
                
            gradebook.append(
                (self.name,
                 self.section.get("label"),
                 attempt_date.strftime("%Y-%m-%d-%H"),
                 correct,
                 week+1)
            )
            
            self.attempt(week, gradebook)
    def asdict(self):
        return {'Username':self.name, 'Section': self.section['section']}


class Course:
    """Course class"""

    def __init__(self, length, sections = 'deadlines.csv'):
        self.length = length
        self.students = []
        self.submissions = None
        
        if type(sections) == str:
            with open('deadlines.csv') as deadline_file:
                self.sections = list(csv.DictReader(deadline_file))
        else:
            self.sections=sections

        self.start = self.get_start()            

        # Create students
        for section in self.sections:
            for i in range(int(section.get("size"))):
                name = str(random.randrange(1000000,9999999))
                motivation = random.randint(1,3)
                self.students.append(
                    Student(name, section, motivation, self.length)
                )

    def run(self):
        "simulates running a semester of the course"
        submissions = []
        for student in self.students:
            for week in range(0,self.length):
                student.attempt(week = week, gradebook = submissions)

        self.submissions = submissions
    
    def write_files(self):
        # Create roster file
        with open('roster.csv', 'w', newline='') as rosterfile:
            writer = csv.DictWriter(rosterfile, ['Username', 'Section'])
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.asdict())
            
        # Create submission files
        fieldnames = ['UID', 'Section','Submission date', 'Correct', 'week']
        file_names = []
        for w in range(1,self.length+1):
            file_names.append('submissions_week%i' % w)
            with open(file_names[w-1], 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)
                # write file for each week
                for r in range(len(self.submissions)):
                    # check if row was for week w (current loop)
                    if self.submissions[r][-1] == w:
                        writer.writerow(self.submissions[r])
        
        # Create submssion info file
        with open('submission_info.csv', 'w', newline='') as infofile:
            writer = csv.writer(infofile)
            writer.writerow(['path'])
            for path in file_names:
                writer.writerow([path])

    def get_start(self):
        starts = []
        for section in self.sections:
            starts.append(
                datetime.datetime.strptime(section["start"],"%Y-%m-%d-%H"))
        
        starts.sort()
        return starts[0]

def pick_time(target, hours_offset, hours_spread):
        dhours = hours_offset + random.uniform(-hours_spread,hours_spread)
        delta = datetime.timedelta(hours=dhours)
        return target + delta


test_course = Course(length=3)

random.seed(0)
test_course.run()


print('There were '+str(len(test_course.submissions))+' submissions generated')


# test_course.write_files()
print(test_course.start)


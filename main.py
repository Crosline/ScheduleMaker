import random as rnd
import prettytable as pt
import xlrd

class Data:
    # NOW WE READ FROM datasheet.xlsl file
    # ROOMS = \
    #     [["R1", 25],
    #      ["R2", 45],
    #      ["R3", 35]]
    #
    # MEETING_TIMES = \
    #     [["MT1", "MWF 09:00 - 10:00"],
    #      ["MT2", "MWF 10:00 - 11:00"],
    #      ["MT3", "TTH 09:00 - 10:30"],
    #      ["MT4", "TTH 10:30 - 12:00"]]
    #
    # INSTRUCTORS = \
    #     [["I1", "YGT YVZ", "MATH, PHYS"],
    #      ["I2", "EIN AIS", "MATH, ELE"],
    #      ["I3", "STEVE JOBS", "MATH"],
    #      ["I4", "EKIN DENIZ", "PHYS, BBM"]]
    #
    # COURSES = \
    #     [["C1", "MATH", "CS", 25],
    #      ["C2", "MATH", "EE", 35],
    #      ["C3", "PHYS", "CS", 20],
    #      ["C4", "PHYS", "EE", 30],
    #      ["C5", "ELE", "EE", 40],
    #      ["C6", "ELE", "EE", 25],
    #      ["C7", "BBM", "CS", 20]]

    def __init__(self):
        self._rooms = []
        self._meeting_times = []
        self._instructors = []

        datas = self.read_data("datasheet")

        self.ROOMS = datas[0]
        self.MEETING_TIMES = datas[1]
        self.INSTRUCTORS = datas[2]
        self.COURSES = datas[3]

        for i in range(len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(len(self.MEETING_TIMES)):
            self._meeting_times.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(len(self.INSTRUCTORS)):
            for j in self.INSTRUCTORS[i][2].split(","):
                self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1], j))

        course = []
        for i in range(len(self.COURSES)):
            instruct = []
            for j in range(len(self._instructors)):
                if self.COURSES[i][1] in self._instructors[j].get_lessons():
                    instruct.append(self._instructors[j])
            course.append(Course(self.COURSES[i][0], self.COURSES[i][1], instruct, self.COURSES[i][3]))

        self._courses = course

        department = []
        temp_course = []

        for i in range(len(self.COURSES)):
            if self.COURSES[i][2] not in temp_course:
                temp_course.append(self.COURSES[i][2])
                crs = []
                for j in range(len(self.COURSES)):
                    if self.COURSES[j][2] == self.COURSES[i][2]:
                        crs.append(course[i])

                department.append(Department(self.COURSES[i][2], crs))

        self._departments = department
        self._number_of_classes = len(self.COURSES)

    @staticmethod
    def read_data(excel):
        wb = xlrd.open_workbook(excel + ".xlsx")
        output = []
        z = wb.nsheets
        for n in range(z):
            sheet = wb.sheet_by_index(n)
            rows = sheet.nrows
            cols = sheet.ncols
            data_of_sheet = []
            for i in range(rows):
                data_of_row = []
                for j in range(cols):
                    data_of_row.append(sheet.cell_value(i, j))
                data_of_sheet.append(data_of_row)
            output.append(data_of_sheet)
        return output

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_departments(self):
        return self._departments

    def get_meeting_times(self):
        return self._meeting_times

    def get_number_of_classes(self):
        return self._number_of_classes

    @staticmethod
    def get_data(excel_file = "datasheet.xlsl"):
        # PLACE FOR EINAIS TO COMPLETE
        return 0


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._number_of_conflicts = 0
        self._fitness = -1
        self._class_number = 0
        self._is_fitness_changed = True

    def get_number_of_conflicts(self):
        return self._number_of_conflicts

    def get_fitness(self):
        if self._is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False

        return self._fitness

    def get_classes(self):
        self._is_fitness_changed = True
        return self._classes

    def calculate_fitness(self):
        self._number_of_conflicts = 0
        classes = self.get_classes()

        for i in range(0, len(classes)):
            if classes[i].get_room().get_capacity() < classes[i].get_course().get_max_students():
                self._number_of_conflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if classes[i].get_meeting_time() == classes[j].get_meeting_time() and \
                            classes[i].get_id() != classes[j].get_id():
                        if classes[i].get_room() == classes[j].get_instructor():
                            self._number_of_conflicts += 1
                        if classes[i].get_instructor() == classes[j].get_instructor():
                            self._number_of_conflicts += 1

        return 1 / (1.0 * self._number_of_conflicts + 1)

    def initialize(self):
        departments = self._data.get_departments()

        for i in range(0, len(departments)):
            courses = departments[i].get_courses()
            for j in range(0, len(courses)):
                new_class = Class(self._class_number, departments[i], courses[j])
                self._class_number += 1
                new_class.set_meeting_time(data.get_meeting_times()[rnd.randrange(0, len(data.get_meeting_times()))])
                new_class.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                new_class.set_instructor(
                    courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(new_class)

        return self

    def __str__(self):
        value = [str(self._classes[i]) for i in range(len(self._classes))]

        return ", ".join(value)


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []

        for i in range(size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    ''' '''


class Course:
    def __init__(self, number, name, instructors, max_students):
        self._number = number
        self._name = name
        self._max_students = max_students
        self._instructors = instructors

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_max_students(self):
        return self._max_students

    def get_instructors(self):
        return self._instructors

    def __str__(self):
        return self._name


class Instructor:
    def __init__(self, id_number, name, lessons):
        self._id = id_number
        self._name = name
        self._lessons = lessons

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_lessons(self):
        return self._lessons

    def __str__(self):
        return self._name


class Room:
    def __init__(self, number, capacity):
        self._number = number
        self._capacity = capacity

    def get_number(self):
        return self._number

    def get_capacity(self):
        return self._capacity


class MeetingTime:
    def __init__(self, id_number, time):
        self._id = id_number
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._id


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self):
        return self._name

    def get_courses(self):
        return self._courses


class Class:
    def __init__(self, id_number, dept, course):
        self._id = id_number
        self._dept = dept
        self._course = course

        self._instructor = None
        self._meeting_time = None
        self._room = None

    def get_id(self):
        return self._id

    def get_dept(self):
        return self._dept

    def get_course(self):
        return self._course

    def get_instructor(self):
        return self._instructor

    def get_meeting_time(self):
        return self._meeting_time

    def get_room(self):
        return self._room

    def set_instructor(self, instructor):
        self._instructor = instructor

    def set_meeting_time(self, meeting_time):
        self._meeting_time = meeting_time

    def set_room(self, room):
        self._room = room

    def __str__(self):
        return str(self._dept.get_name()) + ", " + str(self._course.get_number()) + ", " + \
               str(self._room.get_number()) + ", " + str(self._instructor.get_id()) + ", " + str(
            self._meeting_time.get_id())


class DisplayMgr:
    def print_available_data(self):
        print("--------------------All Data--------------------")
        self.print_department()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    def print_department(self):
        lst = data.get_departments()
        table = pt.PrettyTable(["Department", "Courses"])
        for i in range(len(lst)):

            courses = []
            temp = lst.__getitem__(i).get_courses()
            for j in temp:
                courses.append(j.get_name() + " (" + j.get_number() + ")")

            table.add_row([lst.__getitem__(i).get_name(), courses])

        print(table)

    def print_course(self):
        lst = data.get_courses()
        table = pt.PrettyTable(["Course Number", "Name", "Instructors", "Max Students"])
        for i in range(len(lst)):
            instructors = []
            temp = lst.__getitem__(i).get_instructors()
            for j in temp:
                instructors.append(j.get_name() + " (" + j.get_id() + ")")
            table.add_row([lst.__getitem__(i).get_number(), lst.__getitem__(i).get_name(), instructors, lst.__getitem__(i).get_max_students()])
        print(table)

    def print_meeting_times(self):
        lst = data.get_meeting_times()
        table = pt.PrettyTable(["Meeting ID", "Time"])
        for i in range(len(lst)):
            table.add_row([lst.__getitem__(i).get_id(), lst.__getitem__(i).get_time()])

        print(table)

    def print_instructor(self):
        lst = data.get_instructors()
        table = pt.PrettyTable(["Instructor ID", "Name", "Lessons"])
        for i in range(len(lst)):
            table.add_row([lst.__getitem__(i).get_id(), lst.__getitem__(i).get_name(), lst.__getitem__(i).get_lessons()])
        print(table)

    def print_room(self):
        lst = data.get_rooms()
        table = pt.PrettyTable(["Room Number", "Capacity"])
        for i in range(len(lst)):
            table.add_row([lst.__getitem__(i).get_number(), lst.__getitem__(i).get_capacity()])

        print(table)


data = Data()

displayMgr = DisplayMgr()

displayMgr.print_available_data()
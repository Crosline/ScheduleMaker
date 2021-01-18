import random as rnd
import xlrd

POPULATION_SIZE = 9
NUMBER_OF_ELITE_SCHEDULES = 2
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Data:
    # NOW WE READ FROM datasheet.xls file
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
    #     [["I1", "YGT YVZ", "MATH, PHYS", "MT1, MT2, MT3, MT4, MT5, MT6, MT7, MT8, MT9, MT10"],
    #      ["I2", "EIN AIS", "MATH, ELE", "MT1, MT2, MT3, MT4, MT5, MT6, MT7, MT8, MT9, MT10"],
    #      ["I3", "STEVE JOBS", "MATH", "MT11, MT12, MT13, MT14, MT15, MT16, MT17, MT18, MT19, MT20"],
    #      ["I4", "EKIN DENIZ", "PHYS, BBM", "MT11, MT12, MT13, MT14, MT15, MT16, MT17, MT18, MT19, MT20"]]
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

        self.ROOMS, self.MEETING_TIMES, self.INSTRUCTORS, self.COURSES = self.read_data("datasheet")

        # self.ROOMS = datas[0]
        # self.MEETING_TIMES = datas[1]
        # self.INSTRUCTORS = datas[2]
        # self.COURSES = datas[3]

        for i in range(len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(len(self.MEETING_TIMES)):
            self._meeting_times.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(len(self.INSTRUCTORS)):
            for j in self.INSTRUCTORS[i][2].split(","):
                for k in self.INSTRUCTORS[i][3].split(","):
                    self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1], j, k))

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
                        crs.append(course[j])
                department.append(Department(self.COURSES[i][2], crs))

        self._departments = department
        self._number_of_classes = len(self.COURSES)

    @staticmethod
    def read_data(excel):
        wb = xlrd.open_workbook(excel + ".xls")
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

        for i in range(len(classes)):
            if classes[i].get_room().get_capacity() < classes[i].get_course().get_max_students():
                self._number_of_conflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if classes[i].get_meeting_time() == classes[j].get_meeting_time() and \
                            classes[i].get_id() != classes[j].get_id():
                        if classes[i].get_dept() == classes[j].get_dept():
                            self._number_of_conflicts += 1
                        if classes[i].get_room() == classes[j].get_room():
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
    def evolve(self, pop):
        return self._mutate_population(self._crossover_population(pop))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMBER_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])

        for i in range(NUMBER_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            s1 = self._select_tournament_population(pop).get_schedules()[0]
            s2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(s1, s2))

        return crossover_pop

    def _mutate_population(self, pop):
        for i in range(NUMBER_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(pop.get_schedules()[i])
        return pop

    @staticmethod
    def _crossover_schedule(schedule1, schedule2):
        c_schedule = Schedule().initialize()
        for i in range(len(c_schedule.get_classes())):
            if rnd.random() > 0.5:
                c_schedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                c_schedule.get_classes()[i] = schedule2.get_classes()[i]
        return c_schedule

    @staticmethod
    def _mutate_schedule(s1):
        s2 = Schedule().initialize()

        for i in range(len(s1.get_classes())):
            if MUTATION_RATE > rnd.random():
                s1.get_classes()[i] = s2.get_classes()[i]

        return s2

    @staticmethod
    def _select_tournament_population(pop):
        t_pop = Population(0)
        for i in range(TOURNAMENT_SELECTION_SIZE):
            t_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
        t_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        return t_pop


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
    def __init__(self, id_number, name, lessons, meeting_times):
        self._id = id_number
        self._name = name
        self._lessons = lessons
        self._meeting_times = meeting_times

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_meeting_times(self):
        return self._meeting_times

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


# "MT1 MT1 id"
# "W 09:00 - 10:00"
class MeetingTime:
    def __init__(self, id_number, time):
        self._id = id_number
        self._time = time

    # def __eq__(self, other):
    #     if self._id == other.get_id():
    #         return True
    #     return False

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time


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


class Displayer:
    @staticmethod
    def print_available_data(self):
        print("--------------------All Data--------------------")
        self.print_department()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    @staticmethod
    def print_department():
        lst = data.get_departments()
        table = [["Department", "Courses"]]
        for i in range(len(lst)):
            courses = []
            temp = lst.__getitem__(i).get_courses()
            for j in temp:
                courses.append(j.get_name() + " (" + j.get_number() + ")")
            table.append([lst.__getitem__(i).get_name(), courses])

        print(table)

    @staticmethod
    def print_course():
        lst = data.get_courses()
        table = [["Course Number", "Name", "Instructors", "Max Students"]]
        for i in range(len(lst)):
            instructors = []
            temp = lst.__getitem__(i).get_instructors()
            for j in temp:
                instructors.append(j.get_name() + " (" + j.get_id() + ")")
            table.append([lst.__getitem__(i).get_number(), lst.__getitem__(i).get_name(), instructors,
                          lst.__getitem__(i).get_max_students()])
        print(table)

    @staticmethod
    def print_meeting_times():
        lst = data.get_meeting_times()
        table = [["Meeting ID", "Time"]]
        for i in range(len(lst)):
            table.append([lst.__getitem__(i).get_id(), lst.__getitem__(i).get_time()])

        print(table)

    @staticmethod
    def print_instructor():
        lst = data.get_instructors()
        table = [["Instructor ID", "Name", "Lessons"]]
        for i in range(len(lst)):
            table.append(
                [lst.__getitem__(i).get_id(), lst.__getitem__(i).get_name(), lst.__getitem__(i).get_lessons()])
        print(table)

    @staticmethod
    def print_room():
        lst = data.get_rooms()
        table = [["Room Number", "Capacity"]]
        for i in range(len(lst)):
            table.append([lst.__getitem__(i).get_number(), lst.__getitem__(i).get_capacity()])

        print(table)

    def print_generation(self, schedule, is_dept=True):
        table = [["Schedule #", "Fitness", "# of Conflicts", "Classes [Dept, Class, Room, Instructor, Meeting Time]"]]

        for i in range(len(schedule)):
            x = schedule.__getitem__(i)
            y = []
            for j in x.get_classes():
                y.append([j.get_dept().get_name(), j.get_course().get_name(), j.get_room().get_number(),
                          j.get_instructor().get_id(), j.get_meeting_time().get_time()])

            if is_dept:
                y.sort(key=lambda z: (z[0], self.gs(z[4])))
            else:
                y.sort(key=lambda z: (z[3], self.gs(z[4])))

            # y.sort(key=lambda x: (x[0][0], self.gs(x[0][4])))

            table.append([i, x.get_fitness(), x.get_number_of_conflicts(), y])

        for i in table:
            print(i)

    @staticmethod
    def get_first(elem):
        return elem[0][0]

    @staticmethod
    def gs(obj1):
        days = ["M", "T", "W", "Th", "F", "St", "Sn"]
        temp1 = obj1.split(" ")
        index = 0
        for i in range(len(days)):
            if temp1[0] == days[i]:
                index = i + 1
        # "009:00 - 10:00"
        # "1
        return_string = str(index)
        for i in range(1, len(temp1)):
            return_string += temp1[i]
        return return_string

    @staticmethod
    def ge(obj1, other):
        days = ["M", "T", "W", "Th", "F", "St", "Sn"]
        index = [0, 0]
        temp1 = obj1.split(" ")[0]
        temp2 = other.split(" ")[0]
        for i in range(len(days)):
            if temp1 == days[i]:
                index[0] = i + 1
            if temp2 == days[i]:
                index[1] = i + 1

        if index[0] > index[1]:
            return True
        elif index[0] == index[1]:
            if obj1[2:] >= other[2:]:
                return True

        return False


data = Data()

display = Displayer()
display.print_available_data()

generation_number = 0
print("\nGeneration #" + str(generation_number))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

genetic_algorithm = GeneticAlgorithm()

schedules = population.get_schedules()

display.print_generation(schedules)
# while generation_number < 15:
while population.get_schedules()[8].get_fitness() != 1 and generation_number < 2000:
    generation_number += 1
    print("\n-------------------------------------------------------------------")
    print("Generation #" + str(generation_number))
    population = genetic_algorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

    display.print_generation(population.get_schedules())
    display.print_generation(population.get_schedules(), False)
    print("-------------------------------------------------------------------\n")

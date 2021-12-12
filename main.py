import enum
import os
import sys


def put_max(instructors, courses, instructor_count, myset):
    # print(set(courses))
    list_courses = list(set(courses))  # will be removing the course when it got visited
    if len(list_courses) == 0:
        return myset
    max_size = max([len(value) for value in instructor_count])
    sizes = [len(value) for value in instructor_count]  # weight of courses on instructor
    # print("Max_size_index",sizes.index(max_size))
    # getting the real index of instructor
    instructor_index = instructors[sizes.index(max_size)]
    # print("instructors index: ",instructor_index)
    teach_courses = instructor_count[sizes.index(max_size)]
    for item in instructor_count[sizes.index(max_size)]:
        if item in list_courses:
            # visited course for that instructor
            list_courses.remove(item)
        else:
            # already visited
            pass
    # courses = [courses.remove(item) for item in instructor_count[sizes.index(max_size)] if item in courses]
    instructor_count[sizes.index(max_size)] = []
    # print("Instructor Count: ", instructor_count)
    # print("Courses after: ",mylist_courses)
    # print(instructor_count)
    # instructor_count.remove(sizes.index(max_size))
    myset.append((instructor_index, teach_courses))
    return put_max(instructors, list_courses, instructor_count, myset)


class InstructorMap:
    def __init__(self, input_file):
        self.nodes = []
        # self.vertices = [] # to capture
        self.courses = []  # to capture the courses
        self.adjacentList = []  # created for adjacent matrix will be initialized when creating connection
        # self.adjacentList = [[0 for j in range(20)] for i in range(20)]
        self.instructors = []
        self.input_file = input_file

        print("Initializing with file: " + self.input_file)
        self.read_file_and_create_node()
        # print(instructor_map.nodes)
        self.create_connections()

    # return indices
    # creating nodes and returning indices of that node for better understanding
    # analysing and creating nodes
    def get_node_index(self, node):
        # print("looking for: ", node)
        try:
            return self.nodes.index(node)
        except IndexError as e:
            return e
            # print("no index found for that node")
        finally:
            pass
            # print("no index found for that node, please check the course code")

    def check_and_add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
        return self.get_node_index(node)

    # analysing and calculating the nodes ,subjects,instructors
    def read_file_and_create_node(self):

        with open(file=self.input_file) as my_file:
            self.nodes.append(NO_SUBJECT)
            lines = my_file.readlines()
            for line in lines:
                # print(line)
                data_array = line.split("/")
                name = data_array[0].strip()
                subjects = data_array[1:]
                # print(name, subjects)
                name_index = self.check_and_add_node(node=name.strip())
                # print(self.nodes)
                self.instructors.append(name_index)
                for subject in subjects:
                    # print("adding subject: ", subject)
                    subject_index = self.check_and_add_node(node=subject.strip())  # it will add the node if not present
                    # print(subject_index)
                    self.courses.append(subject_index)
                # self.courses = set(self.courses.add(subjects))
                # self.instructors = set(self.instructors.add(name))

    def print_graph(self):
        print("getting list of instructors")
        print(self.instructors)

    def get_subjects(self):
        return set(self.nodes[i] for i in self.courses)

    # return list(set(items[1] for items in self.instructors))

    def get_instructors(self):
        return set(self.nodes[i] for i in self.instructors)

    # return set(items[0] for items in self.instructors)
    def create_connections(self):
        self.adjacentList = [[0 for j in range(len(set(self.courses)) + len(set(self.instructors)) + 1)] for i in
                             range(len(set(self.courses)) + len(set(self.instructors)) + 1)]
        with open(file=self.input_file) as my_file:
            lines = my_file.readlines()
            for line in lines:
                # print(line)
                data_array = line.split("/")
                name = data_array[0].strip()
                subjects = data_array[1:]
                # print(name, subjects)
                # print("creating map")
                self.create_map(name, subjects)
                # for subject in subjects:
                #     print("adding subject: ", subject)
                #     subject_index = self.check_and_add_node(node=subject.strip())
                #     print(subject_index)
                #     self.courses.append(subject_index)
                # # self.courses = set(self.courses.add(subjects))
                # # self.instructors = set(self.instructors.add(name))

    def create_map(self, instructor, subjects):
        # print("inside")
        #  self.adjacentList = [[0 for j in range(len(self.nodes))] for i in range(len(self.nodes))]
        # print(self.adjacentList)
        try:
            name_index = self.get_node_index(instructor)
            # print("inside create_map")
            no_subject_index = self.get_node_index(NO_SUBJECT)
            if subjects:
                self.adjacentList[name_index][no_subject_index] = 0
                for subject in subjects:
                    subject_index = self.get_node_index(subject.strip())
                    # print("Indexes", name_index, subject_index)
                    self.adjacentList[name_index][subject_index] = 1
                    # self.adjacentList[subject_index][name_index] = 1
                    # print(self.adjacentList)
            else:
                self.adjacentList[name_index][no_subject_index] = 1
        except:
            print("unable to create map to the course")

    # performing depth first search
    def search_course_instructors(self, course):
        # print(self.nodes)
        total_instructors = []
        # checking the teachers who teach this course
        print("List of Candidates who can handle : ", course)
        try:
            course_index = self.get_node_index(course)
            # print("Course Index : ", course_index)
            for item in set(self.instructors):
                # print("Item looking for :",item)
                # print("Index of item: ", self.get_node_index(item))
                if self.adjacentList[item][course_index] == 1:
                    total_instructors.append(self.nodes[item])
            #   items = [item for item in self.instructors if item[1] == course]
            if total_instructors:
                print(*list(item for item in total_instructors), sep='\n')
            else:
                print("No instructor found for that course: ", course)
        except:
            print("no course found with that name in database ",course)

    def show_hire_list(self):
        courses_map = set(self.courses)
        instructor_map = list(set(self.instructors))
        courses_instructors_counts = [0 for i in range(len(set(self.instructors)))]
        # print("min_list")
        print("--------Function displayHireList--------")
        length = len(instructor_map)
        instructor_count = 0
        while instructor_count < length:
            instructor_index = instructor_map[instructor_count]
            # print(instructor_index)
            courses_register = []
            count = 0
            for j in range(len(courses_map)):
                course_index = list(courses_map)[j]
                if self.adjacentList[instructor_index][course_index] == 1:
                    courses_register.append(course_index)
                    # print("found at index : ", instructor_index, course_index)
                    count = count + 1
                else:
                    pass
                    # print("no course")
            courses_instructors_counts[instructor_count] = courses_register
            instructor_count += 1
        # print(courses_instructors_counts)
        my_minimal_list = []  #
        my_minimal_list = put_max(self.instructors, self.courses, courses_instructors_counts, my_minimal_list)
        # print("My Set ",my_minimal_list)
        print("No of candidates required to cover most of the courses: ", len(my_minimal_list))
        for element in my_minimal_list:
            data = []
            node_name = self.nodes[element[0]]
            data.append(node_name)
            for elements in element[1]:
                data.append(self.nodes[elements])
            print(*data, sep=' / ')
            # instructor_to_choose=find_the_instructors_optimal(courses_instructors_counts,sum_required=len(set(self.courses)))

    # performing depth first search
    def find_course_instructors(self, courseA, courseB):
        try:
            # print(self.nodes)
            total_instructors_a = []
            total_instructors_b = []
            # checking the teachers who teach this course
            print("Part A: List of Candidates who can handle : ", courseA)
            print("Part B: List of Candidates who can handle : ", courseB)
            try:
                course_index_a = self.get_node_index(courseA)
                for item in set(self.instructors):
                    # print("Item looking for :",item)
                    # print("Index of item: ", self.get_node_index(item))
                    if self.adjacentList[item][course_index_a] == 1:
                        total_instructors_a.append(self.nodes[item])
                    # if self.adjacentList[item][course_index_b] == 1:
                    #     total_instructors_b.append(self.nodes[item])
            except Exception as e:
                pass
            finally:
                pass
            try:
                course_index_b = self.get_node_index(courseB)
                # print("Course Index : ", course_index_a)
                # print("Course Index : ", course_index_b)
                for item in set(self.instructors):
                    # print("Item looking for :",item)
                    # print("Index of item: ", self.get_node_index(item))
                    if self.adjacentList[item][course_index_b] == 1:
                        total_instructors_b.append(self.nodes[item])
            except Exception as e:
                pass
            finally:
                pass

            #   items = [item for item in self.instructors if item[1] == course]
            if total_instructors_a:
                print("Part A: ", list(item for item in total_instructors_a))
            else:
                print("Part A: No instructor found for that course: ", courseA)

            if total_instructors_b:
                print("Part B: ", list(item for item in total_instructors_b))
            else:
                print("Part B: No instructor found for that course: ", courseB)
        except Exception as e:
            print("Unable to find the instructors for course")

    def show_all(self):
        print("--------Function showAll--------")
        print("Total No. of Candidates: ", len(self.get_instructors()))
        print("Total No. of Subjects: ", len(self.get_subjects()))
        print()
        print("List of Candidates: ")
        print(*self.get_instructors(), sep='\n')
        print()
        print("List of Courses:")
        print()
        print(*self.get_subjects(), sep='\n')


class Action(enum.Enum):
    show_all='showAll'
    show_mini_list = 'showMinList'
    part_a = 'Part A'
    part_b = 'Part B'
    search_course = 'searchCourse'


class Prompt:
    part_a_value=None
    part_b_value=None

    def __init__(self, inputFile, promptFile='',resultFile='output.txt'):
        self.inputFile = inputFile
        self.resultFile= resultFile
        self.promptFile = promptFile
        self.read_prompt_file(prompt_file=self.promptFile,output_file_name=self.resultFile)
        self.instructor_map=InstructorMap(input_file=self.inputFile)

    def read_prompt_file(self, prompt_file='',output_file_name=''):
        if self.inputFile == '':
            print("input file entered location is empty")
            exit(0)
        if prompt_file == '':
            prompt_file = self.promptFile
        if output_file_name == '':
            output_file_name=self.resultFile
        print("reading promptfile: ",prompt_file,output_file_name)
        # with open(outputFileName,"a") as outputFile:
        try:
            sys.stdout = open(output_file_name,"w")
            with open(file=prompt_file) as prompts:
                lines= prompts.readlines()
                for prompt in lines:
                    self.find_and_execute(promptIn=prompt)
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            print("file saved at path: ",os.getcwd()+"/"+output_file_name)
        except:
            print("found error while reading the prompt file: ", prompt_file)

    def find_and_execute(self,promptIn):
        # part_a_value=None
        # sys.stdout=outputFile
        # part_b_value=None
        print()
        # print("Len of action: ",len(str(Action.show_mini_list)),"prompt sub: ",prompt[:len(
        # Action.show_mini_list.value)],"length of prompt: ",print(len(str(prompt))),Action.show_mini_list.value)
        if promptIn.split(':')[0].strip() == str(Action.show_mini_list.value):
            # print("executing min list")
            # outputFile.write(str(sel.instructor_map.show_hire_list()))
            # outputFile.writelines(print(self.instructor_map.show_hire_list()))
            self.instructor_map.show_hire_list()
            # original_stdout = sys.stdout # Save a reference to the original standard output
            print()
        if promptIn.split(':')[0].strip() == str(Action.show_all.value):
            # print("executing min list")
            # outputFile.write(str(sel.instructor_map.show_hire_list()))
            # outputFile.writelines(print(self.instructor_map.show_hire_list()))
            self.instructor_map.show_all()
            # original_stdout = sys.stdout # Save a reference to the original standard output
            print()
        if promptIn.split(':')[0].strip() == str(Action.search_course.value):
            print('----------------------Function displayCandidates --------')
            course_val=promptIn.split(':')[1].strip()
            self.instructor_map.search_course_instructors(course=course_val)
            print()

        if promptIn.split(':')[0].strip() == str(Action.part_a.value):
            # print("checking part a")
            Prompt.part_a_value=promptIn.split(':')[1].strip()
            # print(part_a_value)
            # part_a_value=prompt[len(Action.part_a.value):].strip(':').strip()
            # self.instructor_map.find_course_instructors(courseA=part_a_value,courseB=part_b_value)
        # else:
        #     print("looking for part_b value")
        # print("printing part_a value : ",Prompt.part_a_value)
        if promptIn.split(':')[0].strip() == str(Action.part_b.value):
            Prompt.part_b_value=promptIn.split(':')[1].strip()
            # print(part_b_value)
            # part_a_value=prompt[len(Action.part_b.value):].strip(':').strip()
        #     # self.instructor_map.find_course_instructors(courseA=part_a_value,courseB=part_b_value)
        # else:
        #     print("looking for part_a value")

        # print(part_a_value,part_b_value)
        if Prompt.part_b_value is not None and Prompt.part_a_value is not None:
            print("-------Function findCourseInstructors --------")
            self.instructor_map.find_course_instructors(courseA=Prompt.part_a_value,courseB=Prompt.part_b_value)
            print()


    # try:
        #     instructor_map = InstructorMap(self.inputFile)
        # except Exception as e:
        #     print("please check the inputfile as we are not able to locate", e)
        # try:
        #     with open(file=promptFile)


if __name__ == '__main__':
    NO_SUBJECT = 'no_subject'
    prompt = Prompt(inputFile='inputs/inputPS07.txt', promptFile='',resultFile='outputPS07.txt')
    # prompt = Prompt(inputFile='inputs/inputPS07.txt', promptFile='inputs/Sample promptsPS07.txt',
    # resultFile='outputPS07.txt')
    prompt.read_prompt_file(prompt_file='inputs/Sample promptsPS07.txt')
    # prompt.read_prompt_file(promptFile="inputs/Sample promptsPS07.txt")
    # try:
    #     instructor_map = InstructorMap(input_file='inputs/inputPS071.txt')
    # except:
    #     print("unable to open file")
    # instructor_map.read_file_and_create_node()
    # # print(instructor_map.nodes)
    # instructor_map.create_connections()
    # print("Instructors Map", instructor_map.instructors)
    # print("Courses Map: ", instructor_map.courses)
    # print("Adjacent List: ", instructor_map.adjacentList)
    # instructor_map.print_graph()
    # instructor_map.get_instructors()
    # print()
    # instructor_map.search_course_instructors(course='Software Architecture')
    # print()
    # instructor_map.find_course_instructors(courseA='Data Structures', courseB='ADE')
    # print()
    # instructor_map.show_all()
    # print()
    # instructor_map.show_hire_list()
    # print("Adjacent List: ", instructor_map.adjacentList)
    # print("Instructors Map", instructor_map.instructors)
    # print("Courses Map: ", instructor_map.courses)

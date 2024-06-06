COMMAND_EXIT = "exit"
COMMAND_ADD_STUDENTS = "add students"
COMMAND_BACK = "back"
NO_INPUT = ""
LIST_ALL = "list"
ADD_POINTS = "add points"
LOCATE_STUDENTS = "find"
CHECK_STATISTICS = "statistics"
total_courses = {"Python": 600, "DSA": 400, "Databases": 480, "Flask": 550}
current_courses = {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0}
students = list()
new_points = dict()
number_points = list()
info_add = list()
tot_notified = 0
notified_students = []


print("Learning Progress Tracker")


def check_credentials(credentials):
    each_student = dict()
    errors = {
        'first name': lambda name: check_name(name),
        'last name': lambda name: check_name(name),
        'email': lambda e_mail: check_email(e_mail)
    }
    cred_list = credentials.split()
    if len(cred_list) < 3:
        return "Incorrect credentials"
    else:
        first_name, last_name, email = cred_list[0], ' '.join(cred_list[1:-1]), cred_list[-1]
        for field, value in zip(errors.keys(), [first_name, last_name, email]):
            each_student[field] = value
            if not errors[field](value):
                return f"Incorrect {field}."
        students.append(each_student)
        if email_exists(students[:-1], email):
            students.pop()
            return "This email is already taken."
        return "The student has been added."


def email_exists(persons, email):
    for person in persons:
        if person['email'] == email:
            return True
    return False


def students_hashable(students_filled):
    student_stack = dict()
    hash_id = 10_001
    for id_hash, student in enumerate(students_filled, start=hash_id):
        student_stack[id_hash] = student
        # break
    return student_stack


def list_all_students():
    student_in_stack = students_hashable(students)
    if not student_in_stack:
        print("No students found.")
    else:
        print("Students:")
        for student in student_in_stack.keys():
            print(f"{student}")


def _is_short_name(name):
    return "." in name[-1] or len(name) == 1


def _is_char_forbidden(char):
    forbidden_chars = ["'", "-"]
    return char in forbidden_chars


def _has_forbidden_start_end_chars(name):
    return _is_char_forbidden(name[0]) or _is_char_forbidden(name[-1])


def _has_forbidden_sequences(name):
    return any(substring in name for substring in ["--", "''", "-'", "'-"])


def _has_non_ascii_chars(name):
    for char in name:
        if not char.isascii() and char not in "-'":
            return True
    return False


def check_name(name):
    if _is_short_name(name):
        return False
    if _has_forbidden_start_end_chars(name):
        return False
    if _has_forbidden_sequences(name):
        return False
    if _has_non_ascii_chars(name):
        return False
    return True


def check_email(address):
    counter = 0
    if "." not in address:
        return False
    else:
        for char in address:
            if not char.isascii() and char != "@" and char != ".":
                return False
            if char == "@":
                counter += 1
        if counter == 1:
            return True
        else:
            return False


def update_student_courses(student_dict, student_id, course_points):
    if not student_dict.get(student_id):
        print(f"No student found for id={student_id}.")
        return False
    student_dict = _process_points(student_dict, student_id, course_points)
    print("Points updated.")
    _new_points(student_dict)
    return True


def _process_points(dict_student, id_student, points_course):
    if dict_student[id_student].get('Python') is None:
        dict_student[id_student] = dict_student[id_student] | current_courses
    for course, point in zip(current_courses.keys(), points_course):
        if dict_student[id_student][course] > 0:
            dict_student[id_student][course] += point
        if dict_student[id_student][course] == 0:
            dict_student[id_student] |= {course: point}
    return dict_student


def _new_points(new_student_dict):
    for key, value in new_student_dict.items():
        new_points[key] = value
    return new_points


def student_finder():
    print("Enter an ID or 'back' to return:")
    student_all = _new_points(new_points)
    while True:
        find_input = input()
        if find_input == COMMAND_BACK:
            break
        else:
            try:
                int(find_input)
            except ValueError:
                print(f"No student is found for id={find_input}.")
                continue
        if student_all.get(int(find_input)):
            if _check_zeros(find_input):
                print(f"No student is found for id={find_input}.")
            else:
                many_points = _course_score(student_all, find_input)
                print(f"{find_input} points: {many_points}")
                continue
        else:
            print(f"No student is found for id={find_input}.")
            continue


def _course_score(student_data, finder_input):
    nothing = list()
    course_points = list()
    for course, score in student_data[int(finder_input)].items():
        if isinstance(score, int):
            course_points.append((course, score))
            nothing.append(score)
    number_points.append((finder_input, nothing))
    return "; ".join([f"{course}={score}" for course, score in course_points])


def _check_zeros(user_finder):
    zeros = list()
    [zeros.append(number_points[ref][0]) for ref in range(0, len(number_points))
     if any(number_points[ref][1]) is False]
    for ref in zeros:
        if ref == user_finder:
            if zeros.count(ref) > 0:
                return True
            break
    return False


def _check_length(added_points):
    if len(added_points) != 5:
        print("Incorrect points format.")
        return True


def _check_first_alg(added_data):
    try:
        int(added_data[0])
    except ValueError:
        if len(added_data) == 5:
            print(f"No student is found for id={added_data[0]}.")
            return True
    return False


def _check_integer(added_numbers):
    try:
        [int(point) for point in added_numbers]
    except ValueError:
        print("Incorrect points format.")
        return True


def _check_positive(added_integers):
    if not all(point >= 0 for point in [int(alg) for alg in added_integers]):
        print("Incorrect points format.")
        return True


def update_points():
    print("Enter an ID and points or 'back' to return:")
    while True:
        if students_hashable(new_points):
            all_students = _new_points(new_points)
        else:
            all_students = students_hashable(students)
        entered_data = input().split(" ")
        if entered_data[0] == COMMAND_BACK:
            break
        elif _check_first_alg(entered_data):
            continue
        elif _check_length(entered_data):
            continue
        elif _check_integer(entered_data[1:]):
            continue
        elif _check_positive(entered_data[1:]):
            continue
        student_id = int(entered_data[0])
        entered_points = [int(point) for point in entered_data[1:]]
        info_add.append((student_id, entered_points))
        if update_student_courses(all_students, student_id, entered_points):
            continue


def statistics():
    all_students = _new_points(new_points)
    print("Type the name of a course to see details or 'back' to quit")
    brief = {
        "Most popular": "n/a",
        "Least popular": "n/a",
        "Highest activity": "n/a",
        "Lowest activity": "n/a",
        "Easiest course": "n/a",
        "Hardest course": "n/a"
    }
    pointed_courses, enroll, average, activity = _stat_points(all_students, current_courses)
    for name, point in pointed_courses.items():
        if point > 0:
            brief["Most popular"] = ", ".join(_stat_roller(enroll)[0])
            brief["Least popular"] = ", ".join(_stat_roller(enroll)[1])
            brief["Highest activity"] = ", ".join(_stat_roller(activity)[0])
            brief["Lowest activity"] = ", ".join(_stat_roller(activity)[1])
            brief["Easiest course"] = ", ".join(_stat_roller(average)[0])
            brief["Hardest course"] = ", ".join(_stat_roller(average)[1])
            for key, value in brief.items():
                print(f"{key}: {value}")
            break
        else:
            for key, value in brief.items():
                print(f"{key}: {value}")
            break
    while True:
        input_course = get_validated_input()
        if input_course == COMMAND_BACK:
            break
        if input_course in current_courses.keys():
            print(input_course)
            _stat_process_points(input_course, all_students)
        else:
            print("Unknown course.")
            continue


def get_validated_input():
    course_input = input().lower()
    if course_input in ["python", "databases", "flask"]:
        course_input = course_input.title()
    if course_input in "dsa":
        course_input = course_input.upper()
    return course_input


def _stat_points(all_data, just_courses):
    enrolled = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
    for point in just_courses:
        for key in all_data:
            try:
                all_data[key][point] in just_courses.keys()
            except KeyError:
                continue
            just_courses[point] += all_data[key][point]
            if all_data[key][point] > 0:
                enrolled[point] += 1
    activity_course = _activity_topic(just_courses, info_add)
    average_course = _average_topic(just_courses, activity_course)
    return just_courses, enrolled, average_course, activity_course


def _average_topic(gross_total, enroll_topic):
    average = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
    for chain in gross_total.keys():
        if gross_total[chain] > 0:
            average[chain] = gross_total[chain] / enroll_topic[chain]
        if average[chain] == 0:
            average.pop(chain)
    return average


def _activity_topic(total_points, recording):
    activity = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
    for one in recording:
        points = one[1]
        for num in range(len(points)):
            if points[num] > 0:
                activity[list(total_points.keys())[num]] += 1
    return activity


def _stat_roller(enlisted):
    roll_out = list()
    roll_in = list()
    for cab in enlisted.keys():
        if enlisted[cab] == max(enlisted.values()):
            roll_out.append(cab)
        if enlisted[cab] == min(enlisted.values()):
            roll_in.append(cab)
    [roll_in.remove(topic) for topic in roll_out if topic in roll_in]
    if len(roll_in) == 0:
        roll_in.insert(0, "n/a")
    return roll_out, roll_in


def _stat_process_points(user_choice, students_all):
    points_of = list()
    id_pts = 0
    for key, value in students_all.items():
        id_n = key
        for course in value:
            if isinstance(value[course], int):
                id_pts = students_all[key][user_choice]
        partial = id_pts / total_courses[user_choice]
        points_of.append((id_n, id_pts, partial))
    return _stat_points_of_one(points_of)


def _stat_points_of_one(points_one_course):
    print("id      points     completed")
    points_student_course = sorted(points_one_course, key=lambda x: x[1], reverse=True)
    for person in points_student_course:
        print(f"{person[0]}   {person[1]}        {person[2]: .1%}")


def process_user_commands(input_command):
    global tot_notified
    global notified_students
    if input_command == NO_INPUT:
        print("No input")
    else:
        if input_command == COMMAND_EXIT:
            print("Bye!")
            exit()
        elif input_command == COMMAND_BACK:
            print("Enter 'exit' to exit the program.")
        elif input_command == COMMAND_ADD_STUDENTS:
            process_add_students_command()
        elif input_command == LOCATE_STUDENTS:
            student_finder()
        elif input_command == LIST_ALL:
            list_all_students()
        elif input_command == ADD_POINTS:
            update_points()
        elif input_command == CHECK_STATISTICS:
            statistics()
        elif input_command == "notify":
            add_notified = notify(new_points, notified_students)
            tot_notified += add_notified
        else:
            print("Unknown command!")


def notify(new_points, notified_students):
    new_notifications = 0
    for student_id, student_data in new_points.items():
        email = student_data.get("email")
        full_name = f"{student_data.get('first name')} {student_data.get('last name')}"
        notified = False  # Flag to track if the student has been notified
        completed_courses = [
            course for course, points in student_data.items() if
            course in total_courses and points >= total_courses[course]
        ]
        for course_completed in completed_courses:
            notification = (
                f"To: {email}\nRe: Your Learning Progress\nHello, {full_name}! You have accomplished our {course_completed} course!")
            print(notification)  # Print the notification directly
            if email not in notified_students:
                new_notifications += 1
            notified_students.append(email)  # Add the email to notified_students only once per student
    print(f'Total {new_notifications} students have been notified.')  # Update to count unique notified students
    return new_notifications

def add_student(student_command, total):
    output = check_credentials(student_command)
    print(output)
    if "Incorrect" not in output:
        total += 1
    if "already" in output:
        total -= 1
    student_command = input().strip()
    return student_command, total


def process_add_students_command():
    total = 0
    student_command = input("Enter student credentials or 'back' to return:\n").strip()
    while True:
        if student_command == COMMAND_BACK:
            print(f'Total {total} students have been added.')
            break
        elif student_command == NO_INPUT:
            print("Incorrect credentials")
            student_command = input().strip()
        else:
            student_command, total = add_student(student_command, total)



#> add students
#Enter student credentials or 'back' to return:
#> John Doe johnd@email.net
#The student has been added.
#> Jane Spark jspark@yahoo.com
#The student has been added.
#> back
#Total 2 students have been added.
#> list
#Students:
#10001
#10002
#> add points
#Enter an ID and points or 'back' to return:
#> 10001 600 400 0 0
#Points updated.
#> back
#> notify


if __name__ == "__main__":
    while True:
        user_command = input().strip()
        process_user_commands(user_command)

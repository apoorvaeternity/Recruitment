import xlsxwriter
from .models import *


def total_marks():
    marks = 0
    try:
        question = Question.objects.all()
        for q in question:
            marks += q.marks
    except Exception as e:
        print(e)

    return marks

label_personal = [
    'Sno.',
    'Student Number',
    'Name',
    'Branch',
    'Email',
    'Contact',
]

label_exam = [
    'Sno.',
    'Student Number',
    'name',
    'Marks Obtained (Out of = '+str(total_marks())+')',
    'Algorithm analysis',
    'Grand Total',
]

label_skillset = [
    'Sno.',
    'Student Number',
    'Name',
    'skills',
    'Hostler',
    'Designer',
]


class StudentInformation:
    def __init__(self):
        print("Instantiating the Constructor of StudentInformation class")

    def student_data(self):

        students = Student.objects.all()
        info = []
        for student in students:
            data = (
                int(list(students).index(student) + 1), student.student_no, student.name, student.branch, student.email,
                student.contact)
            info.append(data)
        return info

    def skill_set(self):

        info = []
        students = Student.objects.all()
        for student in students:
            data = (int(list(students).index(student) + 1), student.student_no, student.name, student.skills,
            student.hosteler,
            student.designer)
            info.append(data)
            print(info)
        return info

    def exam_data(self):

        students = MarksOfStudent.objects.all()
        info = []
        for student in students:
            data = (
                int(list(students).index(student) + 1), student.student.student_no, student.student.name, student.marks,
                None, None)
            info.append(data)
            print (info)
        return info


def create_excel():
    print("creating excel")
    print(os.system("pwd"))

    student = StudentInformation()
    student_info = student.student_data()
    exam_info = student.exam_data()
    skill_info = student.skill_set()

    workbook = xlsxwriter.Workbook("../Student_Info.xlsx")
    worksheet_info = workbook.add_worksheet('Students Info')
    worksheet_exam = workbook.add_worksheet('Exam Info')
    worksheet_skillset = workbook.add_worksheet('Student Skillset')

    # # Adding a bold format to workbook
    bold = workbook.add_format({"bold": True, 'align': 'center'})
    center_align = workbook.add_format({"align": "center"})
    row = 0
    col = 0

    for head in label_personal:
        worksheet_info.write(row, col, head, bold)
        col += 1
    col = 0

    for head in label_exam:
        worksheet_exam.write(row, col, head, bold)
        col += 1
    col = 0
    for head in label_skillset:
        worksheet_skillset.write(row, col, head, bold)
        col += 1

    row += 1

    for sn, stdno, name, email, branch, contact in student_info:
        col = 0
        worksheet_info.write(row, col, sn, center_align)
        worksheet_info.write(row, col + 1, stdno, center_align)
        worksheet_info.write(row, col + 2, name, center_align)
        worksheet_info.write(row, col + 3, email, center_align)
        worksheet_info.write(row, col + 4, branch, center_align)
        worksheet_info.write(row, col + 5, contact, center_align)
        row += 1

    row = 1
    for sn, stdno, name, tmark, almarks, grandtotal in exam_info:
        col = 0
        worksheet_exam.write(row, col, sn, center_align)
        worksheet_exam.write(row, col + 1, stdno, center_align)
        worksheet_exam.write(row, col + 2, name, center_align)
        worksheet_exam.write(row, col + 3, tmark, center_align)
        worksheet_exam.write(row, col + 4, almarks, center_align)
        worksheet_exam.write(row, col + 5, grandtotal, center_align)
        row += 1
    row = 1

    for sn, stdno, name,skills,  hostler, designer in skill_info:
        col = 0

        if hostler is True:
            h = "Yes"
        else:
            h = "No"
        if designer == '':
            d = "None"
        else:
            d = designer

        worksheet_skillset.write(row, col, sn, center_align)
        worksheet_skillset.write(row, col + 1, stdno, center_align)
        worksheet_skillset.write(row, col + 2, name, center_align)
        worksheet_skillset.write(row, col + 3, skills, center_align)
        worksheet_skillset.write(row, col + 4, h, center_align)
        worksheet_skillset.write(row, col + 5, d, center_align)
        row += 1

    # Writing content to the worksheet of work
    # worksheet.write(row,col,data)


    workbook.close()

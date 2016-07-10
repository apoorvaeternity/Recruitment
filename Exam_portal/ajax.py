import json, os
import StringIO
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .excel_creator import create_excel

from .models import Student, QuestionChoice, Question, StudentAnswer, CorrectChoice, MarksOfStudent


def excel(request):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_excel()

    excel_path = os.path.dirname(base)

    excel = open("%s/Student_Info.xlsx"%excel_path, "r")
    output = StringIO.StringIO(excel.read())
    out_content = output.getvalue()
    output.close()
    response = HttpResponse(out_content,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Students_Info.xlsx'
    return response



def delete(request):
    pk = request.GET.get('id')

    question = Question.objects.get(pk=int(pk))

    try:
        question.delete()

        return HttpResponse(json.dumps({"status": True}), content_type="application/json")
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps({"status": False}), content_type="application/json")


def question_update(request):
    if request.is_ajax() or request.method == "POST":
        id = (request.GET.get('id'))
        data = getUpdate(request, id)

        return HttpResponse(json.dumps(data), content_type="application/json")


def getUpdate(request, id):
    question = Question.objects.get(pk=id)
    print("fetching data")

    choice = question.questionchoice_set.all().order_by('id')

    correct_choice = question.correctchoice_set.all()
    correct = correct_choice[0].correct_choice.choice

    choice_list = []
    choice_data = []
    for i in range(0, len(choice)):
        data = (choice[i].choice, choice[i].id)
        choice_list.append(choice[i].choice)
        choice_data.append(data)

    correct_radio_checked = choice_list.index(correct) + 1
    print(correct_radio_checked + 1)

    data = {
        "question": question.question_text,
        "question_id": question.id,
        "marks": question.marks,
        "choice": choice_data,
        "negative": question.negative,
        "negative_marks": question.negative_marks,
        "category": question.type.id,
        "correct_checked": correct_radio_checked,

    }

    return data


def grid(request):
    if request.is_ajax() or request.method == "POST":
        id = int(request.GET.get('id'))
        print(id)

        choice, query_set = getData(id, request)

        request.session['current'] = int(id)

        return HttpResponse(json.dumps(query_set),
                            content_type="application/json")
    return None


def markCalculate(request):
    student = request.session.get('student_id')
    # question_keys = request.session.get('key_list')

    student_instance = Student.objects.get(pk=student)

    student_answer_all = student_instance.studentanswer_set.all()

    answered_question_key = []
    for i in student_answer_all:
        answered_question_key.append(i.question.id)

    print(answered_question_key)
    marks = 0

    for i in answered_question_key:
        print(i)
        question = Question.objects.get(pk=i)
        correct_choice = CorrectChoice.objects.get(question_id=i)

        student_answer = student_answer_all.get(student=student, question=question)

        # student_answer = StudentAnswer.objects.all(student=student)

        if student_answer.answer == correct_choice.correct_choice:
            marks = marks + question.marks
        elif question.negative is True and student_answer.answer != correct_choice.correct_choice and question.negative_marks is not None:
            if question.marks is not None:
                marks = marks - question.negative_marks
    print("marks")
    print(marks)

    marks_of_student, flag = MarksOfStudent.objects.get_or_create(student=Student.objects.get(pk=student),
                                                                  defaults={'marks': 0})
    marks_of_student.marks = marks
    marks_of_student.save()

    return None


#  next ajax request will also submit the question answer
#  previous will only traverse the question on the page via ajax request
#  viewing a question again will show that it is unmarked but the grid color will indicate whether you have answered the question or not
#  again submitting the answer will update the previuos answer


def submitAnswer(request):
    # print ("-----")
    # print (request.session.get('current'))
    # print (request.POST.get('answer'))
    # print (request.session.get('student_id'))
    # print ('-----')
    current = request.session.get('current')
    answer = request.POST.get('answer')
    student_id = request.session.get('student_id')

    student = Student.objects.get(pk=student_id)
    question = Question.objects.get(pk=current)
    choice = QuestionChoice.objects.get(pk=answer)

    print("student answer = {}".format(answer))

    try:
        data = StudentAnswer.objects.get(question=question, student=student)
        if data is not None:
            data.answer = choice
            data.save()
    except ObjectDoesNotExist:
        print("Object does not found")
        print("creating new instance")

        StudentAnswer.objects.create(answer=choice, question=question, student=student)

    return None


def getData(pk, request):
    question = Question.objects.get(pk=pk)
    choice = question.questionchoice_set.all().order_by('id')

    choice_data = []
    color_key = request.session.get('current')

    student = Student.objects.get(pk=request.session.get('student_id'))

    try:
        radio_checked = StudentAnswer.objects.get(student=student, question=question)
        radio_checked_key = radio_checked.answer.id
        print("Request for selecting the radio button")
        print(radio_checked_key)
    except ObjectDoesNotExist:
        pass
        radio_checked_key = None

    # print("question_no {}".format(request.session.get('key_list').index(color_key)+1))
    # print("Question :{}".format())
    question_no = request.session.get('key_list').index(pk) + 1

    for i in range(0, len(choice)):
        data = (choice[i].choice, choice[i].id)
        choice_data.append(data)

    if request.method == "POST" and request.POST.get('answer') != '':
        print("True")
        query_set = {
            "question_no": question_no,
            "question": question.question_text,
            "negative": question.negative,
            "choice_data": choice_data,
            "color": color_key,
            "radio_checked_key": radio_checked_key,
        }
    else:
        print("Method not POST or answer not submitted")
        query_set = {
            "question_no": question_no,
            "question": question.question_text,
            "negative": question.negative,
            "choice_data": choice_data,
            "radio_checked_key": radio_checked_key,
        }

    # query_set = {
    # "question": question.question_text,
    # "choices": choices,
    # }


    return choice, query_set


def ajaxnext(request):
    """
    this will select the number of any data from the database
    serialize it
    start a session
    and send the json on the page and render is using jQuery
    :param request:
    :return:
    """

    if request.is_ajax() or request.method == 'POST':

        if (request.POST.get('answer') != ''):
            submitAnswer(request)

        print(request.POST.get('answer'))

        current = request.session.get('current')
        key_list = request.session.get('key_list')

        print(key_list.index(current))
        print("before if " + str(current))
        # if (key_list.index(current) != key_list[-2]):
        if (key_list.index(current) != len(key_list) - 1):

            print(current)
            print("if is true")
            next = key_list.index(current) + 1
        else:
            next = key_list.index(current)

        print("current"),
        print(request.session.get('current'))
        print("index " + str(next))
        print(key_list[next])

        choice, query_set = getData(key_list[next], request)

        if (request.session.get('current') != key_list[-1]):
            request.session['current'] = key_list[next]

        return HttpResponse(json.dumps(query_set),
                            content_type="application/json")


def ajaxprevious(request):
    """

    :param request:
    :return:
    """
    if request.is_ajax():
        current = request.session.get('current')
        key_list = request.session.get('key_list')

        if (key_list.index(current) >= 1):
            print(current)
            previous = key_list.index(current) - 1
        else:
            previous = key_list.index(current)

        choice, query_set = getData(key_list[previous], request)

        print(request.session.get('current'))

        if request.session.get(current) != key_list[0]:
            request.session['current'] = key_list[previous]

        return HttpResponse(json.dumps(query_set),
                            content_type='application/json')

    return None


def postajax(request):
    if request.is_ajax() and request.method == "POST":
        data = request.POST.get("item")

        print (data)
        return HttpResponse(json.dumps("['rupanshu']"),
                            content_type="application/json")


def ajax_excel(request):
    create_excel()
    return HttpResponse(json.dumps("['rupanshu']"), content_type="application/json")


def checkstudent(request):
    student = None
    try:
        student_no = request.POST.get('student_no')
        student = Student.objects.get(student_no=student_no)
        print student
    except Exception as e:
        print(str(e))

    if student is not None:
        status = True
    else:
        status = False

    query_set = {
        'status': status,
        'message': "Student Number already exist in the DataBase",
    }

    return HttpResponse(json.dumps(query_set), content_type="application/json")

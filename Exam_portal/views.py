from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth
import json, os
from django.core.exceptions import ObjectDoesNotExist
# from django.template import loader, Context
from .forms import RegistrationForm, AdminForm, AdminLoginForm
from .models import Student, Question, Category, Test, CorrectChoice, MarksOfStudent
from .ajax import markCalculate


def timer(request):
    time = Test.objects.all()

    hours = time[0].time.hour
    minutes = time[0].time.minute
    seconds = time[0].time.second

    warn = time[0].warn_time

    data = {'time': [hours, minutes, seconds],
            'warn': warn}

    return HttpResponse(json.dumps(data), content_type='application/json')


def adminchoice(request):
    if not request.user.is_authenticated():
        messages.error(request, "Opps You're not an admin ")
        return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))
    path = os.path.join(os.path.dirname(settings.BASE_DIR))

    return render(request, 'Exam_portal/admin_interface.html', {"path": path})


def end(request):
    print (request.session.get('student_id'))
    if request.session.get('student_id') is None:
        messages.error(request, "First, Register for the examination here..")
        return redirect(reverse('Exam_portal:register'))
    markCalculate(request)
    print(request.session['student_id'])
    del request.session['student_id']
    request.session.modified = True

    return render(request, 'Exam_portal/end.html', {})


def show(request):
    if request.session.get('student_id') is None:
        messages.error(request, "First Register for the examination here..")
        return redirect(reverse('Exam_portal:register'))

    # category1 = get_object_or_404(Category)
    category1 = Category.objects.all()

    print category1
    if len(category1) == 0:
        messages.error(request, "Oops look like the exam is not created yet. Try after some time")
        return redirect(reverse('Exam_portal:register'))

    question = category1[0].question_set.all().order_by('id')
    # print(question[0])
    # question_object_list = list(question)
    # print(list(question))
    choice = question[0].questionchoice_set.all().order_by('id')

    category_first_data = []
    question_key = []
    print(len(category1))

    time = Test.objects.all()

    if len(time) == 0:
        messages.error(request, "Oops Time of exam is not specified yet Try after some time")
        return redirect(reverse('Exam_portal:register'))

    for i in range(0, len(category1)):
        print(i)
        print(category1[i])

        qs = category1[i].question_set.all().order_by('id')
        try:
            data = (qs[0].id, category1[i].category)
            category_first_data.append(data)
        except IndexError:
            print("skipping")
        for j in range(0, len(qs)):
            question_key.append(qs[j].id)

    print(category_first_data)
    print(question_key)
    # print(data)

    choice_data = []

    for i in range(0, len(choice)):
        data = (choice[i].choice, choice[i].id)
        choice_data.append(data)

    print (choice_data)

    # question_key =[]
    # for i in range(0,len(question_object_list)):
    #     question_key.append(question_object_list[i].id)

    print(question_key)

    # for i in range(len(choice)):
    #     print (choice.choice)
    query_set = {
        "question_no": "1",
        "question": question[0].question_text,
        "negative": question[0].negative,
        "choice_data": choice_data,
        "category": category_first_data
    }

    request.session['key_list'] = question_key
    request.session['current'] = question[0].id

    # when the first question is displayed, we first have to store its pk in a session for further submittion
    # of the user/student answer
    # on the ajax call function again a list of pk for the corresponding question will be generated and on next
    # button the index of the list will be incremented for next question fetch

    time = time[0]
    print(time.time.hour)
    print(len(str(time.time.minute)))

    if len(str(time.time.minute)) == 1:
        time_string = '0' + str(time.time.minute)
    else:
        time_string = str(time.time.minute)

    if len(str(time.time.hour)) == 1:
        time_string = '0' + str(time.time.hour) + ':' + time_string
    else:
        time_string = str(time.time.hour) + ':' + time_string

    print (time_string)
    context_variable = {
        "keys": question_key,
        "Number": range(1, len(question) + 1),
        "instance": query_set,
        "time": time_string,
        "warn": time.warn_time,

    }

    # t = loader.get_template("Exam_portal/test_template.html")
    # c = Context(context_variable)
    # render = t.render(request, c)
    # print(str(render))
    #
    #
    # return render(request, "Exam_postal/end.html" , {'page': render})
    return render(request, 'Exam_portal/ajax.html', context_variable)


def register(request):
    form = RegistrationForm()

    if request.session.get('student_id'):
        return redirect(reverse('Exam_portal:instruction'))

    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        # print("hello")
        if request.method != "POST":
            raise Http404("Only POST methods are allowed")

        if form.is_valid():
            name = form.cleaned_data['Name']
            email = form.cleaned_data['Email']
            contact = form.cleaned_data['Contact']
            studentno = form.cleaned_data['StudentNo']
            if len(str(studentno)) > 10:
                messages.error(request, "Enter a valid mobile number")
                return HttpResponseRedirect(reverse("Exam_portal:register"))
            branch = form.cleaned_data['Branch']
            if form.cleaned_data['Hosteler'] == 'y':
                hosteler = True
            else:
                hosteler = False
            skills = form.cleaned_data['Skills']
            designer = form.cleaned_data['Designer']

            data = Student.objects.create(name=name, student_no=studentno,
                                          branch=branch, contact=contact,
                                          skills=skills, email=email,
                                          hosteler=hosteler, designer=designer)
            if data:
                request.session['name'] = name
                request.session['student_id'] = data.student_no
                # same data can be used to get the corresponding did associate with the students

                return HttpResponseRedirect(reverse('Exam_portal:instruction'))

        print(form.cleaned_data)

        # print (form.errors)
    context = {
        'title': 'SI recruitment',
        'form': form,
    }

    return render(request, 'Exam_portal/register.html', context)


def instruction(request):
    # nothing to do here
    print(request)
    if request.session.get('student_id') is None:
        return redirect(reverse('Exam_portal:register'))

    return render(request, "Exam_portal/instruction.html", context={})


def admin(request):
    if not request.user.is_authenticated():
        messages.error(request, "Opps You're not an admin ")
        return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))

    category = Category.objects.all().order_by('id')
    # time = Test.objects.all()[0]
    # test = Test.objects.all()
    if request.method == "POST":
        form = AdminForm(request.POST or None)

        print("admin view is running")

        if form.is_valid():
            choice_selector = "choice"
            choice = []

            for i in range(1, 5):
                choice.append(request.POST.get(choice_selector + str(i)))

            # print(request.POST.get('new_category'))

            if request.POST.get('new_category') != "" and request.POST.get('new_category') is not None:
                category = request.POST.get('new_category')
            else:
                category = request.POST.get('category')

            # elif :
            #
            # if request.POST.get('category') != '' and request.POST.get('new_category') != "":
            #     category = request.POST.get('category')
            # else:
            #     category = request.POST.get('new_category')

            correct_choice = request.POST.get('correct_choice')

            print(choice)
            print(category)
            print(correct_choice)
            print (form.cleaned_data)

            question_data = {
                "choice": choice,
                "category": category,
                "correct_choice": correct_choice,
                "form_data": form.cleaned_data,

            }

            if update_question(question_data):
                messages.success(request, "Question have been Added into the data base")

            print(type(request.POST.get('correct_choice')))
            return HttpResponseRedirect(reverse('Exam_portal:admin'))

    else:
        form = AdminForm()

    # first = category[0].question_set.all().order_by('id')

    if category is None:
        category = "No category yet"
        category_flag = False
    else:
        category_flag = True

    query_set = {
        "category_flag": category_flag,
        "category": category,
        "form": form,
        # "first": first,
        'display_not': True,
        # "test": test,
        # "time": time,
    }

    # print (query_set)

    return render(request, "Exam_portal/update.html", query_set)


def update_question(question_data):
    print(question_data)
    print(question_data['category'])

    print(question_data['form_data']['question'])

    if question_data['form_data']['negative'] is False and question_data['form_data']['negative_marks'] is None:
        negative_marks = 0

    elif question_data['form_data']['negative'] is False and question_data['form_data']['negative_marks'] is not None:

        negative_marks = 0
    else:
        negative_marks = question_data['form_data']['negative_marks']

    print(negative_marks)
    try:
        category = Category.objects.get(category=question_data['category'])
    except ObjectDoesNotExist:
        category = Category.objects.create(category=question_data['category'])

    question = category.question_set.create(question_text=question_data['form_data']['question'],
                                            negative=question_data['form_data']['negative'],
                                            negative_marks=negative_marks,
                                            marks=question_data['form_data']['marks'])

    choice = question.questionchoice_set

    # correct_choice = question.correctchoice_set
    choice_data = question_data['choice']
    for i in range(len(choice_data)):
        choice.create(choice=choice_data[i])
        print (choice_data[i])

    CorrectChoice.objects.create(question_id=question,
                                 correct_choice=choice.get(
                                     choice=choice_data[int(question_data['correct_choice']) - 1])

                                 )

    return True


def edit_question(request):
    if not request.user.is_authenticated():
        messages.error(request, "Opps You're not an admin ")
        return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))

    category1 = Category.objects.all().order_by('id')
    question = Question.objects.all().order_by('id')
    if len(question) < 1:
        messages.success(request, "first add a Question to be added kiddo :P !!!")
        return HttpResponseRedirect(reverse('Exam_portal:adminchoice'))
    choice = question[0].questionchoice_set.all().order_by('id')

    question_key = []
    for i in question:
        question_key.append(i.id)

    print(question_key)

    question_data = []
    for i in range(1, len(question_key) + 1):
        data = (i, question_key[i - 1])
        question_data.append(data)

    # first = category1[0].question_set.all().order_by('id')

    choice_data = []
    for i in range(0, len(choice)):
        data = (choice[i].choice, choice[i].id)
        choice_data.append(data)
    # correct_choice = question.correctchoice_set.all()

    print("admin update question view is running")

    if request.method == "POST":
        form = AdminForm(request.POST or None)

        if form.is_valid():

            print("almost there")
            choice_selector = "choice"
            choice = []

            for i in range(1, 5):
                choice.append(request.POST.get(choice_selector + str(i)))
            print(choice)
            current_question = int(request.POST.get('current'))
            print(current_question)

            correct_choice = request.POST.get('correct_choice')
            #
            # time = request.POST.get('time')
            print(choice)

            print(correct_choice)
            print (form.cleaned_data)
            #
            data = {
                "choice": choice,
                "current_question": current_question,
                "correct_choice": correct_choice,
                "form_data": form.cleaned_data,

            }

            if edit_again(request, data):
                messages.success(request, "Question have been updated!")

    else:
        form = AdminForm(None)

    query_set = {
        "category": category1,
        "display": True,
        "display_not": False,
        "form": form,
        "Number": question_data,
        "question": question[0],
        # "first":first[0].id,
    }

    return render(request, "Exam_portal/update.html", query_set)


def edit_again(request, data):
    print(data)
    question = Question.objects.get(pk=data['current_question'])

    question.question_text = data['form_data']['question']

    choices = question.questionchoice_set.all().order_by('id')
    print (choices)

    count = 0
    for choice in choices:
        choice.choice = data['choice'][count]
        count += 1
        choice.save()
    if data['form_data']['negative'] is True and data['form_data']['negative_marks'] != 0:
        question.negative = data['form_data']['negative']
        question.negative_marks = data['form_data']['negative_marks']
    elif data['form_data']['negative'] is False:
        question.negative = data['form_data']['negative']
        question.negative_marks = 0
    # else:
    #     question.negative_marks = 0

    correct_query_set = question.correctchoice_set.all()

    # print(choices[int(data['correct_choice'])])

    for i in correct_query_set:
        i.correct_choice = choices[int(data['correct_choice']) - 1]
        i.save()

    question.marks = int(data['form_data']['marks'])

    question.save()

    return True


def edittime(request):
    if not request.user.is_authenticated():
        messages.error(request, "Opps You're not an admin ")
        return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))

    try:
        time_test = Test.objects.all()[0]
        time_flag = True
    except Exception:
        time_test = None
        time_flag = False

    if request.method == "POST":

        time = int(request.POST.get("minutes"))
        warn = int(request.POST.get("warn"))
        if time != 0:
            hour = int(time / 60)
            min = time % 60
            time_str = "{}:{}:00".format(hour, min)
            print(time_str)
            if time_test is None:
                Test.objects.create(name=request.POST.get('name'), time=time_str)
            else:
                time_test.time = time_str
                time_test.name = request.POST.get('name')
                time_test.warn_time = warn
                time_test.save()
            messages.success(request, "Time have been changed ! ")
            return HttpResponseRedirect(reverse('Exam_portal:edittime'))

    return render(request, "Exam_portal/time.html", {"time": time_test})


def student_section(request):
    if not request.user.is_authenticated():
        messages.error(request, "Opps You're not an admin ")
        return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))

    try:
        student_marks = MarksOfStudent.objects.all().order_by('-marks')
    except ObjectDoesNotExist:
        student_marks = "No student have given the exams yet !"

    return render(request, "Exam_portal/student_section.html", {"students": student_marks})


def admin_auth(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("Exam_portal:adminchoice"))

    error = False
    if request.method == "POST":
        form = AdminLoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            user = auth.authenticate(username=username, password=password)

            print(user)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect("/exam/adminchoice")
            else:
                messages.error(request, "Invalid user. Please enter a valid username")
                error = True
                return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))
    else:
        error = False
        form = AdminLoginForm()

    context_variable = {
        "form": form,
        "error": error,
    }

    return render(request, "Exam_portal/admin_login.html", context_variable)


def logout_admin(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("Exam_portal:admin_auth"))




# def admin_register(request):

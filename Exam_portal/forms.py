from django import forms
import re
from material import Layout, Row, Column
from .models import Student, Question
from ckeditor.widgets import CKEditorWidget
# form django.utils.translation import ugettext_lazy as _

BRANCH_CHOICES = (('cse', 'CSE'),
                  ('it', 'IT'),
                  ('ec', 'ECE'),
                  ('en', 'EN'),
                  ('me', 'ME'),
                  ('ce', 'CE'),
                  ('ei', 'EI'),
                  ('mca', 'MCA'),
                  )
YES_OR_NO = (('y', 'yes'),
             ('n', 'no'))


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class QuestionForm(forms.Form):
    question = forms.CharField(label='Question Text', max_length=500, required=True,
                               widget=forms.Textarea(attrs={'class': 'col-sm-6', 'required': 'true'}))


    # question = forms.CharField(widget=CKEditorWidget())
    marks = forms.IntegerField(label='marks', widget=forms.NumberInput(
        attrs={"required": "true"}))
    negative = forms.BooleanField(label='has negative marking', required=False)
    negative_marks = forms.IntegerField(label="negative marks", required=False)

    def clean_question(self):
        print("sddssd")
        return self.cleaned_data.get('question')


class LoginForm(forms.Form):
    student_no = forms.CharField(max_length=80, label="Student Number", widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'icon_prefix', 'class': 'validate',
                   'name': 'name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "validate"}), label="Password")

    layout = Layout(
        Row('student_no'),
        Row('password'),
    )


class RegistrationForm(forms.Form):
    Name = forms.CharField(max_length=80,
                           label='Name', widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'icon_prefix', 'class': 'validate register',
                   'name': 'name'})
                           )

    Contact = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'number', 'id': 'icon_telephone', 'class': 'validate register',
               'name': 'contact'}), label='Contact No.'
    )
    Email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'email', 'class': 'validate register'}),
        label="Email"
    )
    Password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "validate register"}), label="Password")

    Cnf_Password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "validate register"}), label="Confirm Password")

    StudentNo = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'icon_student', 'class': 'validate register',
               'name': 'student_no'}),
        label='Student No.'
    )

    Branch = forms.ChoiceField(widget=forms.Select(
        attrs={'type': 'text', 'id': 'branch', 'class': 'select-dropdown ', 'name': 'Branch'}),
        label='Choose your branch name',
        choices=BRANCH_CHOICES, required=True
    )

    Hosteler = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'type': 'radio', 'id': 'test1', 'name': 'group1'}),
        label='Are you a Hosteler?',
        choices=YES_OR_NO, required=True
    )

    Skills = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'skills_area', 'class': 'validate ',
               'name': 'skills'}),
        label='Mention your Technical skills e.g HTML, CSS, PHP, etc'
    )

    Designer = forms.CharField(widget=forms.Textarea(
        attrs={'type': 'textarea', 'id': 'designer_area', 'class': 'validate register',
               'name': 'skills'}),
        label='Any Designing Software used like Photostop,etc',
        required=False,
    )

    layout = Layout(
        Row('Name', 'StudentNo'),
        Row('Email', 'Contact'),
        Row('Password', 'Cnf_Password'),

        Row('Branch'),
        Row('Skills'),
        Row(Column('Hosteler'),
            Column('Designer')
            )
    )

    def clean_Name(self):
        name = self.cleaned_data.get('Name')

        pat = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$"
        pro = re.compile(pat)
        result = pro.match(name)

        if not bool(result):
            raise forms.ValidationError("Invalid Name format")

        if len(str(name)) > 100:
            raise forms.ValidationError("Invalid length ")

        return name

    def clean_Skills(self):
        skills = self.cleaned_data.get('Skills')

        if len(str(skills)) > 1500:
            raise forms.ValidationError("Invalid length ")

        return skills


    def clean_Designer(self):
        dsg = self.cleaned_data.get("Designer")

        if len(str(dsg)) > 200:
            raise forms.ValidationError("Invalid length ")

        return dsg

    def clean_Contact(self):
        contact = self.cleaned_data.get('Contact')
        patt = "^[7-9][0-9]{9}"
        pro = re.compile(patt)
        result = pro.match(str(contact))

        if not bool(result):
            raise forms.ValidationError("Invalid Contact number format ")

        if len(str(contact)) != 10:
            raise forms.ValidationError("Invalid Contact number format ")
        return contact


    def clean_Email(self):
        email = self.cleaned_data.get("Email")

        pattern = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
        prog = re.compile(pattern)
        result = prog.match(email)

        if not bool(result):
            raise forms.ValidationError("Invalid Email address. Use a valid email address.")

        if len(str(email)) > 60:
            raise forms.ValidationError("Invalid Length")

        return email

    def clean_Password(self):
        password = self.cleaned_data.get("Password")

        if len(str(password)) > 35:
            raise forms.ValidationError("Invalid length of password")

        return password

    def clean_Password_Cnf(self):
        cnf = self.cleaned_data.get("Cnf_Password")

        if len(str(cnf)) > 35:
            raise forms.ValidationError("Invalid length of password")

        return cnf

    def clean(self):
        if 'Password' in self.cleaned_data and 'Cnf_Password' in self.cleaned_data:
            if self.cleaned_data['Password'] != self.cleaned_data['Cnf_Password']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data

    def clean_StudentNo(self):

        std = self.cleaned_data.get('StudentNo')
        pattern = '^\d{7}[D]{0,1}$'
        prog = re.compile(pattern)
        result = prog.match(std)

        if Student.objects.all().filter(student_no=std).exists():
            raise forms.ValidationError("Student Number already exist in data base")

        if not bool(result):
            raise forms.ValidationError("Invalid format of Student number ")
        return std


class ReviewForm(RegistrationForm):

    def clean_StudentNo(self):
        return self.cleaned_data.get('StudentNo')

from django import forms
from django.http import request
import re
# from django.contrib.auth.models import User
from material import Layout, Row, Fieldset, Column, Span5
from .models import Student , ReviewFlag

# form django.utils.translation import ugettext_lazy as _

BRANCH_CHOICES = (('cse', 'CSE'),
                  ('it', 'IT'),
                  ('ec', 'EC'),
                  ('en', 'EN'),
                  ('me', 'ME'),
                  ('ce', 'CE'),
                  ('ei', 'EI'),
                  )
YES_OR_NO = (('y', 'yes'),
             ('n', 'no'))


# class AdminRegister(forms.Form):
#     username = forms.CharField(label="Username", max_length=20, required=True)
#     password1 = forms.CharField(label="Password", max_length=20,
#                                 widget=forms.PasswordInput(attrs={"name": "password1", "type": "password"}))
#     password2 = forms.CharField(label="Password Again", max_length=20,
#                                 widget=forms.PasswordInput(attrs={"name": "password1", "type": "password"}))


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class AdminForm(forms.Form):
    question = forms.CharField(label='Question Text', max_length=500, required=True,
                               widget=forms.Textarea(attrs={'class': 'col-sm-6'}))
    marks = forms.IntegerField(label='marks', required=True)
    negative = forms.BooleanField(label='have negative marking', required=False)
    negative_marks = forms.IntegerField(label="negative marks", required=False)






class RegistrationForm(forms.Form):
    Name = forms.CharField(max_length=80,
                           label='Name', widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'icon_prefix', 'class': 'validate',
                   'name': 'name'})
                           )

    Contact = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'number', 'id': 'icon_telephone', 'class': 'validate',
               'name': 'contact'}), label='Contact No.'
    )
    Email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'email', 'class': 'validate'}),
        label="Email"
    )

    StudentNo = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'icon_prefix', 'class': 'validate',
               'name': 'student_no'}),
        label='Student No.'
    )

    Branch = forms.ChoiceField(widget=forms.Select(
        attrs={'type': 'text', 'id': 'branch', 'class': 'select-dropdown', 'name': 'Branch'}),
        label='Choose your branch name',
        choices=BRANCH_CHOICES, required=True
    )

    Hosteler = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'type': 'radio', 'id': 'test1', 'name': 'group1'}),
        label='Are you a Hosteler?',
        choices=YES_OR_NO, required=True
    )

    Skills = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'id': 'icon_prefix', 'class': 'validate',
               'name': 'skills'}),
        label='Mention your Technical skills e.g HTML, CSS, PHP, etc'
    )

    Designer = forms.CharField(widget=forms.Textarea(
        attrs={'type': 'textarea', 'id': 'icon_prefix', 'class': 'validate',
               'name': 'skills'}),
        label='Any Designing Software used like Photostop,etc',
        required=False,
    )

    layout = Layout(
        Row('Name', 'StudentNo'),
        Row('Email', 'Contact'),
        Row('Branch'),
        Row('Skills'),
        Row(Column('Hosteler'),
            Column('Designer')
            )
    )

    def clean_Contact(self):
        contact = self.cleaned_data.get('Contact')
        if len(str(contact)) != 10:
            raise forms.ValidationError("Invalid length of mobile number")
        return contact

    def clean_Email(self):
        email = self.cleaned_data.get("Email")

        pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        prog = re.compile(pattern)
        result = prog.match(email)

        if not bool(result):
            raise forms.ValidationError("Invalid Email address. Use a valid email address.")

        return email

    def clean_StudentNo(self):

        review_flag = ReviewFlag.objects.get(pk=1)


        std = self.cleaned_data.get('StudentNo')
        pattern = '^\d{7}[Dd]{0,1}$'
        prog = re.compile(pattern)
        result = prog.match(std)

        if review_flag.flag:
            if Student.objects.all().filter(student_no=std).exists():
                raise forms.ValidationError("Roll Number already exist in data base")

        if not bool(result):
            raise forms.ValidationError("Invalid format of Roll number ")
        return std

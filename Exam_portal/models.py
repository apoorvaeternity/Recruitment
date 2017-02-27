from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from markdown_deux import markdown


class StudentInfo(models.Model):
    name = models.CharField(max_length=100)  # Stage1 of registration
    student_no = models.CharField(primary_key=True, max_length=225)  # Stage2 of registration
    email = models.EmailField()  # Stage1 of registration

    def __str__(self):
        return "{}|{}".format(self.name,self.student_no)



@python_2_unicode_compatible
class Student(models.Model):

    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    branch = models.CharField(max_length=5)
    contact = models.BigIntegerField()
    password = models.CharField(max_length=35, default="rupanshu")
    cnf_password = models.CharField(max_length=35 ,default="rupanshu")
    skills = models.CharField(max_length=2255)
    hosteler = models.BooleanField()  # Stage2 of
    refresh_flag = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    designer = models.CharField(
        "Mention any software you worked on(photoshop etc)",
        max_length=225)

    def __str__(self):
        return "<Name = %s>" % self.name


@python_2_unicode_compatible
class Category(models.Model):
    category = models.CharField(max_length=225)
    order = models.IntegerField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return "Category = %s" % self.category

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=5000)
    negative = models.BooleanField()
    negative_marks = models.IntegerField(null=True)
    marks = models.IntegerField()
    type = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_marked_down(self):
        return markdown(self.question_text)

    def __str__(self):
        return "<Question: %s>" % self.question_text


@python_2_unicode_compatible
class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2000)

    def get_marked_choice(self):
        return markdown(self.choice)

    def __str__(self):
        return "<Choice = %s>" % self.choice


@python_2_unicode_compatible
class CorrectChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                                    db_column='question_id')
    correct_choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

    def __str__(self):
        return "<Correct choice = %s>" % self.correct_choice


@python_2_unicode_compatible
class StudentAnswer(models.Model):
    # answer = models.CharField(max_length=225)
    answer = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    marked = models.BooleanField(default=False)

    def __str__(self):
        return "<Answer = %s>" % self.answer


@python_2_unicode_compatible
class MarksOfStudent(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return "<Option= %s>" % self.marks

@python_2_unicode_compatible

class Test(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    time = models.TimeField(null=True)
    warn_time = models.IntegerField(default=1)

    def __str__(self):
        return "<Test name = %s>" % self.name


@python_2_unicode_compatible
class ExamStarter(models.Model):
    flag = models.BooleanField(default=False)

    def __str__(self):
        return "Exam starter object"

# class PythonRegister(models.Model):
#     name = models.CharField(max_length=1000)
#     student_number = models.IntegerField()
#     email = models.EmailField()
#
#     def __str__(self):
#         return "{} - {}".format(self.name,self.student_number)

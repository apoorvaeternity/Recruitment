from django.db import models


class Student(models.Model):

    # create a  another model with student id and instantiate it with the help of this class constructor

    name = models.CharField(max_length=100)  # Stage1 of registration
    student_no = models.CharField(primary_key=True, max_length=225)  # Stage2 of registration
    branch = models.CharField(max_length=5)  # Stage2 of registration
    contact = models.BigIntegerField()  # Stage1 of registration
    skills = models.CharField(max_length=225)  # Stage3 of registration
    email = models.EmailField()  # Stage1 of registration
    hosteler = models.BooleanField()  # Stage2 of registration
    designer = models.CharField(
        "Mention any software you worked on(photoshop etc)",
        max_length=225)  # Stage3 of registration

    def __str__(self):
        return "<Name = %s>"%self.name

class Category(models.Model):
    category = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return "Category = %s"%self.category


class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    negative = models.BooleanField()
    negative_marks = models.IntegerField(null=True)
    marks = models.IntegerField()
    type = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "<Question = %s>"%self.question_text


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=225)

    def __str__(self):
        return "<Choice = %s>"%self.choice


class CorrectChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                                    db_column='question_id')
    correct_choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

    def __str__(self):
        return "<Correct choice = %s>"%self.correct_choice


class StudentAnswer(models.Model):
    # answer = models.CharField(max_length=225)
    answer = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "<Answer = %s>"%self.answer


class MarksOfStudent(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    marks = models.IntegerField()


class Test(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    time = models.TimeField(null=True)
    warn_time = models.IntegerField(default=1)

    def __str__(self):
        return "<Test name = %s>"%self.name

class ExamStarter(models.Model):

    flag = models.BooleanField(default=False)

    def __str__(self):
        return "Exam starter object"


'''
class Instructions(models.Model):
    instructions = models.CharField()

'''






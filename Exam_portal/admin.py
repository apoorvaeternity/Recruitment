from django.contrib import admin

from .models import *


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_editable = ['category','order']
    search_fields = ['category', 'order']
    list_display = ('id', 'category' , 'order')
    inlines = [QuestionInLine]

    class Meta:
        model = Category


class CorrectChoiceInLine(admin.TabularInline):
    model = CorrectChoice
    extra = 1


class QuestionChoiceInLine(admin.TabularInline):
    model = QuestionChoice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    list_editable = ['question_text', 'marks']
    list_display = ('id', 'question_text', 'marks')
    search_fields = ['quesiton_text']
    inlines = [QuestionChoiceInLine, CorrectChoiceInLine]

    class Meta:
        model = Question


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_no', 'name', 'branch')
    search_fields = ['name']
    ordering = ('student_no',)

    class Meta:
        model = Student


class Marks(admin.ModelAdmin):
    list_display = ('id', 'student', 'marks')
    ordering = ('id',)

    class Meta:
        model = MarksOfStudent


class TestDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'time')

    class Meta:
        model = Test


# Register your models here.
admin.site.register(QuestionChoice)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test,TestDisplay)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CorrectChoice)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentAnswer)
admin.site.register(MarksOfStudent, Marks)

import os
from django.contrib import admin
from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course
from django.shortcuts  import HttpResponseRedirect #
from django.urls import path #
from django.shortcuts import render #
import random

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('campus', 'name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'building', 'name', 'classroomType', 'show_schedule',
        'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(ClassroomType)
class ClassroomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'firstMonday', 'start', 'end')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'courseid', 'name', 'teacher', 'term', 'classroom', 'CLASS_TIME',
        'START_TIME', 'XQ', 'KS', 'JS', 'ZC1', 'ZC2', 'SJBZ', 'showtext')
    
    change_list_template = "entities/heroes_button.html"    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
        ]
        return my_urls + urls
    def set_immortal(self, request):
        """后台在这里加代码"""
        if request.method == 'POST':
            filepath = 'data/statefile.txt'
            with open(filepath,'w+') as fp:  
                fp.write('0') 
  
        return HttpResponseRedirect("../")

 
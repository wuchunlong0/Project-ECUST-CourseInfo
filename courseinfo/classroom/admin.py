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
    
    """ admin 添加按钮
        1、关于访问后台admin数据库问题：
        在此写入代码后，首次访问页面时，是执行后台代码的，以后再访问该页面，就不执行后台代码了。
        访问页面 http://localhost:8000/admin/classroom/course/
        2、添加按钮，后台数据如何传到前端？
        
        本例采用另外方法，实现下列功能：
        1、admin 添加按钮
        2、按‘数据库状态’按钮，判断文件是否存在
        3、文件不存在，显示‘数据库状态’按钮、‘同步数据库’按钮。按‘同步数据库’按钮，创建一个文件
        4、文件存在，显示‘数据库状态’按钮、‘数据库同步中，请稍等...’。    
    """
    
    filepath = 'data/statefile.txt' #创建文件路径
    change_list_template = "entities/heroes_span.html"     
    def get_urls(self):        
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
            path('mortal/', self.set_mortal),
        ]
        return my_urls + urls
    
    def set_immortal(self, request):
        """后台在这里加代码"""
        #self.message_user(request, "All heroes are now mortal")
        if request.method == 'POST':
            with open(self.filepath,'w+') as fp:  
                fp.write('0') 
        self.change_list_template = "entities/heroes_span.html"  
        return HttpResponseRedirect("../")
    
    def set_mortal(self, request):
        """后台在这里加代码"""        
        if os.path.exists(self.filepath):
            self.change_list_template = "entities/heroes_span.html"             
        else:
            self.change_list_template = "entities/heroes_button.html" 
        return HttpResponseRedirect("../")


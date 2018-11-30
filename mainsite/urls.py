# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:urls.py
@time:2018/11/27 17:31
"""
from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    re_path(r'^$', views.signin, name='signin'),
    re_path(r'^signin/$', views.signin_action, name='signin_action'),
    re_path(r'^mainpage$', views.mainpage, name='mainpage'),
    re_path(r'^student(?P<order>s_.*)/$', views.student, name='student'),
    re_path(r'^student/edit/(?P<s_no>[0-9]+)/$', views.student_edit, name='student_edit'),
    re_path(r'^student/edit/action$', views.student_edit_action, name='student_edit_action'),
    re_path(r'^student/delete/(?P<s_no>[0-9]+)/$', views.student_delete, name='student_delete'),
    re_path(r'^course/(?P<order>c_.*)/$', views.course, name='course'),
    re_path(r'^course/edit/(?P<c_no>[0-9]+)/$', views.course_edit, name='course_edit'),
    re_path(r'^course/edit/action$', views.course_edit_action, name='course_edit_action'),
    re_path(r'^course/delete/(?P<c_no>[0-9]+)/$', views.course_delete, name='course_delete'),
    re_path(r'^score/student/(?P<s_no>[0-9]+)/(?P<order>mainsite.*)/$', views.score_student, name='score_student'),
    re_path(r'^score/student/edit/(?P<s_no>[0-9]+)/(?P<c_no>[0-9]+)/$', views.score_student_edit,name='score_student_edit'),
    re_path(r'^score/student/edit/action$', views.score_student_edit_action,name='score_student_edit_action'),
    re_path(r'^score/student/add/(?P<s_no>[0-9]+)$', views.score_student_add,name='score_student_add'),
    re_path(r'^score/student/add/action$', views.score_student_add_action,name='score_student_add_action'),
    re_path(r'^score/student/delete/(?P<s_no>[0-9]+)/(?P<c_no>[0-9]+)/$', views.score_student_delete,name='score_student_delete'),
    re_path(r'^score/course/(?P<c_no>[0-9]+)/(?P<order>mainsite.*)/$', views.score_course, name='score_course'),
    re_path(r'^score/course/edit/(?P<c_no>[0-9]+)/(?P<s_no>[0-9]+)/$', views.score_course_edit,name='score_course_edit'),
    re_path(r'^score/course/edit/action$', views.score_course_edit_action,name='score_course_edit_action'),
    re_path(r'^score/course/add/(?P<c_no>[0-9]+)$', views.score_course_add,name='score_course_add'),
    re_path(r'^score/course/add/action$', views.score_course_add_action,name='score_course_add_action'),
    re_path(r'^score/course/delete/(?P<c_no>[0-9]+)/(?P<s_no>[0-9]+)/$', views.score_course_delete,name='score_course_delete'),
]

urlpatterns += staticfiles_urlpatterns()
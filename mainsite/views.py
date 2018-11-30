import sqlite3

from django.shortcuts import render
from django.http import HttpResponse

from . import models


# Create your views here.

def signin(request):
    return render(request, 'mainsite/signin.html', {'info': '请输入管理员账号密码'})


def signin_action(request):
    name = request.POST.get('username')
    password = request.POST.get('password')

    users = models.User.objects.filter(pk=name)
    if len(users) == 0:
        return render(request, 'mainsite/signin.html', {'info': '用户名错误!'})
    if users[0].user_password != password:
        return render(request, 'mainsite/signin.html', {'info': '密码错误!'})

    return render(request, 'mainsite/mainpage.html')


def mainpage(request):
    return render(request, 'mainsite/mainpage.html')


def student(request, order='s_no'):
    students = models.Student.objects.all().order_by(order, 's_no')
    return render(request, 'mainsite/student.html', {'students': students})


def student_edit(request, s_no):
    if str(s_no) == '0':
        return render(request, 'mainsite/student_edit.html')
    student = models.Student.objects.get(s_no=s_no)
    return render(request, 'mainsite/student_edit.html', {'student': student})


def student_edit_action(request):
    s_no = request.POST.get('no')
    s_name = request.POST.get('name')
    s_age = int(request.POST.get('age'))
    s_sex = request.POST.get('sex')
    s_class = request.POST.get('class')

    students = models.Student.objects.filter(s_no=s_no)

    if len(students) == 0:
        models.Student.objects.create(s_no=s_no, s_name=s_name, s_age=s_age, s_sex=s_sex, s_class=s_class)
    elif len(students) == 1:
        students[0].s_no = s_no
        students[0].s_name = s_name
        students[0].s_sex = s_sex
        students[0].s_age = s_age
        students[0].s_class = s_class
        students[0].save()

    return student(request)


def student_delete(request, s_no):
    models.Student.objects.get(s_no=s_no).delete()

    return student(request)


def course(request, order='c_no'):
    courses = models.Course.objects.all().order_by(order, 'c_no')
    return render(request, 'mainsite/course.html', {'courses': courses})


def course_edit(request, c_no):
    if str(c_no) == '0':
        return render(request, 'mainsite/course_edit.html')
    course = models.Course.objects.get(c_no=c_no)
    return render(request, 'mainsite/course_edit.html', {'course': course})


def course_edit_action(request):
    c_no = request.POST.get('no')
    c_name = request.POST.get('name')

    courses = models.Course.objects.filter(c_no=c_no)

    if len(courses) == 0:
        models.Course.objects.create(c_no=c_no, c_name=c_name)
    elif len(courses) == 1:
        courses[0].c_no = c_no
        courses[0].c_name = c_name
        courses[0].save()

    return course(request)


def course_delete(request, c_no):
    models.Course.objects.get(c_no=c_no).delete()

    return course(request)


def score_student(request, s_no, order='mainsite_course.c_no'):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    sql = """SELECT mainsite_course.c_no,mainsite_course.c_name,mainsite_score.sc_score\
    FROM mainsite_score JOIN mainsite_course\
    ON mainsite_course.c_no=mainsite_score.sc_cno_id\
    WHERE mainsite_score.sc_sno_id='{s_no}' ORDER BY  {order},mainsite_course.c_no """.format(s_no=s_no, order=order)

    result = c.execute(sql)
    conn.commit()

    scores = []
    for i in result:
        scores.append({'c_no': i[0], 'c_name': i[1], 'score': i[2]})

    s_name = models.Student.objects.get(s_no=s_no).s_name

    return render(request, 'mainsite/score_student.html', {'s_no': s_no, 's_name': s_name, 'scores': scores})


def score_student_edit(request, s_no, c_no):
    score = models.Score.objects.get(sc_sno=s_no, sc_cno=c_no)
    s_name = models.Student.objects.get(s_no=s_no).s_name

    return render(request, 'mainsite/score_student_edit.html',
                  {'score': score, 's_no': s_no, 's_name': s_name, 'c_no': c_no})


def score_student_edit_action(request):
    s_no = request.POST.get('s_no')
    c_no = request.POST.get('c_no')
    score = int(request.POST.get('score'))

    sc = models.Score.objects.get(sc_sno=s_no, sc_cno=c_no)
    sc.sc_score = score
    sc.save()

    return score_student(request, s_no)


def score_student_add(request, s_no):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    sql = """SELECT * FROM  mainsite_course"""

    result = c.execute(sql)
    conn.commit()

    courses = []
    for i in result:
        courses.append({'c_no': i[0], 'c_name': i[1]})

    s_name = models.Student.objects.get(s_no=s_no).s_name

    return render(request, 'mainsite/score_student_add.html', {'courses': courses, 's_no': s_no, 's_name': s_name})


def score_student_add_action(request):
    c_no = request.POST.get('c_no')
    s_no = request.POST.get('s_no')
    score = int(request.POST.get('score'))

    scs = models.Score.objects.filter(sc_sno=s_no, sc_cno=c_no)

    if len(scs) == 0:
        models.Score.objects.create(sc_sno=models.Student.objects.get(s_no=s_no),
                                    sc_cno=models.Course.objects.get(c_no=c_no), sc_score=score)
    elif len(scs) == 1:
        scs[0].sc_sno = models.Student.objects.get(s_no=s_no)
        scs[0].sc_cno = models.Course.objects.get(c_no=c_no)
        scs[0].sc_score = score
        scs[0].save()

    return score_student(request, s_no)


def score_student_delete(request, s_no, c_no):
    models.Score.objects.get(sc_sno=s_no, sc_cno=c_no).delete()

    return score_student(request, s_no)

def score_course(request, c_no, order='mainsite_student.s_no'):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    sql = """SELECT mainsite_student.s_no,mainsite_student.s_name,mainsite_student.s_class,mainsite_score.sc_score\
    FROM mainsite_score JOIN mainsite_student\
    ON mainsite_student.s_no=mainsite_score.sc_sno_id\
    WHERE mainsite_score.sc_cno_id='{c_no}' ORDER BY  {order},mainsite_student.s_no """.format(c_no=c_no, order=order)

    result = c.execute(sql)
    conn.commit()

    scores = []
    for i in result:
        scores.append({'s_no': i[0], 's_name': i[1],'s_class':i[2], 'score': i[3]})

    c_name = models.Course.objects.get(c_no=c_no).c_name

    return render(request, 'mainsite/score_course.html', {'c_no': c_no, 'c_name': c_name, 'scores': scores})

def score_course_edit(request, s_no, c_no):
    score = models.Score.objects.get(sc_sno=s_no, sc_cno=c_no)
    s_name = models.Student.objects.get(s_no=s_no).s_name
    c_name = models.Course.objects.get(c_no=c_no).c_name

    return render(request, 'mainsite/score_course_edit.html',
                  {'score': score, 's_no': s_no, 's_name': s_name, 'c_name': c_name,'c_no': c_no})


def score_course_edit_action(request):
    s_no = request.POST.get('s_no')
    c_no = request.POST.get('c_no')
    score = int(request.POST.get('score'))

    sc = models.Score.objects.get(sc_sno=s_no, sc_cno=c_no)
    sc.sc_score = score
    sc.save()

    return score_course(request, c_no)


def score_course_add(request, c_no):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    sql = """SELECT * FROM  mainsite_student"""

    result = c.execute(sql)
    conn.commit()

    students = []
    for i in result:
        students.append({'s_no': i[0], 's_name': i[1]})

    c_name = models.Course.objects.get(c_no=c_no).c_name

    return render(request, 'mainsite/score_course_add.html', {'students': students, 'c_no': c_no, 'c_name': c_name})


def score_course_add_action(request):
    c_no = request.POST.get('c_no')
    s_no = request.POST.get('s_no')
    score = int(request.POST.get('score'))

    scs = models.Score.objects.filter(sc_sno=s_no, sc_cno=c_no)

    if len(scs) == 0:
        models.Score.objects.create(sc_sno=models.Student.objects.get(s_no=s_no),
                                    sc_cno=models.Course.objects.get(c_no=c_no), sc_score=score)
    elif len(scs) == 1:
        scs[0].sc_sno = models.Student.objects.get(s_no=s_no)
        scs[0].sc_cno = models.Course.objects.get(c_no=c_no)
        scs[0].sc_score = score
        scs[0].save()

    return score_course(request, c_no)


def score_course_delete(request, c_no, s_no):
    models.Score.objects.get(sc_sno=s_no, sc_cno=c_no).delete()

    return score_course(request, c_no)


from django.db import models


# Create your models here.

class Student(models.Model):
    s_no = models.CharField(primary_key=True, max_length=12)
    s_name = models.CharField(max_length=32)
    s_sex = models.CharField(max_length=3)
    s_age = models.IntegerField()
    s_class = models.CharField(max_length=5)
    pub_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{no} {name}".format(no=self.s_no, name=self.s_name)


class Course(models.Model):
    c_no = models.CharField(primary_key=True, max_length=12)
    c_name = models.CharField(max_length=32)
    pub_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.c_name


class Score(models.Model):
    sc_sno = models.ForeignKey(to='Student', to_field='s_no', on_delete=models.CASCADE)
    sc_cno = models.ForeignKey(to='Course', to_field='c_no', on_delete=models.CASCADE)
    sc_score = models.IntegerField()
    pub_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{sno} {cno} {score}".format(sno=self.sc_sno, cno=self.sc_cno,score=self.sc_score)

class User(models.Model):

    user_name=models.CharField(max_length=32,primary_key=True)
    user_password=models.CharField(max_length=3)
    pub_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
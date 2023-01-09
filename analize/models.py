from sre_constants import BRANCH
from django.db import models

class Mydata(models.Model):
    RollNo=models.CharField(max_length=30)
    SGPA=models.CharField(max_length=30)
    CGPA=models.CharField(max_length=30)
    Failed_Subjects= models.CharField(max_length=30)
    Passed_Subjects= models.CharField(max_length=30)
    Passed_Out_Year= models.CharField(max_length=30)
    Semester=models.CharField(max_length=30)
    Section=models.CharField(max_length=30)
    No_of_backlogs=models.IntegerField()
    Absent_subjects=models.CharField(max_length=30)
    def __str__(self):
        return self.RollNo
class Reference(models.Model):
    Subjects= models.CharField(max_length=30)
    Passed_Out_Year= models.CharField(max_length=30)
    Semester=models.CharField(max_length=30)
    Absenties=models.CharField(max_length=30)
    Faculty=models.TextField()
    Sections=models.CharField(max_length=20,default="None")
    # def __str__(self):
    #     return self.Passed_Out_Year
class Login(models.Model):
    id=models.IntegerField(primary_key=True)
    Username=models.CharField(max_length=30)
    Password=models.CharField(max_length=30)
    Branch=models.CharField(max_length=30)
class students_info(models.Model):
    RollNo=models.CharField(max_length=30 ,primary_key=True)
    SGPA=models.TextField(max_length=1000)
    CGPA=models.TextField(max_length=1000)
    Failed_Subjects= models.TextField(max_length=1000)
    Passed_Subjects= models.TextField(max_length=1000)
    Passed_Out_Year= models.TextField(max_length=1000)
    Semester=models.TextField(max_length=1000)
    Branch=models.CharField(max_length=30)
    Section=models.CharField(max_length=30)
    No_of_backlogs=models.CharField(max_length=30)

# Create your models here.

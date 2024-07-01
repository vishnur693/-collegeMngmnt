from django.db import models
from django.contrib.auth.models import User

class userDB(models.Model):
    user_name=models.CharField(max_length=255,null=True)
    user_mail=models.EmailField(null=True)
    user_password=models.CharField(max_length=255,null=True)

class courseDB(models.Model):
    course_name=models.CharField(max_length=255,null=True)
    course_fee=models.IntegerField(null=True)

class studentDB(models.Model):
    student_name=models.CharField(max_length=255,null=True)
    address=models.CharField(max_length=255,null=True)
    age=models.IntegerField(null=True)
    course=models.ForeignKey(courseDB,on_delete=models.CASCADE,null=True)

class teacherDB(models.Model):
    t_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    t_course = models.ForeignKey(courseDB, on_delete=models.CASCADE, null=True)
    t_add = models.CharField(max_length=255, null=True)
    t_age = models.IntegerField(null=True)
    t_cno = models.BigIntegerField(null=True)  # Adjusted to BigIntegerField
    t_pht = models.ImageField(upload_to="image/", null=True)
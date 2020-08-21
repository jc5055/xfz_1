from django.db import models
from shortuuidfield import ShortUUIDField

# Create your models here.

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)


class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()


class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)


class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1 支付宝 2微信
    istype = models.SmallIntegerField(default=0)
    # 1未支付 2支付成功
    status = models.SmallIntegerField(default=1)

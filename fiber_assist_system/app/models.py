from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


# Create your models here.


class User(AbstractUser):
    is_reset = models.CharField(max_length=20, null=False, verbose_name='是否重置')
    photo = models.ImageField(upload_to='img',null=True,default='/media/1.jpg')
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


class Team(models.Model):
    teamname=models.CharField(max_length=30,null=False,verbose_name='团队名')
    teamdate = models.DateTimeField(default=timezone.now, name='teamdate')

    class Meta:
        # permissions = (("view_team_page","can see team page"),
        #                ("change_team_info", "can change team "),)
        verbose_name = '团队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teamname

class Teamer_temp(models.Model):
    user = models.ForeignKey(User, verbose_name='用户id')
    team = models.ForeignKey(Team, verbose_name='团队id')
    date = models.DateTimeField(default=timezone.now, name='applydate')
    is_pass = models.CharField(max_length=20, null=False, verbose_name='是否通过审核')


    class Meta:
        verbose_name = '团队成员审核表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username+" "+self.team.teamname)


class User_login_log(models.Model):
    login_ip = models.CharField(max_length=20, null=False, verbose_name='登录ip')
    login_date = models.DateTimeField(default=timezone.now, name='login_date')
    user = models.ForeignKey(User, verbose_name='用户')
    login_system = models.CharField(max_length=20,verbose_name='用户系统')

    class Meta:
        verbose_name = '用户登录信息'
        verbose_name_plural = verbose_name
        ordering = ['-login_date']

    def __str__(self):
        return str(self.user.username)


class Team_temp(models.Model):
    teamname = models.CharField(max_length=30, null=False, verbose_name='团队名')
    teamdate = models.DateTimeField(default=timezone.now, name='teamdate')
    user = models.ForeignKey(User, verbose_name='用户id')
    is_pass = models.CharField(max_length=10, null=False, verbose_name='是否通过验证')

    class Meta:
        verbose_name = '团队审核中间表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.teamname



class Team_User(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    team = models.ForeignKey(Team, verbose_name='团队')
    ut_type = models.CharField(max_length=20, null=False, verbose_name='团队身份')

    class Meta:
        verbose_name = '团队用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username+" "+self.team.teamname)


class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=100)


class Rule_score(models.Model):
    rulestrs = models.CharField(max_length=2000,verbose_name="规则", null=False)
    score = models.FloatField(default=0.00)
    user_num = models.IntegerField(default=0,verbose_name="打分人数")
    class Meta:
        verbose_name = '规则得分'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)



class Rule_user(models.Model):
    rule = models.ForeignKey(Rule_score,verbose_name="规则")
    user = models.ForeignKey(User,verbose_name='用户')
    myscore = models.FloatField(default=0.00)
    class Meta:
        verbose_name = '用户规则评分'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.rule.id)


class Analysis_manage(models.Model):
    ana_id = models.CharField(max_length=100, verbose_name="分析id", null=False)
    ana_name = models.CharField(max_length=100, verbose_name="分析管理名", null=False)
    is_show = models.BooleanField(default=False, verbose_name="是否显示", null=False)
    class Meta:
        verbose_name = '分析管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)


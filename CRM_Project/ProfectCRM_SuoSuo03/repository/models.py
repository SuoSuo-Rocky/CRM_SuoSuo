from django.db import models

# Create your models here.
from django.contrib.auth.models import  User



from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        # default="shiwei@qq.com",
        # blank = True,
        # null = True,
    )
    name = models.CharField(max_length=1024, verbose_name='姓名')
    role = models.ManyToManyField('Role', blank=True, null=True, verbose_name='拥有角色')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    class Meta:
        verbose_name_plural = "自定义用户登录表"
        permissions = (
            ("repository_backend_page", "可访问所有 app 下的 所有表"),
            ("repository_app_page", "可访问一个 app 下的所有表"),
            ("repository_table_obj_list", "可访问一张表中的 所有 数据记录"),
            ("repository_table_obj_add", "可添加表记录数据"),
            ("repository_table_obj_change", "可对表记录数据进行修改"),
            ("repository_table_obj_delete", "可删除表记录数据"),
        )
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


# class UserProfile(models.Model):
#     """用户信息表"""
#     # 与 系统关联 账户 该 为  一 对 一
#     user = models.OneToOneField(to=User,on_delete=models.CASCADE, verbose_name='关联系统账户')
#     name = models.CharField(max_length=1024,verbose_name='姓名')
#     role = models.ManyToManyField('Role', blank=True, null=True, verbose_name='拥有角色')
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural = "用户信息表"



class Role(models.Model):
    """ 角色表"""
    name = models.CharField(max_length=1024,unique=True)
    menus = models.ManyToManyField('Menus', blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "角色表"

class CustomerInfo(models.Model):
    """ 客户信息表 """
    name = models.CharField(max_length=1024,default=None,verbose_name='客户姓名')
    contact_type_choices = (
        (0, 'qq '),
        (1, '微信'),
        (2, '手机'),
    )
    contact_type = models.SmallIntegerField(choices=contact_type_choices,default=0,verbose_name='联系来源')
    contact = models.CharField(max_length=1024,unique=True,verbose_name='联系方式')
    source_choices = (
        (0, 'QQ群'),
        (1, '51CTO'),
        (2, "百度推广"),
        (3, "知乎"),
        (4, "转介绍"),
        (5, "其他"),
    )
    source = models.SmallIntegerField(choices=source_choices,verbose_name='客户来源')
    referral_from = models.ForeignKey('self', blank=True,null=True,verbose_name='转介绍', on_delete=models.CASCADE)
    consult_courses = models.ManyToManyField('Course',verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')
    status_choices = (
        (0, '未报名'),
        (1, '已报名'),
        (2, '已退学'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='客户状态')
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE,verbose_name='课程顾问')

    id_num = models.CharField(max_length=1024, blank=True, null=True, verbose_name='身份证号')
    emergency_contact = models.PositiveSmallIntegerField( blank=True, null=True, verbose_name='紧急联系')
    sex_choices = (
        (0, '男'),
        (1, '女')
    )
    sex = models.PositiveSmallIntegerField(choices=sex_choices, blank=True, null=True, verbose_name='性别')

    date = models.DateField(auto_now_add=True,verbose_name='建交时间')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "客户信息表"

class Student(models.Model):
    """  学员表"""
    # name = models. CharField(max_length=1024,verbose_name='学员姓名')
    customer = models.OneToOneField('CustomerInfo', on_delete=models.CASCADE, verbose_name='详细信息')
    class_grades = models.ManyToManyField('ClassList', verbose_name='所在班级')
    def __str__(self):
        return self.customer.name    # 要添加  name , 否则报错， 返回类型必须是 字符串
    class Meta:
        verbose_name_plural = '学员表'

class CustomerFollowUp(models.Model):
    """  客户跟踪  记录表 """
    customer = models.ForeignKey('CustomerInfo',verbose_name='客户', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟踪内容')
    user = models.ForeignKey("UserProfile" ,verbose_name='跟进人', on_delete=models.CASCADE)
    status_choices = (
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2 周内报名'),
        (3, '已 报名'),
    )
    status = models.SmallIntegerField(choices=status_choices,verbose_name='跟踪客户状态')
    date = models.DateField(auto_now_add=True, verbose_name='跟踪 创建时间')
    def __str__(self):
        return self.content
    class Meta:
        verbose_name_plural = '客户跟踪记录表'

class Course(models.Model):
    """ 课程表 """
    name = models.CharField(max_length=1024,verbose_name='课程名称',unique=True)
    price = models.PositiveIntegerField(verbose_name='课程价格')
    perid = models.PositiveIntegerField(verbose_name='课程周期(月)', default=5)
    outline = models.TextField(verbose_name='课程大纲')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '课程表'

class  ClassList(models.Model):
    """  班级列表 """
    branch = models.ForeignKey('Branch',verbose_name='所在校区', on_delete=models.CASCADE)
    course = models.ForeignKey('Course',verbose_name='班级课程', on_delete=models.CASCADE)
    class_type = (
        (0, '脱产'),
        (0, '周末'),
        (0, '网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type,verbose_name='班级类型', default=0)
    semester = models.SmallIntegerField(verbose_name='学期')
    contract_template = models.ForeignKey('ContractTemplate', blank=True, null=True, on_delete=models.CASCADE, verbose_name='班级合同')
    teachers = models.ManyToManyField('UserProfile', verbose_name='讲师',)
    start_date = models.DateField('开班日期')
    graduate_date = models.DateField('毕业日期', blank=True, null=True)

    def __str__(self):
        return "%s(%s)期"%(self.course.name,self.semester)
    class Meta:
        unique_together = ('branch', 'class_type', 'course', 'semester')
        verbose_name_plural = '班级列表 '

class CourseRecord(models.Model):
    """   上课记录 """
    class_grade = models.ForeignKey(to='ClassList', verbose_name='所属班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey('UserProfile', verbose_name='讲师', on_delete=models.CASCADE)
    title = models.CharField('本节主题', max_length=1024,)
    content = models.TextField(verbose_name='本节内容')
    has_homework = models.BooleanField(verbose_name='本节是否有作业', default=True)
    homework = models.TextField(verbose_name='作业需求法', blank=True, null=True)
    date = models.DateTimeField(verbose_name='上课记录创建时间', auto_now_add=True)
    def   __str__(self):
        return "%s(第%s)节"%(self.class_grade,self.day_num)

    class Meta:
        unique_together = ('class_grade', 'day_num')
        verbose_name_plural = '讲师上课记录表'

class StudyRecord(models.Model):
    """  学习记录表"""
    course_record = models.ForeignKey(to='CourseRecord', verbose_name='所属课堂', on_delete=models.CASCADE)
    student = models.ForeignKey('Student' ,verbose_name='学生姓名', on_delete=models.CASCADE)
    score_choices = (
        (100, "A+"),
        (90, "A"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (0, "N/A"),  # not avaliable
        (-100, "COPY"),  # not avaliable
    )
    score = models.SmallIntegerField(choices=score_choices,verbose_name='学生成绩', default=0)
    show_choices = (
        (0, '缺勤'),
        (1, '已签到'),
        (2, '迟到'),
        (3, '早退'),
    )
    show_status = models.SmallIntegerField(choices=show_choices, verbose_name='学生状态', default=1)
    note = models.TextField(verbose_name='成绩备注')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-->%s:%s"%(self.course_record,self.student, self.score)
    class Meta:
        verbose_name_plural = '学员学习记录表'

class Branch(models.Model):
    """  校区"""
    name = models.CharField(max_length=1024,unique=True)
    addr = models.CharField(max_length=1024, blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '校区表'

class Menus(models.Model):
    """  动态菜单 """
    name = models.CharField(max_length=1024,verbose_name='菜单名')
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic')
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0, verbose_name='菜单类型')
    url_name = models.CharField(max_length=1024, verbose_name=' 菜单URL')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')
        verbose_name_plural = '动态菜单表'

class ContractTemplate(models.Model):
    """   存储 合同模板  """
    name = models.CharField(max_length=1024)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "合同模板表"

class StudentEnrollment(models.Model):
    """  学员报名表 """
    customer = models.ForeignKey("CustomerInfo", verbose_name='客户名', on_delete=models.CASCADE)
    class_grade = models.ForeignKey('ClassList', verbose_name='报名班级', on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile', verbose_name='报名顾问', on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False, verbose_name='合同状态')
    contract_signed_date = models.DateTimeField(blank=True, null=True, verbose_name='合同同意日期')
    contract_approved = models.BooleanField(default=False, verbose_name='审核状态')
    contract_approved_date = models.DateTimeField(blank=True, null=True, verbose_name='合同审核日期')
    class Meta:
        verbose_name_plural = '学员报名表'
        unique_together = ('customer', 'class_grade')

    def __str__(self):
        return self.customer.name

class PaymentRecord(models.Model):
    """  学员缴费 记录表  """
    enrollment  = models.ForeignKey('StudentEnrollment', verbose_name='所在报名表', on_delete=models.CASCADE)
    payment_type_choices = (
        (0, '报名费'),
        (1, '学费'),
        (2, '退费'),
    )
    payment_type = models.SmallIntegerField(choices=payment_type_choices, verbose_name='缴费类型')
    amount = models.IntegerField(default=500, verbose_name='缴费金额')
    consultant = models.ForeignKey('UserProfile', verbose_name='缴费顾问', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='缴费日期')

    class Meta:
        verbose_name_plural = '缴费记录表'
    def __str__(self):
        return "%s 缴费 %s 金额" %(self.enrollment.customer.name, self.amount)








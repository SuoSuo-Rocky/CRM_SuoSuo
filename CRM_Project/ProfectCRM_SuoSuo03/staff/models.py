from django.db import models

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=1024, verbose_name='名称')
    gender_choices = (
        (0, "男"),
        (1, '女')
    )
    gender = models.IntegerField(choices=gender_choices, verbose_name='性别')
    age = models.BigIntegerField(verbose_name='年龄')
    role = models.ManyToManyField('Role', verbose_name='角色', null=True, blank=True)
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=1024)
    menus = models.ManyToManyField('Menus', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"


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
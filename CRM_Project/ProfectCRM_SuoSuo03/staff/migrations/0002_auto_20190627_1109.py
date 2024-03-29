# Generated by Django 2.1.3 on 2019-06-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='菜单名')),
                ('url_type', models.SmallIntegerField(choices=[(0, 'absolute'), (1, 'dynamic')], default=0, verbose_name='菜单类型')),
                ('url_name', models.CharField(max_length=1024, verbose_name=' 菜单URL')),
            ],
            options={
                'verbose_name_plural': '动态菜单表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('menus', models.ManyToManyField(blank=True, null=True, to='staff.Menus')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together={('name', 'url_name')},
        ),
        migrations.AddField(
            model_name='animal',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, to='staff.Role', verbose_name='角色'),
        ),
    ]

# Generated by Django 3.2.23 on 2024-01-16 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Config', '0003_webauth_m_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.IntegerField(blank=True, verbose_name='菜单id')),
                ('m_path', models.CharField(blank=True, max_length=100, verbose_name='menu路径')),
                ('username', models.CharField(blank=True, max_length=50, verbose_name='用户登录名')),
                ('switch', models.BooleanField(default=False, verbose_name='开关')),
                ('state', models.BooleanField(default=False, verbose_name='状态')),
            ],
        ),
    ]

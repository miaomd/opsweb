# Generated by Django 3.2.23 on 2024-01-04 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.IntegerField(blank=True, verbose_name='菜单id')),
                ('role', models.CharField(blank=True, max_length=50, verbose_name='角色')),
                ('switch', models.BooleanField(default=False, verbose_name='开关')),
                ('state', models.BooleanField(default=False, verbose_name='状态')),
            ],
        ),
        migrations.RemoveField(
            model_name='menu',
            name='level',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='up_level',
        ),
        migrations.AddField(
            model_name='menu',
            name='fid',
            field=models.IntegerField(blank=True, default=0, verbose_name='上级id'),
        ),
        migrations.AddField(
            model_name='menu',
            name='has_child',
            field=models.BooleanField(default=False, verbose_name='是否有下级'),
        ),
        migrations.AddField(
            model_name='menu',
            name='index',
            field=models.IntegerField(blank=True, null=True, verbose_name='层级内顺序号'),
        ),
        migrations.AddField(
            model_name='menu',
            name='step',
            field=models.IntegerField(blank=True, null=True, verbose_name='层级深度'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='state',
            field=models.BooleanField(default=False, verbose_name='状态'),
        ),
    ]
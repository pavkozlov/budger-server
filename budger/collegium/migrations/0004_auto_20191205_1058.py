# Generated by Django 2.2.6 on 2019-12-05 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collegium', '0003_auto_20191204_2043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ['exec_date'], 'permissions': [('manage_meeting', 'Создание, редактирование и отправка на согласование черновика плана заседания.'), ('approve_meeting', 'Согласование плана заседания.'), ('use_meeting', 'Просмотр согласованного плана заседания.')]},
        ),
    ]
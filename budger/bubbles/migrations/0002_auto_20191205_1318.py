# Generated by Django 2.2.6 on 2019-12-05 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0018_ksoemployee_is_developer'),
        ('bubbles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetfact',
            name='year',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='budgetplan',
            name='year',
            field=models.IntegerField(db_index=True),
        ),
        migrations.CreateModel(
            name='EntityBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(db_index=True)),
                ('amount_plan', models.FloatField(blank=True, null=True)),
                ('amount_fact', models.FloatField(blank=True, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.Entity')),
            ],
            options={
                'unique_together': {('entity', 'year')},
            },
        ),
    ]

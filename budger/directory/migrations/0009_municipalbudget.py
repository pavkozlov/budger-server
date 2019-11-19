from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0008_entity'),
    ]

    operations = [
        migrations.CreateModel(
            name='MunicipalBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_original', models.CharField(max_length=2000)),
                ('title_display', models.CharField(db_index=True, blank=True, null=True, max_length=2000)),
                ('code', models.CharField(db_index=True, max_length=8)),
                ('subordinates', ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
            ],
            options={
                'ordering': ['title_display'],
            },
        ),
    ]

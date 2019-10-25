# Generated by Django 2.2.6 on 2019-10-25 11:25

from django.db import migrations, models
import django.db.models.deletion


def populate_kso_entity(apps, schema_editor):
    """ Добавление entity в KSO """
    Kso = apps.get_model('directory', 'Kso')
    Entity = apps.get_model('directory', 'Entity')

    kso_objects = Kso.objects.all()

    for kso_obj in kso_objects:
        ogrn = kso_obj.ogrn
        try:
            entity = Entity.objects.get(ogrn=ogrn)
            kso_obj.entity = entity
            kso_obj.save()
        except Entity.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0007_entity_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='kso',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='directory.Entity'),
        ),
        migrations.RunPython(populate_kso_entity),
        migrations.RemoveField(
            model_name='kso',
            name='ogrn',
        ),
    ]

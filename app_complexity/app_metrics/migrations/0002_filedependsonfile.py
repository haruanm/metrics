# Generated by Django 3.1.2 on 2021-03-23 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_metrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDependsOnFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_depends_on_destionations', to='app_metrics.file')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_metrics.file')),
            ],
            options={
                'verbose_name': 'FileDependsOnFile',
                'verbose_name_plural': 'FileDependsOnFiles',
            },
        ),
    ]
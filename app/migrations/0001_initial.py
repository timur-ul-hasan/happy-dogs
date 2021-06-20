# Generated by Django 2.2.10 on 2021-06-20 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
            ],
            options={
                'unique_together': {('first_name', 'last_name')},
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='Start Date')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='app.Dog', verbose_name='Dog')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_caracteristics_quizset_caracteristics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizset',
            name='caracteristics',
        ),
        migrations.AddField(
            model_name='quizset',
            name='caracteristics',
            field=models.ManyToManyField(to='listings.caracteristics'),
        ),
    ]

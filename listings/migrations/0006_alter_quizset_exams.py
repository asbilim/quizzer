# Generated by Django 4.2.2 on 2023-07-03 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_alter_quiz_final_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizset',
            name='exams',
            field=models.ManyToManyField(null=True, to='listings.exam'),
        ),
    ]

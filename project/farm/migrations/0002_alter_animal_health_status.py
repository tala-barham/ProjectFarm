# Generated by Django 4.2.6 on 2023-11-03 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='health_status',
            field=models.CharField(choices=[('good', 'Good'), ('bad', 'Bad')], max_length=10),
        ),
    ]
